import pytest

from tasks.models import (
    Mission, Task, Item
)

from modules.order_strategy.models import Strategy


@pytest.mark.django_db
def test_items(setup_task_with_items):
    assert Task.objects.count() == 1
    task = Task.objects.first()
    assert task.items.count() == 2
    assert Item.objects.count() == 2

