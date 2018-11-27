import pytest

from tasks.models import (
    Task, Item, Annotation
)
from tasks.controllers.validators.annotation import (
    AnnotationDoneValidator,
    SourceFieldValuesValidator,
    AnnotationFieldsValidator
)


@pytest.mark.django_db
def test_source_field_values(setup_task_with_items_data_source, setup_user):
    user = setup_user
    task = Task.objects.first()
    item = task.items.first()

    annotation, _ = item.get_or_create_annotation(user)
    is_verified, errors = SourceFieldValuesValidator().verify(annotation)
    assert is_verified is False
    assert len(errors) == 1
    assert errors[0].name == "ValueNotInDataSourceError"
    assert errors[0].field == 'output'

    annotation.data['output'] = "C"
    is_verified, errors = SourceFieldValuesValidator().verify(annotation)
    assert is_verified is False
    assert len(errors) == 1

    annotation.data['output'] = "A"
    is_verified, errors = SourceFieldValuesValidator().verify(annotation)
    assert is_verified is True
    assert len(errors) == 0

    annotation.data['output'] = "B"
    is_verified, errors = SourceFieldValuesValidator().verify(annotation)
    assert is_verified is True
    assert len(errors) == 0


@pytest.mark.django_db
def test_annotation_is_done(setup_task_with_items, setup_user):
    user = setup_user
    task = Task.objects.first()
    item = task.items.first()

    annotation, _ = item.get_or_create_annotation(user)
    is_verified, errors = AnnotationDoneValidator().verify(annotation)
    assert is_verified is False
    assert len(errors) == 1
    assert errors[0].name == "RequiredFieldEmptyError"
    assert errors[0].field == 'output'

    annotation.data['optional'] = "test"
    assert is_verified is False
    assert len(errors) == 1

    annotation.data['output'] = "test"
    is_verified, errors = AnnotationDoneValidator().verify(annotation)
    assert is_verified is True
    assert len(errors) == 0


@pytest.mark.django_db
def test_annotation_fields(setup_task_with_items, setup_user):
    user = setup_user
    task = Task.objects.first()
    item = task.items.first()

    annotation, _ = item.get_or_create_annotation(user)
    is_verified, errors = AnnotationFieldsValidator().verify(annotation)
    assert is_verified is True
    assert len(errors) == 0

    annotation.data = {}
    is_verified, errors = AnnotationFieldsValidator().verify(annotation)
    assert is_verified is False
    assert len(errors) == 1
    assert errors[0].name == "RequiredFieldNotFoundError"
    assert errors[0].field == 'output'

    annotation.data = {"optional": "test"}
    is_verified, errors = AnnotationFieldsValidator().verify(annotation)
    assert is_verified is False
    assert len(errors) == 1
    assert errors[0].name == "RequiredFieldNotFoundError"
    assert errors[0].field == 'output'

    annotation.data = {"output": "test", "other": "test"}
    is_verified, errors = AnnotationFieldsValidator().verify(annotation)
    assert is_verified is False
    assert len(errors) == 1
    assert errors[0].name == "FieldNotInTemplateError"
    assert errors[0].field == 'other'

    annotation.data = {"optional": "test", "output": "test"}
    is_verified, errors = AnnotationFieldsValidator().verify(annotation)
    assert is_verified is True
    assert len(errors) == 0
