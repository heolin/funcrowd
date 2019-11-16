import pytest

from modules.order_strategy.tests.conftest import add_annotation
from tasks.models import Task
from modules.order_strategy.models import Strategy
from modules.order_strategy.exceptions import ActionNotSupported


@pytest.mark.django_db
def test_empty_items(task_with_items, user1):
    task = Task.objects.first()
    task.strategy = Strategy.objects.get(name="BreadthFirstStrategyLogic")

    item = task.next_item(user1, None)
    assert item.order == 0

    item = task.next_item(user1, None)
    assert item.order == 0

    item = task.next_item(user1, item)
    assert item.order == 0

    annotation, _ = add_annotation(item, user1)

    item = task.next_item(user1, item)
    assert item.order == 1

    annotation, _ = add_annotation(item, user1)

    item = task.next_item(user1, item)
    assert item.order == 2

    annotation, _ = add_annotation(item, user1)

    item = task.next_item(user1, item)
    assert item is None

    with pytest.raises(ActionNotSupported):
        task.prev_item(user1, item)


@pytest.mark.django_db
def test_items_with_annotations(task_with_annotations, user1, user2):
    task = Task.objects.first()
    task.strategy = Strategy.objects.get(name="BreadthFirstStrategyLogic")

    item = task.next_item(user2, None)
    assert item.order == 1

    item = task.next_item(user1, None)
    assert item.order == 0
    item = task.next_item(user1, item)
    assert item.order == 0

    annotation, _ = add_annotation(item, user1)

    item = task.next_item(user1, item)
    assert item.order == 1

    item = task.next_item(user2, None)
    assert item.order == 1

    annotation, _ = add_annotation(item, user2)

    item = task.next_item(user1, item)
    assert item.order == 1

    item = task.next_item(user2, item)
    assert item.order == 2

    annotation, _ = add_annotation(item, user2)

    item = task.next_item(user2, item)
    assert item is None


@pytest.mark.django_db
def test_annotations_skip_and_reject(task_with_annotations, user1, user2):
    task = Task.objects.first()
    task.strategy = Strategy.objects.get(name="BreadthFirstStrategyLogic")

    item = task.next_item(user1, None)
    assert item.order == 0
    item = task.next_item(user1, item)
    assert item.order == 0
    item = task.next_item(user2, item)
    assert item.order == 1

    annotation = task.items.first().annotations.get(user=user2)
    annotation.rejected = True
    annotation.skipped = False
    annotation.save()

    item = task.next_item(user1, item)
    assert item.order == 0

    item = task.next_item(user2, item)
    assert item.order == 1

    annotation.rejected = True
    annotation.skipped = True
    annotation.save()

    item = task.next_item(user1, item)
    assert item.order == 0

    item = task.next_item(user2, item)
    assert item.order == 1

    annotation.rejected = False
    annotation.skipped = True
    annotation.save()

    item = task.next_item(user1, item)
    assert item.order == 0

    item = task.next_item(user2, item)
    assert item.order == 1


@pytest.mark.django_db
def test_max_annotations(task_with_annotations, user1, user2):
    task = Task.objects.first()
    task.strategy = Strategy.objects.get(name="BreadthFirstStrategyLogic")
    task.max_annotations = 1

    item = task.next_item(user1, None)
    assert item.order == 1

    annotation, _ = add_annotation(item, user1)

    item = task.next_item(user2, item)
    assert item.order == 2

    annotation, _ = add_annotation(item, user2)

    item = task.next_item(user1, item)
    assert item is None

    item = task.next_item(user2, item)
    assert item is None


@pytest.mark.django_db
def test_multiple_annotations(task_with_annotations, user1, user2):
    task = Task.objects.first()
    task.strategy = Strategy.objects.get(name="BreadthFirstStrategyLogic")
    task.multiple_annotations = True
    task.max_annotations = 2

    item = task.next_item(user1, None)
    assert item.order == 0

    annotation, _ = add_annotation(item, user1)

    item = task.next_item(user1, item)
    assert item.order == 1

    annotation, _ = add_annotation(item, user1)

    item = task.next_item(user1, item)
    assert item.order == 1

    annotation, _ = add_annotation(item, user1)

    item = task.next_item(user1, item)
    assert item.order == 2

    annotation, _ = add_annotation(item, user1)

    item = task.next_item(user1, item)
    assert item.order == 2

    annotation, _ = add_annotation(item, user1)

    item = task.next_item(user1, item)
    assert item is None
