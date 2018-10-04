import pytest

from tasks.models import (
    Task, Item, Annotation
)


@pytest.mark.django_db
def test_create_annotations(setup_task_with_items, setup_user, setup_other_user):
    user = setup_user
    task = Task.objects.first()
    item = task.items.first()

    annotation, created = item.get_or_create_annotation(user)
    assert created
    annotation, created = item.get_or_create_annotation(user)
    assert created is False

    assert annotation.verify_fields()
    annotation.data['test'] = 1
    assert annotation.verify_fields() is False
    annotation.data = {"output": "", "optional": ""}

    assert annotation.verify_done() is False
    annotation.data['output'] = 1
    assert annotation.verify_done()

    annotation.data = {"output": "", "optional": ""}
    annotation.data['optional'] = 1
    print(annotation.data)
    assert annotation.verify_done() is False

    assert item.annotations.count() == 1
    other_user = setup_other_user
    annotation, created = item.get_or_create_annotation(other_user)
    assert created
    assert item.annotations.count() == 2
