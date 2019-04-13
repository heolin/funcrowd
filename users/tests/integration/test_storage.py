import pytest
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from users.api.views.storage import EndWorkerStorageView, EndWorkerStorageBatchView


@pytest.mark.django_db
def test_storage_view(setup_user):
    factory = APIRequestFactory()

    request = factory.get('/api/v1/users/storage/test')
    force_authenticate(request, user=setup_user)
    view = EndWorkerStorageView.as_view()
    response = view(request, 'test')
    assert response.status_code == 200
    assert response.data['key'] == 'test'
    assert response.data['data'] == {}

    payload = {
        "data": {"test": 1}
    }
    request = factory.post('/api/v1/users/storage/test', payload, format="json")
    force_authenticate(request, user=setup_user)
    view = EndWorkerStorageView.as_view()
    response = view(request, 'test')
    assert response.status_code == 200
    assert response.data['key'] == 'test'
    assert response.data['data'] == {"test": 1}

    request = factory.get('/api/v1/users/storage/test')
    force_authenticate(request, user=setup_user)
    view = EndWorkerStorageView.as_view()
    response = view(request, 'test')
    assert response.status_code == 200
    assert response.data['key'] == 'test'
    assert response.data['data'] == {"test": 1}


@pytest.mark.django_db
def test_storage_view(setup_user, setup_storage_data):
    factory = APIRequestFactory()

    request = factory.get('/api/v1/users/storage')
    force_authenticate(request, user=setup_user)
    view = EndWorkerStorageBatchView.as_view()
    response = view(request)
    assert len(response.data) == 2
    assert response.data[0]['key'] == 'test2'
    assert response.data[1]['key'] == 'test1'

    payload = [
        {'key': 'test1', "data": "value"},
        {'key': 'test3', "data": "value"}
    ]
    request = factory.post('/api/v1/users/storage', payload, format="json")
    force_authenticate(request, user=setup_user)
    view = EndWorkerStorageBatchView.as_view()
    response = view(request)
    assert len(response.data) == 3
    assert response.data[0]['key'] == 'test3'
    assert response.data[1]['key'] == 'test2'
    assert response.data[2]['key'] == 'test1'
