import pytest
from rest_framework.test import APIRequestFactory
from tasks.api.views.item import (
    TaskNextItem, TaskNextItemWithPrevious
)
from tasks.models import Task


def create_item(task_id, item_id, template_id, first_value, second_value,
                field1_id, field2_id, field3_id, field4_id):
    return {
        'id': item_id,
        'task': task_id,
        'data': {'first': first_value, 'second': second_value},
        'template': {
            'id': template_id,
            'fields': [
                {
                    'id': field1_id,
                    'name': 'first',
                    'editable': False,
                    'required': True
                }, {
                    'id': field2_id,
                    'name': 'second',
                    'editable': False,
                    'required': True
                }, {
                    'id': field3_id,
                    'name': 'output',
                    'editable': True,
                    'required': True
                }, {
                    'id': field4_id,
                    'name': 'optional',
                    'editable': True,
                    'required': False
                }
            ]
        }
    }


@pytest.mark.django_db
def test_next_item(setup_task_with_items):
    factory = APIRequestFactory()

    task = Task.objects.first()
    item = task.items.first()
    item_json = create_item(task.id, item.id, item.template.id, 1, 2, 1, 2, 3, 4)

    request = factory.get('/api/v1/tasks/{0}/next_item'.format(task.id))
    view = TaskNextItem.as_view()
    response = view(request, task.id)
    assert response.status_code == 200

    for key in ['id', 'task', 'data']:
        assert response.data[key] == item_json[key]

    assert response.data['template']['id'] == item_json['template']['id']
    for field in response.data['template']['fields']:
        assert field in item_json['template']['fields']


@pytest.mark.django_db
def test_next_item_with_previous(setup_task_with_items, setup_user):
    factory = APIRequestFactory()

    task = Task.objects.first()
    item = task.items.first()

    # next item with previous given
    request = factory.get('/api/v1/items/{0}/next_item'.format(item.id))
    request.user = setup_user
    next_item = item.task.next_item(request.user, item)
    item_json = create_item(task.id, next_item.id, next_item.template.id, 2, 2, 5, 6, 7, 8)

    view = TaskNextItemWithPrevious.as_view()
    response = view(request, item.id)
    assert response.status_code == 200

    for key in ['id', 'task', 'data']:
        assert response.data[key] == item_json[key]

    assert response.data['template']['id'] == item_json['template']['id']
    for field in response.data['template']['fields']:
        assert field in item_json['template']['fields']

    # no next item
    request = factory.get('/api/v1/items/{0}/next_item'.format(next_item.id))
    request.user = setup_user

    view = TaskNextItemWithPrevious.as_view()
    response = view(request, next_item.id)
    assert response.status_code == 204
    assert response.data is None
