import pytest
from tasks.models import Mission
from modules.order_strategy.models import Strategy


def add_annotation(package, item, user):
    annotation, created = item.get_or_create_annotation(user)
    annotation.data = {"output": "1"}
    annotation.save()


@pytest.mark.django_db
def test_setup_tasks(setup_task_with_items, setup_user, setup_other_user, setup_db_random):
    user1, user2 = setup_user, setup_other_user

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
def test_max_annotations(setup_task_with_items, setup_user, setup_other_user, setup_db_random):
    user1, user2 = setup_user, setup_other_user

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
def test_multiple_annotations(setup_task_with_items, setup_user, setup_other_user, setup_db_random):
    user1, user2 = setup_user, setup_other_user

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
