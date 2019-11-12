from unittest.mock import MagicMock
import pytest
from django.test import Client


@pytest.mark.django_db
def test_end_worker_change_password(setup_user):
    # login success
    payload = {
        "username": "user",
        "password": "password",
    }
    client = Client()
    response = client.post('/api/v1/users/login', payload)
    assert response.status_code == 200

    # change password - old password wrong
    payload = {
        "old_password": "wrong",
        "new_password1": "password1",
        "new_password2": "password1",
    }
    response = client.post('/api/v1/users/change_password', payload)
    assert response.status_code == 401
    assert response.data['detail'].code == "not_authenticated"

    # change password - new passwords don't match
    payload = {
        "old_password": "password",
        "new_password1": "password1",
        "new_password2": "password2",
    }
    response = client.post('/api/v1/users/change_password', payload)
    assert response.status_code == 400
    assert response.data['detail'].code == "password_not_match"

    # change password - success
    payload = {
        "old_password": "password",
        "new_password1": "password1",
        "new_password2": "password1",
    }
    response = client.post('/api/v1/users/change_password', payload)
    assert response.status_code == 204

    # login with new password
    payload = {
        "username": "user",
        "password": "password1",
    }
    client = Client()
    response = client.post('/api/v1/users/login', payload)
    assert response.status_code == 200

    # login with old password
    payload = {
        "username": "user",
        "password": "password",
    }
    client = Client()
    response = client.post('/api/v1/users/login', payload)
    assert response.status_code == 403
