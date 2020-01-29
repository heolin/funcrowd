import pytest

from modules.feedback.models import Feedback, FeedbackScoreField
from tasks.consts import EXP_BONUS_1, EXP_BONUS_3
from tasks.models import (
    Task, Annotation
)


@pytest.mark.django_db
def test_create_annotations(task_with_items, user1, user2):
    task = Task.objects.first()
    item = task.items.first()

    annotation, created = item.get_or_create_annotation(user1)
    assert created
    annotation, created = item.get_or_create_annotation(user1)
    assert created is False

    assert item.annotations.count() == 1
    annotation, created = item.get_or_create_annotation(user2)
    assert created
    assert item.annotations.count() == 2


@pytest.mark.django_db
def test_annotation_exp_no_feedback(task_with_items, user1):
    task = Task.objects.first()
    item = task.items.first()

    annotation = Annotation.objects.create(
        item=item,
        user=user1,
        data={"output": "1"},
        annotated=True
    )

    exp_base, exp_bonus = annotation.get_exp()
    assert exp_base == item.exp
    assert exp_bonus == 0

    annotation = Annotation.objects.get(id=annotation.id)
    assert exp_base + exp_bonus == annotation.exp


@pytest.mark.django_db
def test_annotation_exp_feedback(task_with_items, user1):
    FeedbackScoreField.register_values()

    task = Task.objects.first()
    item = task.items.first()

    feedback = Feedback.objects.create(task=task)
    feedback.score_fields.add(FeedbackScoreField.objects.get(name="ReferenceScore"))

    # reference annotation
    Annotation.objects.create(
        item=item,
        user=None,
        data={"output": "1"},
        annotated=True
    )

    # wrong annotation
    annotation = Annotation.objects.create(
        item=item,
        user=user1,
        data={"output": "0"},
        annotated=True
    )
    annotation_feedback = feedback.create_feedback(annotation)
    assert annotation_feedback.score == 0

    exp_base, exp_bonus = annotation.get_exp()
    assert exp_base == 0
    assert exp_bonus == 0

    # correct annotation
    annotation_feedback.delete()  # resetting current feedback
    annotation.data = {"output": "1"}
    annotation.save()

    annotation_feedback = feedback.create_feedback(annotation)
    assert annotation_feedback.score == 1

    exp_base, exp_bonus = annotation.get_exp()
    assert exp_base == item.exp
    assert exp_bonus == 0


@pytest.mark.django_db
def test_annotation_exp_multiple_feedback_scenario_1(task_with_items, user1):
    # scenario 1 - right
    FeedbackScoreField.register_values()

    task = Task.objects.first()
    task.multiple_annotations = True
    task.save()
    item = task.items.first()

    feedback = Feedback.objects.create(task=task)
    feedback.score_fields.add(FeedbackScoreField.objects.get(name="ReferenceScore"))

    # reference annotation
    Annotation.objects.create(
        item=item,
        user=None,
        data={"output": "1"},
        annotated=True
    )

    annotation = Annotation.objects.create(
        item=item,
        user=user1,
        data={"output": "1"},
        annotated=True
    )

    feedback.create_feedback(annotation)
    exp_base, exp_bonus = annotation.get_exp()
    assert exp_base == item.exp
    assert exp_bonus == EXP_BONUS_1


@pytest.mark.django_db
def test_annotation_exp_multiple_feedback_scenario_2(task_with_items, user1):
    # scenario 2 - wrong x 1 + right
    FeedbackScoreField.register_values()

    task = Task.objects.first()
    task.multiple_annotations = True
    task.save()
    item = task.items.first()

    feedback = Feedback.objects.create(task=task)
    feedback.score_fields.add(FeedbackScoreField.objects.get(name="ReferenceScore"))

    # reference annotation
    Annotation.objects.create(
        item=item,
        user=None,
        data={"output": "1"},
        annotated=True
    )

    for _ in range(1):
        annotation = Annotation.objects.create(
            item=item,
            user=user1,
            data={"output": "0"},
            annotated=True
        )
        feedback.create_feedback(annotation)

        exp_base, exp_bonus = annotation.get_exp()
        assert exp_base == 0
        assert exp_bonus == 0

    annotation = Annotation.objects.create(
        item=item,
        user=user1,
        data={"output": "1"},
        annotated=True
    )

    feedback.create_feedback(annotation)
    exp_base, exp_bonus = annotation.get_exp()
    assert exp_base == item.exp
    assert exp_bonus == EXP_BONUS_3


@pytest.mark.django_db
def test_annotation_exp_multiple_feedback_scenario_(task_with_items, user1):
    # scenario 3 - wrong x 3 + right
    FeedbackScoreField.register_values()

    task = Task.objects.first()
    task.multiple_annotations = True
    task.save()
    item = task.items.first()

    feedback = Feedback.objects.create(task=task)
    feedback.score_fields.add(FeedbackScoreField.objects.get(name="ReferenceScore"))

    # reference annotation
    Annotation.objects.create(
        item=item,
        user=None,
        data={"output": "1"},
        annotated=True
    )

    for _ in range(3):
        annotation = Annotation.objects.create(
            item=item,
            user=user1,
            data={"output": "0"},
            annotated=True
        )
        feedback.create_feedback(annotation)

        exp_base, exp_bonus = annotation.get_exp()
        assert exp_base == 0
        assert exp_bonus == 0

    annotation = Annotation.objects.create(
        item=item,
        user=user1,
        data={"output": "1"},
        annotated=True
    )

    feedback.create_feedback(annotation)
    exp_base, exp_bonus = annotation.get_exp()
    assert exp_base == item.exp
    assert exp_bonus == EXP_BONUS_3
