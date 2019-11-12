import pytest
from unittest.mock import MagicMock

import funcrowd.settings as settings

from rest_framework.test import APIRequestFactory
from django.test import Client

from modules.communication.email import EmailHelper
from users.models import ActivationToken, PasswordToken


@pytest.mark.django_db
def test_end_worker_reset_password(setup_user):
    EmailHelper.send_reset_password_email = MagicMock()

    user = setup_user
    user.set_password('password')
    user.save()

    client = Client()

    # reset password - unauthorized
    response = client.post('/api/v1/users/reset_password', {})
    assert response.status_code == 401

    client.login(username='user', password='password')

    # reset password - authorized
    response = client.post('/api/v1/users/reset_password', {})
    assert response.status_code == 204

    # check if email was sent
    token = PasswordToken.objects.get(user=user)
    EmailHelper.send_reset_password_email.assert_called_once_with(user, token)

    # reset password with a wrong token
    payload = {
        "token": "wrongtoken",
        "password1": "password1",
        "password2": "password1",
    }

    response = client.post('/api/v1/users/reset_password/token', payload)
    assert response.status_code == 400
    assert response.data['detail'].code == "password_token_wrong"

    # reset password with a correct token
    payload = {
        "token": token.token,
        "password1": "password1",
        "password2": "password1",
    }

    response = client.post('/api/v1/users/reset_password/token', payload)
    assert response.status_code == 204

    # login with old password
    payload = {
        "username": "user",
        "password": "password",
    }
    client = Client()
    response = client.post('/api/v1/users/login', payload)
    assert response.status_code == 403

    # login success
    payload = {
        "username": "user",
        "password": "password1",
    }
    client = Client()
    response = client.post('/api/v1/users/login', payload)
    assert response.status_code == 200

    # reset password with an old token
    payload = {
        "token": token.token,
        "password1": "password1",
        "password2": "password1",
    }

    response = client.post('/api/v1/users/reset_password/token', payload)
    assert response.status_code == 400
    assert response.data['detail'].code == "password_token_used"
