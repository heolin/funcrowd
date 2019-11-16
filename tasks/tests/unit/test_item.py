import pytest

from tasks.models import (
    Task, Item, ItemTemplate
)


@pytest.mark.django_db
def test_items(task_with_items):
    assert Task.objects.count() == 1
    task = Task.objects.first()
    assert task.items.count() == 4
    assert Item.objects.count() == 4

    for item in task.items.all():
        assert item.verify_fields()


@pytest.mark.django_db
def test_create_items(task_with_items):
    task = Task.objects.first()

    assert task.items.count() == 4

    template = ItemTemplate.objects.first()
    data = {field.name: "" for field in template.items_fields.all()}
    item = Item.objects.create(task=task, template=template, data=data)
    assert item.verify_fields()
    assert task.items.count() == 5

    item.data = {}
    assert item.verify_fields() is False

    item.data = {"first": "", "second": ""}
    assert item.verify_fields()

    item.data = data
    item.data['first'] = 1
    assert item.verify_fields()

    item.data['test'] = 1
    assert item.verify_fields() is False

    assert item.index == 1
    item.order = 0
    assert item.index == 1
    item.order = 4
    assert item.index == 5
