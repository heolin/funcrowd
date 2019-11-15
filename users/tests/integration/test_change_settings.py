from unittest.mock import MagicMock
import pytest
from django.test import Client

from users.models import EndWorker


@pytest.mark.django_db
def test_end_worker_change_settings(setup_user, setup_other_user):
    user1, user2 = setup_user, setup_other_user
    client = Client()

    # login success
    payload = {
        "username": "user",
        "password": "password",
    }
    response = client.post('/api/v1/users/login', payload)
    assert response.status_code == 200

    # change username - already used
    payload = {
        "username": "other_user"
    }
    response = client.post('/api/v1/users/change_settings', payload)
    assert response.status_code == 400
    assert response.data['detail'].code == "username_used"

    # change username - same username
    payload = {
        "username": "user"
    }
    response = client.post('/api/v1/users/change_settings', payload)
    assert response.status_code == 204

    # change username - new username
    payload = {
        "username": "new"
    }
    response = client.post('/api/v1/users/change_settings', payload)
    assert response.status_code == 204

    user1 = EndWorker.objects.get(id=user1.id)
    assert user1.username == "new"
