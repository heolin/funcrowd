import pytest

from modules.order_strategy.models import Strategy
from modules.packages.models import MissionPackages
from tests.modules.packages.exceptions import InsufficientUnassignedItems


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
def test_create_package(one_task_items_with_reference_annotation):
    task = one_task_items_with_reference_annotation
    mission = task.mission
    strategy = Strategy.objects.get(name="StaticStrategyLogic")
    mp = MissionPackages.objects.create(mission=mission, strategy=strategy, max_annotations=4)

    assert mp.packages.count() == 0

    package1 = mp.create_package(2)
    assert mp.packages.count() == 1
    assert package1.items.count() == 2

    with pytest.raises(InsufficientUnassignedItems):
        mp.create_package(2)

    package2 = mp.create_package(1)
    assert mp.packages.count() == 2
    assert package2.items.count() == 1
