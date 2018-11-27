import pytest

from tasks.models import Task
from modules.order_strategy.models import Strategy
from modules.order_strategy.exceptions import ActionNotSupported


@pytest.mark.django_db
def test_empty_items(setup_task_with_items, setup_user, setup_db_random):
    user = setup_user
    task = Task.objects.first()
    task.strategy = Strategy.objects.get(name="RandomStrategyLogic")

    orders = set()
    for _ in range(30):
        item = task.next_item(user, None)
        orders.add(item.order)
    assert orders == {0, 1, 2}

    with pytest.raises(ActionNotSupported):
        task.prev_item(user, item)


@pytest.mark.django_db
def test_items_with_annotations(setup_task_with_annotations, setup_user, setup_db_random):
    user = setup_user
    task = Task.objects.first()
    task.strategy = Strategy.objects.get(name="RandomStrategyLogic")

    orders = set()
    for _ in range(30):
        item = task.next_item(user, None)
        orders.add(item.order)
    assert orders == {0, 1, 2}

    item = task.items.first()
    annotation, _ = item.get_or_create_annotation(user)
    annotation.data["output"] = 1
    annotation.save()

    orders = set()
    for _ in range(30):
        item = task.next_item(user, None)
        orders.add(item.order)
    assert orders == {1, 2}


@pytest.mark.django_db
def test_max_annotations(setup_task_with_annotations, setup_user, setup_db_random):
    user = setup_user
    task = Task.objects.first()
    task.strategy = Strategy.objects.get(name="RandomStrategyLogic")
    task.max_annotations = 1

    orders = set()
    for _ in range(30):
        item = task.next_item(user, None)
        orders.add(item.order)
    assert orders == {1, 2}


@pytest.mark.django_db
def test_multiple_annotations(setup_task_with_annotations, setup_user, setup_db_random):
    user = setup_user
    task = Task.objects.first()
    task.strategy = Strategy.objects.get(name="RandomStrategyLogic")
    task.multiple_annotations = True

    orders = set()
    for _ in range(30):
        item = task.next_item(user, None)
        orders.add(item.order)
    assert orders == {0, 1, 2}

    item = task.items.first()
    annotation, _ = item.get_or_create_annotation(user)
    annotation.data["output"] = 1
    annotation.save()

    orders = set()
    for _ in range(30):
        item = task.next_item(user, None)
        orders.add(item.order)
    assert orders == {0, 1, 2}

