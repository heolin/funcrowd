import pytest

from tasks.consts import MissionStatus, TaskStatus
from tasks.models import (
    Task, Item, Annotation,
    Mission)
from tasks.controllers.annotation_controller import AnnotationController
from tasks.tests.conftest import add_annotation


@pytest.mark.django_db
def test_task_progress(task_with_items, user1):
    task = Task.objects.first()

    progress = user1.get_task_progress(task=task)

    assert progress.items_count == 4
    assert progress.items_done == 0
    assert progress.progress == 0
    assert progress.status == TaskStatus.UNLOCKED
    assert progress.max_score == 4
    assert progress.score is None

    item = task.items.first()
    controller = AnnotationController()

    # creating an annotation for the first item
    annotation, _ = item.get_or_create_annotation(user1)
    annotation.data = {"output": "C"}
    annotation.annotated = True
    controller.process(annotation)

    progress = user1.get_task_progress(task=task)
    assert progress.items_done == 1
    assert progress.progress == 0.25
    assert progress.status == TaskStatus.IN_PROGRESS

    # creating new annotation for the first item
    annotation, _ = item.get_or_create_annotation(user1)
    annotation.data = {"output": "B"}
    annotation.annotated = True
    controller.process(annotation)

    progress = user1.get_task_progress(task=task)
    assert progress.items_done == 1
    assert progress.progress == 0.25

    # annotation is not marked as annotated
    annotation, _ = item.get_or_create_annotation(user1)
    annotation.data = {"output": "C"}
    annotation.annotated = False
    annotation.save()
    progress.update()

    progress = user1.get_task_progress(task=task)
    assert progress.items_done == 0
    assert progress.progress == 0.0
    assert progress.status == TaskStatus.IN_PROGRESS

    # annotation is marked as skipped
    annotation, _ = item.get_or_create_annotation(user1)
    annotation.data = {"output": "C"}
    annotation.skipped = True
    annotation.annotated = True
    annotation.save()
    progress.update()

    progress = user1.get_task_progress(task=task)
    assert progress.items_done == 0
    assert progress.progress == 0.0
    assert progress.status == TaskStatus.IN_PROGRESS

    # annotation is marked as rejected
    annotation, _ = item.get_or_create_annotation(user1)
    annotation.data = {"output": "C"}
    annotation.skipped = False
    annotation.rejected = True
    annotation.annotated = True
    annotation.save()
    progress.update()

    progress = user1.get_task_progress(task=task)
    assert progress.items_done == 0
    assert progress.progress == 0.0
    assert progress.status == TaskStatus.IN_PROGRESS

    # setting correct values for first item's annotation
    annotation.annotated = True
    annotation.skipped = False
    annotation.rejected = False
    annotation.save()

    # creating an annotation for the second item
    for item in task.items.all()[1:]:
        annotation, _ = item.get_or_create_annotation(user1)
        annotation.data = {"output": "A"}
        annotation.annotated = True
        controller.process(annotation)

    progress = user1.get_task_progress(task=task)
    assert progress.items_done == 4
    assert progress.progress == 1.0
    assert progress.status == TaskStatus.FINISHED


