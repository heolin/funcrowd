import pytest

from tasks.models import Task
from modules.order_strategy.models import Strategy


@pytest.mark.django_db
def test_empty_items(setup_task_with_items, setup_user):
    user = setup_user
    task = Task.objects.first()
    task.strategy = Strategy.objects.get(name="StaticStrategyLogic")

    item = task.next_item(user, None)
    assert item.order == 0
    item = task.next_item(user, None)
    assert item.order == 0

    item = task.next_item(user, item)
    assert item.order == 1
    item = task.next_item(user, item)
    assert item.order == 2
    item = task.next_item(user, item)
    assert item is None


@pytest.mark.django_db
def test_items_with_annotations(setup_task_with_annotations, setup_user, setup_other_user):
    user = setup_user
    task = Task.objects.first()
    task.strategy = Strategy.objects.get(name="StaticStrategyLogic")

    item = task.next_item(user, None)
    assert item.order == 0
    item = task.next_item(user, item)
    assert item.order == 1
    item = task.next_item(user, item)
    assert item.order == 2
    item = task.next_item(user, item)
    assert item is None

    item = task.items.last()
    item = task.prev_item(user, item)
    assert item.order == 1
    item = task.prev_item(user, item)
    assert item.order == 0
    item = task.prev_item(user, item)
    assert item is None


@pytest.mark.django_db
def test_max_annotations(setup_task_with_annotations, setup_user, setup_other_user):
    user = setup_user
    task = Task.objects.first()
    task.strategy = Strategy.objects.get(name="StaticStrategyLogic")
    task.max_annotations = 1

    item = task.next_item(user, None)
    assert item.order == 0
    item = task.next_item(user, item)
    assert item.order == 1
    item = task.next_item(user, item)
    assert item.order == 2
    item = task.next_item(user, item)
    assert item is None


@pytest.mark.django_db
def test_multiple_annotations(setup_task_with_annotations, setup_user, setup_other_user):
    user = setup_user
    task = Task.objects.first()
    task.strategy = Strategy.objects.get(name="StaticStrategyLogic")
    task.multiple_annotations = True

    item = task.next_item(user, None)
    assert item.order == 0
    item = task.next_item(user, item)
    assert item.order == 1
    item = task.next_item(user, item)
    assert item.order == 2
    item = task.next_item(user, item)
    assert item is None
