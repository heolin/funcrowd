import pytest

from modules.packages.consts import UserPackageStatus, PackageStatus
from modules.packages.models import UserPackageProgress
from tests.utils import add_annotation


@pytest.mark.django_db
def test_setup_tasks(packages_with_items):
    mp = packages_with_items
    assert mp.packages.count() == 5

    mission = mp.mission
    assert mission.packages is not None

    package = mp.packages.all()[0]
    assert package.items.count() == 2
    item1, item2 = package.items.all()[0], package.items.all()[1]
    assert item1.data["data_field"] == "task1 item1"
    assert item2.data["data_field"] == "task2 item1"

    package = mp.packages.all()[1]
    item1, item2 = package.items.all()[0], package.items.all()[1]
    assert item1.data["data_field"] == "task1 item2"
    assert item2.data["data_field"] == "task2 item2"


@pytest.mark.django_db
def test_close_do_not_affect_finished_status(packages_with_annotated_items):
    mp = packages_with_annotated_items

    # Package already finished
    package = mp.packages.all()[0]
    package.close()

    assert package.status != PackageStatus.CLOSED


@pytest.mark.django_db
def test_close(packages_with_items):
    mp = packages_with_items

    # Package not finished
    package = mp.packages.all()[0]
    assert package.status != PackageStatus.CLOSED


@pytest.mark.django_db
def test_get_user_progress(packages_with_annotated_items, user1, user2):
    mp = packages_with_annotated_items

    # Package not finished
    package = mp.packages.all()[2]

    upp = package.get_user_progress(user1)
    assert upp.status == UserPackageStatus.IN_PROGRESS

    upp = package.get_user_progress(user2)
    assert upp.status == UserPackageStatus.NONE


@pytest.mark.django_db
def test_is_completed(packages_with_annotated_items, user1, user2):
    mp = packages_with_annotated_items

    # Package finished
    package = mp.packages.all()[0]
    assert package.is_completed

    # Package not finished
    package = mp.packages.all()[1]
    assert not package.is_completed

    package.close()
    assert package.is_completed


@pytest.mark.django_db
def test_get_aggregations(packages_with_annotated_items):
    mp = packages_with_annotated_items

    # two users finished the package
    package = mp.packages.all()[0]
    probability, support, annotations_count = package._get_aggregations()
    assert probability == 1.0
    assert support == 2
    assert annotations_count == 2

    # one user finished the package
    package = mp.packages.all()[1]
    probability, support, annotations_count = package._get_aggregations()
    assert probability == 1.0
    assert support == 1
    assert annotations_count == 1

    # one user started annotation, but not finished
    package = mp.packages.all()[2]
    probability, support, annotations_count = package._get_aggregations()
    assert probability == 0.5
    assert support == 0
    assert annotations_count == 0


@pytest.mark.django_db
def test_update_status(packages_with_items, user1, user2):
    mp = packages_with_items

    # package requires two annotations for two items
    package = mp.packages.all()[0]
    package.update_status()
    assert package.status == PackageStatus.NONE

    # first user
    item = package.items.all()[0]
    add_annotation(item, user1)
    package.update_status()
    assert package.status == PackageStatus.NONE

    item = package.items.all()[1]
    add_annotation(item, user1)
    package.update_status()
    assert package.status == PackageStatus.IN_PROGRESS

    # second user
    item = package.items.all()[0]
    add_annotation(item, user2)
    item = package.items.all()[1]
    add_annotation(item, user2)
    package.update_status()
    assert package.status == PackageStatus.FINISHED