@pytest.mark.django_db
def test_mission_progress(two_missions, user1):
    mission1 = Mission.objects.get(order=1)
    mission2 = Mission.objects.get(order=2)
    mission3 = Mission.objects.get(order=3)

    # get initial statuses
    progress1 = user1.get_mission_progress(mission=mission1)
    progress2 = user1.get_mission_progress(mission=mission2)
    progress3 = user1.get_mission_progress(mission=mission3)

    assert progress1.status == MissionStatus.UNLOCKED
    assert progress2.status == MissionStatus.LOCKED
    assert progress3.status == MissionStatus.UNLOCKED

    # check initial progress for mission 1
    assert progress1.tasks_count == 1
    assert progress1.tasks_done == 0
    assert progress1.progress == 0

    task = mission1.tasks.first()
    item = task.items.first()
    controller = AnnotationController()

    # creating an annotation for the first item
    annotation, _ = add_annotation(item, user1)
    controller.process(annotation)

    progress = user1.get_mission_progress(mission=task.mission)
    assert progress.tasks_done == 0
    assert progress.progress == 0

    # creating an annotation for the other items
    for item in task.items.all()[1:]:
        annotation, _ = add_annotation(item, user1)
        controller.process(annotation)

    progress = user1.get_mission_progress(mission=mission1)
    assert progress.tasks_done == 1
    assert progress.progress == 1.0

    # check statuses after first task
    progress1 = user1.get_mission_progress(mission=mission1)
    progress2 = user1.get_mission_progress(mission=mission2)
    progress3 = user1.get_mission_progress(mission=mission3)

    assert progress1.status == MissionStatus.FINISHED
    assert progress2.status == MissionStatus.UNLOCKED
    assert progress3.status == MissionStatus.UNLOCKED

    progress = user1.get_mission_progress(mission=mission2)
    assert progress.tasks_done == 0
    assert progress.progress == 0.0

    # start annotating first task of the second mission
    task = mission2.tasks.all()[0]
    item = task.items.first()

    annotation, _ = add_annotation(item, user1)
    controller.process(annotation)

    progress = user1.get_mission_progress(mission=mission2)

    assert progress.tasks_done == 1
    assert progress.progress == 0.5
    assert progress.status == MissionStatus.IN_PROGRESS

    # start annotating second task of the second mission
    task = mission2.tasks.all()[1]
    item = task.items.first()

    annotation, _ = add_annotation(item, user1)
    controller.process(annotation)

    progress = user1.get_mission_progress(mission=mission2)

    assert progress.tasks_done == 2
    assert progress.progress == 1.0
    assert progress.status == MissionStatus.FINISHED


@pytest.mark.django_db
def test_task_progress_with_feedback(task_with_items_with_multiple_annotation_fields, user1):
    task = Task.objects.first()

    progress = user1.get_task_progress(task=task)

    assert progress.items_count == 3
    assert progress.items_done == 0
    assert progress.progress == 0
    assert progress.status == TaskStatus.UNLOCKED
    assert progress.max_score == 6
    assert progress.score is None

    item = task.items.first()
    controller = AnnotationController()

    # creating an annotation for the first item
    annotation = Annotation.objects.create(item=item, user=user1, annotated=True,
                                           data={"first": 1, "second": 1})
    controller.process(annotation)

    progress = user1.get_task_progress(task=task)
    assert progress.items_count == 3
    assert progress.items_done == 1
    assert progress.score == 2

    # creating second annotation for the same item
    annotation = Annotation.objects.create(item=item, user=user1, annotated=True,
                                           data={"first": 1, "second": 0})
    controller.process(annotation)

    progress = user1.get_task_progress(task=task)
    assert progress.items_count == 3
    assert progress.items_done == 1
    assert progress.score == 1
    assert item.annotations.filter(user=user1).count() == 2

    # creating an annotation for the second item
    item = task.items.all()[1]
    annotation = Annotation.objects.create(item=item, user=user1, annotated=True,
                                           data={"first": 1, "second": 1})
    controller.process(annotation)

    progress = user1.get_task_progress(task=task)
    assert progress.items_count == 3
    assert progress.items_done == 2
    assert progress.score == 3

    # creating an annotation for the third item
    item = task.items.all()[2]
    annotation = Annotation.objects.create(item=item, user=user1, annotated=True,
                                           data={"first": 0, "second": 0})
    controller.process(annotation)

    progress = user1.get_task_progress(task=task)
    assert progress.items_count == 3
    assert progress.items_done == 3
    assert progress.score == 3

    # creating second annotation for the third item
    annotation = Annotation.objects.create(item=item, user=user1, annotated=True,
                                           data={"first": 1, "second": 1})
    controller.process(annotation)

    progress = user1.get_task_progress(task=task)
    assert progress.items_count == 3
    assert progress.items_done == 3
    assert progress.score == 5
