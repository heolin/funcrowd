import pytest

from modules.order_strategy.tests.conftest import add_annotation
from tasks.models import Task
from modules.order_strategy.models import Strategy
from modules.order_strategy.exceptions import ActionNotSupported


@pytest.mark.django_db
def test_empty_items(setup_task_with_items, setup_user):
    user = setup_user
    task = Task.objects.first()
    task.strategy = Strategy.objects.get(name="DepthFirstStrategyLogic")

    item = task.next_item(user, None)
    assert item.order == 0

    item = task.next_item(user, None)
    assert item.order == 0

    item = task.next_item(user, item)
    assert item.order == 0

    annotation, _ = add_annotation(item, user)

    item = task.next_item(user, item)
    assert item.order == 1

    annotation, _ = add_annotation(item, user)

    item = task.next_item(user, item)
    assert item.order == 2

    annotation, _ = add_annotation(item, user)

    item = task.next_item(user, item)
    assert item is None

    with pytest.raises(ActionNotSupported):
        task.prev_item(user, item)


@pytest.mark.django_db
def test_items_with_annotations(setup_task_with_annotations, setup_user, setup_other_user):
    user, other_user = setup_user, setup_other_user
    task = Task.objects.first()
    task.strategy = Strategy.objects.get(name="DepthFirstStrategyLogic")

    item = task.next_item(user, None)
    assert item.order == 1
    item = task.next_item(user, item)
    assert item.order == 1

    annotation, _ = add_annotation(item, user)

    item = task.next_item(user, item)
    assert item.order == 2

    item = task.next_item(other_user, item)
    assert item.order == 2

    annotation, _ = add_annotation(item, user)

    item = task.next_item(user, item)
    assert item.order == 0

    item = task.next_item(other_user, item)
    assert item.order == 1


@pytest.mark.django_db
def test_max_annotations(setup_task_with_annotations, setup_user, setup_other_user):
    user, other_user = setup_user, setup_other_user
    task = Task.objects.first()
    task.strategy = Strategy.objects.get(name="DepthFirstStrategyLogic")
    task.max_annotations = 1

    item = task.next_item(user, None)
    assert item.order == 1

    annotation, _ = add_annotation(item, user)

    item = task.next_item(other_user, item)
    assert item.order == 2

    annotation, _ = add_annotation(item, other_user)

    item = task.next_item(user, item)
    assert item is None

    item = task.next_item(other_user, item)
    assert item is None

    with pytest.raises(ActionNotSupported):
        task.prev_item(user, item)


@pytest.mark.django_db
def test_multiple_annotations(setup_task_with_annotations, setup_user, setup_other_user):
    user, other_user = setup_user, setup_other_user
    task = Task.objects.first()
    task.strategy = Strategy.objects.get(name="DepthFirstStrategyLogic")
    task.multiple_annotations = True

    item = task.next_item(user, None)
    assert item.order == 1

    annotation, _ = add_annotation(item, user)

    item = task.next_item(user, item)
    assert item.order == 2

    annotation, _ = add_annotation(item, user)

    item = task.next_item(user, item)
    assert item.order == 0

