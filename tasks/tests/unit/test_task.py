import pytest

from tasks.models import (
    Mission, Task
)

from modules.order_strategy.models import Strategy
from tasks.tests.conftest import add_annotation


@pytest.mark.django_db
def test_tasks(task):
    assert Task.objects.count() == 1


@pytest.mark.django_db
def create_task(task):
    strategy = Strategy.objects.get(name="StaticStrategyLogic")

    # task without mission
    Task.objects.create(name="New task", strategy=strategy)

    # task with mission
    mission = Mission.objects.get(id=1)
    assert mission.tasks.count() == 1
    task = Task.objects.create(name="New task 2", strategy=strategy, mission=mission)
    assert task.mission == mission
    assert mission.tasks.count() == 2


@pytest.mark.django_db
def test_mission_total_exp(task_with_items):
    task = Task.objects.first()
    assert task.total_exp == 10


@pytest.mark.django_db
def test_exclude_items_with_user_annotations(task_with_items, user1, user2):
    task = Task.objects.get(id=1)

    items = task.exclude_items_with_user_annotations(user1)
    assert items.count() == 4

    item = task.items.first()
    annotation, _ = add_annotation(item, user1)

    items = task.exclude_items_with_user_annotations(user1)
    assert items.count() == 3

    items = task.exclude_items_with_user_annotations(user2)
    assert items.count() == 4


@pytest.mark.django_db
def test_annotate_annotations_done(task_with_items, user1, user2):
    task = Task.objects.get(id=1)
    items = task.items.all()

    for item in task.annotate_annotations_done(items):
        assert item.annotations_done == 0

    # Add annotation
    annotation1, _ = add_annotation(item, user1)

    _items = task.annotate_annotations_done(items)
    assert _items.get(id=item.id).annotations_done == 1

    # Add second annotation
    annotation2, _ = add_annotation(item, user2)

    _items = task.annotate_annotations_done(items)
    assert _items.get(id=item.id).annotations_done == 2

    # Set annotation as skipped
    annotation1.skipped = True
    annotation1.save()

    _items = task.annotate_annotations_done(items)
    assert _items.get(id=item.id).annotations_done == 1

    # Set annotation as rejected
    annotation2.rejected = True
    annotation2.save()

    _items = task.annotate_annotations_done(items)
    assert _items.get(id=item.id).annotations_done == 0

    # Set annotation as both rejected and skipped
    annotation2.rejected = True
    annotation2.skipped = True
    annotation2.save()

    _items = task.annotate_annotations_done(items)
    assert _items.get(id=item.id).annotations_done == 0

    # Resetting skipped annotation
    annotation1.skipped = False
    annotation1.save()
    assert _items.get(id=item.id).annotations_done == 1
