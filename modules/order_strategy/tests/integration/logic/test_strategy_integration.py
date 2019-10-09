import pytest

from modules.order_strategy.tests.conftest import get_next_item
from tasks.models import Task
from modules.order_strategy.models import Strategy


@pytest.mark.django_db
def test_breadth_first_strategy_next_item(setup_task_with_items, setup_user):
    user = setup_user
    task = Task.objects.first()
    task.strategy = Strategy.objects.get(name="BreadthFirstStrategyLogic")
    task.save()

    item = task.next_item(user, None)

    next_item_id = get_next_item(task, user)
    assert item.id == next_item_id

    next_item_id = get_next_item(task, user)
    assert item.id == next_item_id


@pytest.mark.django_db
def test_depth_first_strategy_next_item(setup_task_with_items, setup_user):
    user = setup_user
    task = Task.objects.first()
    task.strategy = Strategy.objects.get(name="DepthFirstStrategyLogic")
    task.save()

    item = task.next_item(user, None)

    next_item_id = get_next_item(task, user)
    assert item.id == next_item_id

    next_item_id = get_next_item(task, user)
    assert item.id == next_item_id
