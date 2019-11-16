import json
import pytest
import time
from django.test import Client

from tasks.models import Task, Item


@pytest.mark.django_db
def test_get_annotation(task_with_items, user1):
    client = Client()
    client.force_login(user1)

    task = Task.objects.first()
    item = task.items.first()

    # get annotation
    response = client.get('/api/v1/items/{0}/annotation'.format(item.id))
    assert response.status_code == 200
    assert response.data == {
        "annotation": {
            'item_id': item.id,
            'data': {'output': '', 'optional': ''},
            'skipped': False,
            'feedback': None
        },
        'is_verified': False,
        'exp_base': None,
        'exp_bonus': None,
        'errors': [
            {
                'name': 'RequiredFieldEmptyError',
                'field': 'output',
                'message': 'Required field was empty.'
            }
        ]
    }

    # annotation not found
    response = client.get('/api/v1/items/{0}/annotation'.format(100))
    assert response.status_code == 404
    assert response.data["detail"].code == "not_found"


@pytest.mark.django_db
def test_post_annotation(task_with_items, user1):
    task = Task.objects.first()
    item = task.items.first()

    client = Client()
    client.force_login(user1)

    payload = {}
    response = client.post('/api/v1/items/{0}/annotation'.format(item.id), payload)
    assert response.status_code == 400
    assert response.data[0].code == "invalid"

    # annotation not found
    payload = {}
    response = client.post('/api/v1/items/{0}/annotation'.format(100), payload)
    assert response.status_code == 404
    assert response.data["detail"].code == "not_found"

    # posting empty payload
    payload = {
        "data": json.dumps({})
    }
    response = client.post('/api/v1/items/{0}/annotation'.format(item.id), payload)
    assert response.status_code == 200
    assert response.data["is_verified"] is False

    # posting empty fields
    payload = {
        'data': json.dumps({'output': '', 'optional': ''}),
    }
    response = client.post('/api/v1/items/{0}/annotation'.format(item.id), payload)
    assert response.status_code == 200
    assert response.data["is_verified"] is False
    assert len(response.data['errors']) == 1
    assert response.data['errors'][0]['name'] == "RequiredFieldEmptyError"
    assert response.data['errors'][0]['field'] == "output"

    # posting correct payload
    payload = {
        'data': json.dumps({'output': '1', 'optional': ''}),
    }
    response = client.post('/api/v1/items/{0}/annotation'.format(item.id), payload)
    assert response.status_code == 200
    assert response.data["is_verified"] is True

    # get saved annotation
    response = client.get('/api/v1/items/{0}/annotation'.format(item.id))
    assert response.status_code == 200
    assert response.data == {
        "annotation": {
            'item_id': item.id,
            'data': {'output': '1', 'optional': ''},
            'skipped': False,
            'feedback': None
        },
        'exp_base': 0,
        'exp_bonus': 0,
        'is_verified': True,
        'errors': []
    }

    # posting correct skipped annotation
    payload = {
        'data': json.dumps({'output': '', 'optional': ''}),
        'skipped': True
    }
    response = client.post('/api/v1/items/{0}/annotation'.format(item.id), payload)
    assert response.status_code == 200
    assert response.data["is_verified"] is True
    assert response.data["annotation"]["skipped"] is True


@pytest.mark.django_db
def test_annotation_time(task_with_items, user1):
    client = Client()
    client.force_login(user1)

    task = Task.objects.first()

    response = client.get('/api/v1/tasks/{0}/next_item'.format(task.id))
    item_id = response.data['id']

    time.sleep(1)

    # posting correct payload
    payload = {
        'data': json.dumps({'output': '1', 'optional': ''}),
    }
    response = client.post('/api/v1/items/{0}/annotation'.format(item_id), payload)
    assert response.status_code == 200
    assert response.data["is_verified"] is True

    item = Item.objects.get(id=item_id)
    annotation, _ = item.get_or_create_annotation(user1)
    annotation_time = annotation.updated - annotation.created
    assert annotation_time.total_seconds() > 1
    assert annotation.annotated
