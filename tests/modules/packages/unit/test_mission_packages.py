import pytest

from modules.order_strategy.models import Strategy
from modules.packages.models import MissionPackages
from modules.packages.exceptions import InsufficientUnassignedItems


@pytest.mark.django_db
def test_close(packages_with_items):
    mp = packages_with_items
    mp.close()

    for package in mp.packages.all():
        assert package.is_completed


@pytest.mark.django_db
def test_create_package_no_items_left(packages_with_items):
    mp = packages_with_items

    with pytest.raises(InsufficientUnassignedItems):
        mp.create_package(5)


@pytest.mark.django_db
def test_create_package(packages_with_unassigned_items):
    mp = packages_with_unassigned_items

    assert mp.packages.count() == 0

    package1 = mp.create_package(2, metadata={"number": 10})
    assert package1.order == 0
    assert package1.metadata["number"] == 10
    assert package1.items.count() == 2
    assert mp.packages.count() == 1

    with pytest.raises(InsufficientUnassignedItems):
        mp.create_package(2)

    package2 = mp.create_package(1)
    assert package2.order == 1
    assert package2.items.count() == 1
    assert mp.packages.count() == 2


@pytest.mark.django_db
def test_create_package_with_task(packages_with_two_tasks_and_unassigned_items):
    mp = packages_with_two_tasks_and_unassigned_items
    task = mp.mission.tasks.first()

    assert mp.packages.count() == 0

    package = mp.create_package(3, task=task)
    for item in package.items.all():
        assert item.task == task

    with pytest.raises(InsufficientUnassignedItems):
        mp.create_package(3, task=task)
