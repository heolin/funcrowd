import pytest

from tasks.models import (
    Mission, Task
)

from modules.order_strategy.models import Strategy


@pytest.mark.django_db
def test_tasks(setup_task):
    assert Task.objects.count() == 1


@pytest.mark.django_db
def create_task(setup_task):
    strategy = Strategy.objects.get(name="StaticStrategyLogic")

    # task without mission
    Task.objects.create(name="New task", strategy=strategy)

    # task with mission
    mission = Mission.objects.get(id=1)
    assert mission.tasks.count() == 1
    task = Task.objects.create(name="New task 2", strategy=strategy, mission=mission)
    assert task.mission == mission
    assert mission.tasks.count() == 2

