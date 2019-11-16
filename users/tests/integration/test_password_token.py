import pytest
from unittest.mock import MagicMock

import funcrowd.settings as settings

from rest_framework.test import APIRequestFactory
from django.test import Client

from modules.communication.email import EmailHelper
from users.models import ActivationToken, PasswordToken


@pytest.mark.django_db
def test_end_worker_reset_password(user1):
    EmailHelper.send_reset_password_email = MagicMock()

    user1.set_password('password')
    user1.save()

    client = Client()

    # reset password - empty payload
    response = client.post('/api/v1/users/reset_password', {})
    assert response.status_code == 400

    # reset password - wrong email
    payload = {
        'email': "beolin@gmail.com"
    }
    response = client.post('/api/v1/users/reset_password', payload)
    assert response.status_code == 404

    # reset password - correct email
    payload = {
        'email': user1.email
    }
    response = client.post('/api/v1/users/reset_password', payload)
    assert response.status_code == 204

    # check if email was sent
    token = PasswordToken.objects.get(user=user1)
    EmailHelper.send_reset_password_email.assert_called_once_with(user1, token)

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
        "email": "user1@mail.com",
        "password": "password",
    }

    response = client.post('/api/v1/users/login', payload)
    assert response.status_code == 403

    # login success
    payload = {
        "email": "user1@mail.com",
        "password": "password1",
    }

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
