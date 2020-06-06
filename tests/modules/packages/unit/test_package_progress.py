import pytest

from modules.packages.consts import UserPackageStatus
from modules.packages.models import UserPackageProgress
from tests.modules.packages.conftest import add_annotation
from tasks.models import Mission


@pytest.mark.django_db
def test_package_progress(packages_with_items, user1):
    mp = packages_with_items
    package = mp.packages.all()[0]

    upp = package.get_user_progress(user1)
    assert upp.items_done == 0
    assert upp.status == UserPackageStatus.NONE

    item = package.items.all()[0]
    add_annotation(item, user1)

    upp = package.get_user_progress(user1)
    assert upp.items_done == 1
    assert upp.status == UserPackageStatus.IN_PROGRESS
    assert upp.reward_token is not None
    assert upp.reward is None

    item = package.items.all()[1]
    add_annotation(item, user1)

    upp = package.get_user_progress(user1)
    assert upp.items_done == 2
    assert upp.status == UserPackageStatus.FINISHED
    assert upp.reward is not None


@pytest.mark.django_db
def test_close_do_not_affect_finished_status(packages_with_annotated_items):
    mp = packages_with_annotated_items

    # Package already finished
    package = mp.packages.all()[0]
    for upp in UserPackageProgress.objects.filter(package=package):
        assert upp.status == UserPackageStatus.FINISHED

    package.close()

    for upp in UserPackageProgress.objects.filter(package=package):
        assert upp.status == UserPackageStatus.FINISHED


@pytest.mark.django_db
def test_close(packages_with_annotated_items, user1):
    mp = packages_with_annotated_items

    # Package not finished
    package = mp.packages.all()[2]

    upp = UserPackageProgress.objects.get(package=package, user=user1)
    assert upp.status == UserPackageStatus.IN_PROGRESS

    package.close()

    upp = UserPackageProgress.objects.get(package=package, user=user1)
    assert upp.status == UserPackageStatus.CLOSED


@pytest.mark.django_db
def test_is_completed(packages_with_annotated_items, user1, user2):
    mp = packages_with_annotated_items

    # Package not finished
    package = mp.packages.all()[1]

    # user already completed the task
    upp = package.get_user_progress(user1)
    assert upp.status == UserPackageStatus.FINISHED
    assert upp.is_completed

    # user not completed the task
    upp = package.get_user_progress(user2)
    assert upp.status == UserPackageStatus.NONE
    assert not upp.is_completed
    package.close()
    upp = package.get_user_progress(user2)
    assert upp.is_completed


@pytest.mark.django_db
def test_update(packages_with_items, user1):
    mp = packages_with_items
    package = mp.packages.all()[0]

    upp = package.get_user_progress(user1)
    assert upp.status == UserPackageStatus.NONE

    item = package.items.all()[0]
    add_annotation(item, user1)
    upp.update()
    assert upp.status == UserPackageStatus.IN_PROGRESS

    item = package.items.all()[1]
    add_annotation(item, user1)
    upp.update()
    assert upp.status == UserPackageStatus.FINISHED
