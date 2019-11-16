import pytest

from modules.packages.tests.conftest import add_annotation
from tasks.models import Mission
from modules.order_strategy.models import Strategy


@pytest.mark.django_db
def test_tasks(task_with_items, user1, user2, db_random):
    mission = Mission.objects.first()
    mp = mission.packages
    mp.strategy = Strategy.objects.get(name="RandomStrategyLogic")

    orders = set()
    for _ in range(30):
        package = mp.next_package(user1, None)
        orders.add(package.order)
    assert orders == {1, 2, 3, 4}

    package = mp.packages.first()
    add_annotation(package, package.items.all()[0], user1)
    add_annotation(package, package.items.all()[1], user1)

    orders = set()
    for _ in range(30):
        package = mp.next_package(user1, None)
        orders.add(package.order)
    assert orders == {2, 3, 4}

    orders = set()
    for _ in range(30):
        package = mp.next_package(user2, None)
        orders.add(package.order)
    assert orders == {1, 2, 3, 4}


@pytest.mark.django_db
def test_max_annotations(task_with_items, user1, user2, db_random):
    mission = Mission.objects.first()
    mp = mission.packages
    mp.strategy = Strategy.objects.get(name="RandomStrategyLogic")
    mp.max_annotations = 1

    orders = set()
    for _ in range(30):
        package = mp.next_package(user1, None)
        orders.add(package.order)
    assert orders == {1, 2, 3, 4}

    package = mp.packages.first()
    add_annotation(package, package.items.all()[0], user1)
    add_annotation(package, package.items.all()[1], user1)

    orders = set()
    for _ in range(30):
        package = mp.next_package(user1, None)
        orders.add(package.order)
    assert orders == {2, 3, 4}

    orders = set()
    for _ in range(30):
        package = mp.next_package(user2, None)
        orders.add(package.order)
    assert orders == {2, 3, 4}


@pytest.mark.django_db
def test_multiple_annotations(task_with_items, user1, user2, db_random):
    mission = Mission.objects.first()
    mp = mission.packages
    mp.strategy = Strategy.objects.get(name="RandomStrategyLogic")
    mp.max_annotations = 2
    mp.multiple_annotations = True
    for task in mission.tasks.all():
        task.multiple_annotations = mp.multiple_annotations
        task.save()

    orders = set()
    for _ in range(30):
        package = mp.next_package(user1, None)
        orders.add(package.order)
    assert orders == {1, 2, 3, 4}

    package = mp.packages.first()
    add_annotation(package, package.items.all()[0], user1)
    add_annotation(package, package.items.all()[1], user1)

    orders = set()
    for _ in range(30):
        package = mp.next_package(user1, None)
        orders.add(package.order)
    assert orders == {1, 2, 3, 4}

    orders = set()
    for _ in range(30):
        package = mp.next_package(user2, None)
        orders.add(package.order)
    assert orders == {1, 2, 3, 4}

    package = mp.packages.first()
    add_annotation(package, package.items.all()[0], user2)
    add_annotation(package, package.items.all()[1], user2)

    orders = set()
    for _ in range(30):
        package = mp.next_package(user1, None)
        orders.add(package.order)
    assert orders == {2, 3, 4}

    orders = set()
    for _ in range(30):
        package = mp.next_package(user2, None)
        orders.add(package.order)
    assert orders == {2, 3, 4}
