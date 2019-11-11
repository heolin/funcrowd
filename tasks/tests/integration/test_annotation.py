import pytest, json, time
from rest_framework.test import APIRequestFactory, force_authenticate

from tasks.api.views.item import TaskNextItem
from tasks.models import (
    Task,
    Item)

from tasks.api.views.annotation import AnnotationDetail


@pytest.mark.django_db
def test_get_annotation(setup_task_with_items, setup_user):
    factory = APIRequestFactory()

    task = Task.objects.first()
    item = task.items.first()

    # get annotation
    request = factory.get('/api/v1/items/{0}/annotation'.format(item.id))
    force_authenticate(request, setup_user)
    view = AnnotationDetail.as_view()
    response = view(request, item.id)
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
    request = factory.get('/api/v1/items/{0}/annotation'.format(100))
    force_authenticate(request, setup_user)
    view = AnnotationDetail.as_view()
    response = view(request, 100)
    assert response.status_code == 404
    assert response.data["detail"].code == "not_found"


@pytest.mark.django_db
def test_post_annotation(setup_task_with_items, setup_user):
    factory = APIRequestFactory()

    task = Task.objects.first()
    item = task.items.first()

    payload = {}
    request = factory.post('/api/v1/items/{0}/annotation'.format(item.id), payload)
    force_authenticate(request, setup_user)
    view = AnnotationDetail.as_view()
    response = view(request, item.id)
    assert response.status_code == 400
    assert response.data[0].code == "invalid"

    # annotation not found
    payload = {}
    request = factory.post('/api/v1/items/{0}/annotation'.format(100), payload)
    force_authenticate(request, setup_user)
    view = AnnotationDetail.as_view()
    response = view(request, 100)
    assert response.status_code == 404
    assert response.data["detail"].code == "not_found"

    # posting empty payload
    payload = {
        "data": json.dumps({})
    }
    request = factory.post('/api/v1/items/{0}/annotation'.format(item.id), payload)
    force_authenticate(request, setup_user)
    view = AnnotationDetail.as_view()
    response = view(request, item.id)
    assert response.status_code == 200
    assert response.data["is_verified"] is False

    # posting empty fields
    payload = {
        'data': json.dumps({'output': '', 'optional': ''}),
    }
    request = factory.post('/api/v1/items/{0}/annotation'.format(item.id), payload)
    force_authenticate(request, setup_user)
    view = AnnotationDetail.as_view()
    response = view(request, item.id)
    assert response.status_code == 200
    assert response.data["is_verified"] is False
    assert len(response.data['errors']) == 1
    assert response.data['errors'][0]['name'] == "RequiredFieldEmptyError"
    assert response.data['errors'][0]['field'] == "output"

    # posting correct payload
    payload = {
        'data': json.dumps({'output': '1', 'optional': ''}),
    }
    request = factory.post('/api/v1/items/{0}/annotation'.format(item.id), payload)
    force_authenticate(request, setup_user)
    view = AnnotationDetail.as_view()
    response = view(request, item.id)
    assert response.status_code == 200
    assert response.data["is_verified"] is True

    # get saved annotation
    request = factory.get('/api/v1/items/{0}/annotation'.format(item.id))
    force_authenticate(request, setup_user)
    view = AnnotationDetail.as_view()
    response = view(request, item.id)
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
    request = factory.post('/api/v1/items/{0}/annotation'.format(item.id), payload)
    force_authenticate(request, setup_user)
    view = AnnotationDetail.as_view()
    response = view(request, item.id)
    assert response.status_code == 200
    assert response.data["is_verified"] is True
    assert response.data["annotation"]["skipped"] is True


@pytest.mark.django_db
def test_annotation_time(setup_task_with_items, setup_user):
    factory = APIRequestFactory()

    task = Task.objects.first()

    request = factory.get('/api/v1/tasks/{0}/next_item'.format(task.id))
    force_authenticate(request, setup_user)
    view = TaskNextItem.as_view()
    response = view(request, task.id)

    item_id = response.data['id']

    time.sleep(1)

    # posting correct payload
    payload = {
        'data': json.dumps({'output': '1', 'optional': ''}),
    }
    request = factory.post('/api/v1/items/{0}/annotation'.format(item_id), payload)
    force_authenticate(request, setup_user)
    view = AnnotationDetail.as_view()
    response = view(request, item_id)
    assert response.status_code == 200
    assert response.data["is_verified"] is True

    item = Item.objects.get(id=item_id)
    annotation, _ = item.get_or_create_annotation(setup_user)
    annotation_time = annotation.updated - annotation.created
    assert annotation_time.total_seconds() > 1
    assert annotation.annotated
