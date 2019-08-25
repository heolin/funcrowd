import pytest

from tasks.models import (
    Task, Item, Annotation
)
from tasks.controllers.annotation_controller import AnnotationController


@pytest.mark.django_db
def test_task_progress(setup_task_with_items, setup_user):
    user = setup_user
    task = Task.objects.first()

    progress = user.get_task_progress(task=task)

    assert progress.items_count == 2
    assert progress.items_done == 0
    assert progress.progress == 0

    item = task.items.first()
    controller = AnnotationController()

    # creating an annotation for the first item
    annotation, _ = item.get_or_create_annotation(user)
    annotation.data = {"output": "C"}
    controller.process(annotation)

    progress = user.get_task_progress(task=task)
    assert progress.items_done == 1
    assert progress.progress == 0.5

    # creating new annotation for the first item
    annotation, _ = item.get_or_create_annotation(user)
    annotation.data = {"output": "B"}
    controller.process(annotation)

    progress = user.get_task_progress(task=task)
    assert progress.items_done == 1
    assert progress.progress == 0.5

    # creating an annotation for the second item
    item = task.items.all()[1]

    annotation, _ = item.get_or_create_annotation(user)
    annotation.data = {"output": "A"}
    controller.process(annotation)

    progress = user.get_task_progress(task=task)
    assert progress.items_done == 2
    assert progress.progress == 1.0


@pytest.mark.django_db
def test_mission_progress(setup_task_with_items, setup_user):
    user = setup_user
    task = Task.objects.first()

    progress = user.get_mission_progress(mission=task.mission)

    assert progress.tasks_count == 1
    assert progress.tasks_done == 0
    assert progress.progress == 0

    item = task.items.first()
    controller = AnnotationController()

    # creating an annotation for the first item
    annotation, _ = item.get_or_create_annotation(user)
    annotation.data = {"output": "C"}
    controller.process(annotation)

    progress = user.get_mission_progress(mission=task.mission)
    assert progress.tasks_done == 0
    assert progress.progress == 0

    # creating an annotation for the second item
    item = task.items.all()[1]
    annotation, _ = item.get_or_create_annotation(user)
    annotation.data = {"output": "A"}
    controller.process(annotation)

    progress = user.get_mission_progress(mission=task.mission)
    assert progress.tasks_done == 1
    assert progress.progress == 1.0
