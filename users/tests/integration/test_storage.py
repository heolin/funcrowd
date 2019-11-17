import pytest
import json
from django.test import Client


@pytest.mark.django_db
def test_storage_view(user1):
    client = Client()
    client.force_login(user1)

    response = client.get('/api/v1/users/storage/test/')
    assert response.status_code == 200
    assert response.data['key'] == 'test'
    assert response.data['data'] == {}

    payload = {
        "data": {"test": 1}
    }
    response = client.post('/api/v1/users/storage/test/',
                           json.dumps(payload), content_type='application/json')
    assert response.status_code == 200
    assert response.data['key'] == 'test'
    assert response.data['data'] == {"test": 1}

    response = client.get('/api/v1/users/storage/test/')
    assert response.status_code == 200
    assert response.data['key'] == 'test'
    assert response.data['data'] == {"test": 1}


@pytest.mark.django_db
def test_storage_view_with_existing_data(user1, setup_storage_data):
    client = Client()
    client.force_login(user1)

    response = client.get('/api/v1/users/storage/')
    assert len(response.data) == 2
    assert response.data[0]['key'] == 'test2'
    assert response.data[1]['key'] == 'test1'

    payload = [
        {'key': 'test1', "data": "value"},
        {'key': 'test3', "data": "value"}
    ]
    response = client.post('/api/v1/users/storage/',
                           json.dumps(payload), content_type='application/json')
    assert len(response.data) == 3
    assert response.data[0]['key'] == 'test3'
    assert response.data[1]['key'] == 'test2'
    assert response.data[2]['key'] == 'test1'
