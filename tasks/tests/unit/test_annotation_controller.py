import pytest

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
