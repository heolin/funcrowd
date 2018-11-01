import pytest
from tasks.models import Mission
from modules.order_strategy.models import Strategy


def add_annotation(package, item, user):
    annotation, created = item.get_or_create_annotation(user)
    annotation.data = {"output": "1"}
    annotation.save()


@pytest.mark.django_db
def test_setup_tasks_one_user(setup_task_with_items, setup_user):
    user1 = setup_user

    mission = Mission.objects.first()
    mp = mission.packages
    mp.strategy = Strategy.objects.get(name="BreadthFirstStrategyLogic")

    package = mp.next_package(user1, None)
    assert package.order == 1
    package = mp.next_package(user1, package)
    assert package.order == 1

    add_annotation(package, package.items.all()[0], user1)
    package = mp.next_package(user1, package)
    assert package.order == 1

    add_annotation(package, package.items.all()[1], user1)
    package = mp.next_package(user1, package)
    assert package.order == 2

    add_annotation(package, package.items.all()[0], user1)
    add_annotation(package, package.items.all()[1], user1)
    package = mp.next_package(user1, package)
    assert package.order == 3

    add_annotation(package, package.items.all()[0], user1)
    add_annotation(package, package.items.all()[1], user1)
    package = mp.next_package(user1, package)
    assert package.order == 4

    add_annotation(package, package.items.all()[0], user1)
    add_annotation(package, package.items.all()[1], user1)
    package = mp.next_package(user1, package)
    assert package is None


@pytest.mark.django_db
def test_setup_tasks_two_users(setup_task_with_items, setup_user, setup_other_user):
    user1, user2 = setup_user, setup_other_user

    mission = Mission.objects.first()
    mp = mission.packages
    mp.strategy = Strategy.objects.get(name="BreadthFirstStrategyLogic")

    package = mp.next_package(user1, None)
    assert package.order == 1
    add_annotation(package, package.items.all()[0], user1)
    add_annotation(package, package.items.all()[1], user1)

    package = mp.next_package(user2, package)
    assert package.order == 1
    add_annotation(package, package.items.all()[0], user2)
    add_annotation(package, package.items.all()[1], user2)

    package = mp.next_package(user1, package)
    assert package.order == 2
    add_annotation(package, package.items.all()[0], user1)

    package = mp.next_package(user2, package)
    assert package.order == 2
    add_annotation(package, package.items.all()[0], user2)

    package = mp.next_package(user2, package)
    assert package.order == 2

    add_annotation(package, package.items.all()[1], user2)
    package = mp.next_package(user2, package)
    assert package.order == 3


@pytest.mark.django_db
def test_max_annotations(setup_task_with_items, setup_user, setup_other_user):
    user1, user2 = setup_user, setup_other_user

    mission = Mission.objects.first()
    mp = mission.packages
    mp.strategy = Strategy.objects.get(name="BreadthFirstStrategyLogic")
    mp.max_annotations = 1

    package = mp.next_package(user1, None)
    assert package.order == 1
    add_annotation(package, package.items.all()[0], user1)
    add_annotation(package, package.items.all()[1], user1)

    package = mp.next_package(user2, None)
    assert package.order == 2
    add_annotation(package, package.items.all()[0], user2)
    add_annotation(package, package.items.all()[1], user2)

    package = mp.next_package(user2, None)
    assert package.order == 3

    add_annotation(package, package.items.all()[0], user1)
    add_annotation(package, package.items.all()[1], user1)

    package = mp.next_package(user1, None)
    assert package.order == 4

    add_annotation(package, package.items.all()[0], user1)
    add_annotation(package, package.items.all()[1], user1)

    package = mp.next_package(user1, None)
    assert package is None


@pytest.mark.django_db
def test_multiple_annotations(setup_task_with_items, setup_user, setup_other_user):
    user1, user2 = setup_user, setup_other_user

    mission = Mission.objects.first()
    mp = mission.packages
    mp.strategy = Strategy.objects.get(name="BreadthFirstStrategyLogic")
    mp.max_annotations = 2
    mp.multiple_annotations = True
    for task in mission.tasks.all():
        task.multiple_annotations = mp.multiple_annotations
        task.save()

    package = mp.next_package(user1, None)
    assert package.order == 1
    add_annotation(package, package.items.all()[0], user1)
    add_annotation(package, package.items.all()[1], user1)

    package = mp.next_package(user2, None)
    assert package.order == 1

    package = mp.next_package(user1, None)
    assert package.order == 1
    add_annotation(package, package.items.all()[0], user1)
    add_annotation(package, package.items.all()[1], user1)

    package = mp.next_package(user1, None)
    assert package.order == 2
    add_annotation(package, package.items.all()[0], user1)
    add_annotation(package, package.items.all()[1], user1)

    package = mp.next_package(user2, None)
    assert package.order == 2
    add_annotation(package, package.items.all()[0], user2)
    add_annotation(package, package.items.all()[1], user2)

    package = mp.next_package(user2, None)
    assert package.order == 3

    for _ in range(2):
        package = mp.next_package(user1, None)
        add_annotation(package, package.items.all()[0], user1)
        add_annotation(package, package.items.all()[1], user1)
        add_annotation(package, package.items.all()[0], user2)
        add_annotation(package, package.items.all()[1], user2)

    package = mp.next_package(user2, None)
    assert package is None
