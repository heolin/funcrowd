import pytest

from modules.packages.consts import UserPackageStatus
from modules.packages.tests.conftest import add_annotation
from tasks.models import Mission


@pytest.mark.django_db
def test_package_progress(task_with_items, user1):
    mission = Mission.objects.first()
    mp = mission.packages
    package = mp.packages.all()[0]

    progress = package.get_user_progress(user1)
    assert progress.items_done == 0
    assert progress.status == UserPackageStatus.NONE

    item = package.items.all()[0]
    add_annotation(package, item, user1)

    progress = package.get_user_progress(user1)
    assert progress.items_done == 1
    assert progress.status == UserPackageStatus.IN_PROGRESS

    item = package.items.all()[1]
    add_annotation(package, item, user1)

    progress = package.get_user_progress(user1)
    assert progress.items_done == 2
    assert progress.status == UserPackageStatus.FINISHED
