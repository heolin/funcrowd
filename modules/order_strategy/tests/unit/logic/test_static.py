import pytest

from tasks.models import Task
from modules.order_strategy.models import Strategy
from tasks.tests.conftest import add_annotation


@pytest.mark.django_db
def test_empty_items(task_with_items, user1):
    task = Task.objects.first()
    task.strategy = Strategy.objects.get(name="StaticStrategyLogic")
    task.multiple_annotations = True

    item = task.next_item(user1, None)
    assert item.order == 0

    annotation, _ = add_annotation(item, user1)

    item = task.next_item(user1, None)
    assert item.order == 0

    item = task.next_item(user1, item)
    assert item.order == 1
    item = task.next_item(user1, item)
    assert item.order == 2
    item = task.next_item(user1, item)
    assert item is None


@pytest.mark.django_db
def test_items_with_annotations(task_with_annotations, user1, user2):
    task = Task.objects.first()
    task.strategy = Strategy.objects.get(name="StaticStrategyLogic")
    task.multiple_annotations = True

    item = task.next_item(user1, None)
    assert item.order == 0

    annotation, _ = add_annotation(item, user1)

    item = task.next_item(user1, item)
    assert item.order == 1
    item = task.next_item(user1, item)
    assert item.order == 2
    item = task.next_item(user1, item)
    assert item is None

    item = task.items.last()
    item = task.prev_item(user1, item)
    assert item.order == 1
    item = task.prev_item(user1, item)
    assert item.order == 0
    item = task.prev_item(user1, item)
    assert item is None


@pytest.mark.django_db
def test_max_annotations(task_with_annotations, user1, user2):
    task = Task.objects.first()
    task.strategy = Strategy.objects.get(name="StaticStrategyLogic")
    task.max_annotations = 1
    task.multiple_annotations = True

    item = task.next_item(user1, None)
    assert item.order == 0

    annotation, _ = add_annotation(item, user1)

    item = task.next_item(user1, item)
    assert item.order == 1
    item = task.next_item(user1, item)
    assert item.order == 2
    item = task.next_item(user1, item)
    assert item is None
