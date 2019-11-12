import pytest

from modules.feedback.models import Feedback, FeedbackScoreField
from tasks.models import (
    Task, Item, Annotation
)
from tasks.controllers.annotation_controller import AnnotationController


@pytest.mark.django_db
def test_annotation_controller(setup_task_with_items_data_source, setup_user):
    user = setup_user
    task = Task.objects.first()
    item = task.items.first()
    controller = AnnotationController()

    annotation, _ = item.get_or_create_annotation(user)
    response = controller.process(annotation)
    assert response.is_verified is False
    assert len(response.errors) == 2
    assert response.errors[0].name == "RequiredFieldEmptyError"
    assert response.errors[0].field == "output"
    assert response.errors[1].name == "ValueNotInDataSourceError"
    assert response.errors[1].field == "output"

    annotation.data = {"output": "C"}
    response = controller.process(annotation)
    assert response.is_verified is False
    assert len(response.errors) == 1
    assert response.errors[0].name == "ValueNotInDataSourceError"
    assert response.errors[0].field == "output"

    annotation.data = {"other": "C"}
    response = controller.process(annotation)
    assert response.is_verified is False
    assert len(response.errors) == 2
    assert response.errors[0].name == "RequiredFieldNotFoundError"
    assert response.errors[0].field == "output"
    assert response.errors[1].name == "FieldNotInTemplateError"
    assert response.errors[1].field == "other"

    annotation.data = {"output": "A"}
    response = controller.process(annotation)
    assert response.is_verified is True

    # test skipped
    annotation.data = {}
    annotation.skipped = True
    response = controller.process(annotation)
    assert response.is_verified is True


@pytest.mark.django_db
def test_annotation_controller_data_source(setup_task_with_items_data_source, setup_user):
    user = setup_user
    task = Task.objects.first()
    item = task.items.first()
    controller = AnnotationController()

    annotation, _ = item.get_or_create_annotation(user)
    annotation.data = {"output": "C"}
    response = controller.process(annotation)
    assert response.is_verified is False
    assert len(response.errors) == 1
    assert response.errors[0].name == "ValueNotInDataSourceError"
    assert response.errors[0].field == "output"

    field = item.template.fields.get(name="output")
    field.validate_data_source = False
    field.save()

    annotation, _ = item.get_or_create_annotation(user)
    annotation.data = {"output": "C"}
    response = controller.process(annotation)
    assert response.is_verified is True


@pytest.mark.django_db
def test_annotation_controller_feedback_autoreject(setup_task_with_items_data_source, setup_user):
    FeedbackScoreField.register_values()

    user = setup_user
    task = Task.objects.first()
    item = task.items.first()

    controller = AnnotationController()

    feedback = Feedback.objects.create(task=task, autoreject=False)
    feedback.score_fields.add(FeedbackScoreField.objects.get(name="ReferenceScore"))

    # add reference annotation
    Annotation.objects.create(
        item=item,
        user=None,
        data={"output": "A"},
        annotated=True
    )

    # correct annotation
    annotation, _ = item.get_or_create_annotation(user)
    annotation.data = {"output": "A"}
    response = controller.process(annotation)
    assert response.is_verified is True
    assert response.annotation.feedback.score == 1.0
    assert response.annotation.rejected is False

    # wrong annotation
    annotation, _ = item.get_or_create_annotation(user)
    annotation.data = {"output": "B"}
    response = controller.process(annotation)
    assert response.is_verified is True
    assert response.annotation.feedback.score == 0.0
    assert response.annotation.rejected is False

    # set autoreject
    feedback.autoreject = True
    feedback.save()

    # correct annotation with autoreject
    annotation, _ = item.get_or_create_annotation(user)
    annotation.data = {"output": "A"}
    response = controller.process(annotation)
    assert response.is_verified is True
    assert response.annotation.feedback.score == 1.0
    assert response.annotation.rejected is False

    # wrong annotation with autoreject
    annotation, _ = item.get_or_create_annotation(user)
    annotation.data = {"output": "B"}
    response = controller.process(annotation)
    assert response.is_verified is True
    assert response.annotation.feedback.score == 0.0
    assert response.annotation.rejected is True
