import pytest
from tasks.models import Mission
from modules.order_strategy.models import Strategy


@pytest.mark.django_db
def test_tasks(task_with_items, user1, user2):
    mission = Mission.objects.first()
    mp = mission.packages
    mp.strategy = Strategy.objects.get(name="StaticStrategyLogic")

    package = mp.next_package(user1, None)
    assert package.order == 1
    package = mp.next_package(user1, package)
    assert package.order == 2
    package = mp.next_package(user1, package)
    assert package.order == 3
    package = mp.next_package(user1, package)
    assert package.order == 4
    package = mp.next_package(user1, package)
    assert package.order == 5
    package = mp.next_package(user1, package)
    assert package is None

    package = mp.next_package(user2, None)
    assert package.order == 1


@pytest.mark.django_db
def test_annotations(annotations, user1, user2):
    mission = Mission.objects.first()
    mp = mission.packages
    mp.strategy = Strategy.objects.get(name="StaticStrategyLogic")

    package = mp.next_package(user1, None)
    assert package.order == 1
    package = mp.next_package(user1, package)
    assert package.order == 2

    package = mp.next_package(user2, None)
    assert package.order == 1


@pytest.mark.django_db
def test_max_annotations(annotations, user1, user2):
    mission = Mission.objects.first()
    mp = mission.packages
    mp.strategy = Strategy.objects.get(name="StaticStrategyLogic")
    mp.max_annotations = 1

    package = mp.next_package(user1, None)
    assert package.order == 1
    package = mp.next_package(user1, package)
    assert package.order == 2

    package = mp.next_package(user2, None)
    assert package.order == 1


@pytest.mark.django_db
def test_multiple_annotations(annotations, user1, user2):
    mission = Mission.objects.first()
    mp = mission.packages
    mp.strategy = Strategy.objects.get(name="StaticStrategyLogic")
    mp.multiple_annotations = True

    package = mp.next_package(user1, None)
    assert package.order == 1
    package = mp.next_package(user1, package)
    assert package.order == 2

    package = mp.next_package(user2, None)
    assert package.order == 1
