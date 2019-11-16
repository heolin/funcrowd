import pytest

from tasks.models import (
    Task
)
from modules.validators.models.types import (
    FieldTypeValidator
)


@pytest.mark.django_db
def test_type_field_values(task_with_items, user1):
    task = Task.objects.first()
    item = task.items.first()

    annotation, _ = item.get_or_create_annotation(user1)
    is_verified, errors = FieldTypeValidator().verify(annotation)
    assert is_verified is True
    assert len(errors) == 0

    annotation.data['output'] = "C"
    is_verified, errors = FieldTypeValidator().verify(annotation)
    assert is_verified is True
    assert len(errors) == 0

    annotation.data['output'] = 1
    is_verified, errors = FieldTypeValidator().verify(annotation)
    assert is_verified is False
    assert len(errors) == 1
    assert errors[0].name == "FieldTypeError"
    assert errors[0].field == "output"

    field = item.template.fields.get(name="output")
    field.type = "list"
    field.save()

    annotation.data['output'] = [1]
    is_verified, errors = FieldTypeValidator().verify(annotation)
    assert is_verified is True
    assert len(errors) == 0

    annotation.data['output'] = ["S"]
    is_verified, errors = FieldTypeValidator().verify(annotation)
    assert is_verified is True
    assert len(errors) == 0

    annotation.data['output'] = 1
    is_verified, errors = FieldTypeValidator().verify(annotation)
    assert is_verified is False
    assert len(errors) == 1
    assert errors[0].name == "FieldTypeError"
    assert errors[0].field == "output"
