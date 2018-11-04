import pytest, json
from rest_framework.test import APIRequestFactory, force_authenticate
from tasks.models import (
    Task
)

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
            'is_done': False,
            'is_skipped': False
        },
        'is_verified': True
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
    assert response.data["is_verified"] is True
    assert response.data['annotation']['is_done'] is False

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
    assert response.data['annotation']['is_done'] is True

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
            'is_done': True,
            'is_skipped': False
        },
        'is_verified': True
    }
