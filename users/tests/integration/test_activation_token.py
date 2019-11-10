import pytest
from unittest.mock import MagicMock

import funcrowd.settings as settings

from rest_framework.test import APIRequestFactory
from django.test import Client

from modules.communication.email import EmailHelper
from users.api.views.auth import (
    EndWorkerRegistrationView,
)
from users.models import ActivationToken
from users.models.end_workers import EndWorker



@pytest.mark.django_db
def test_end_worker_registration_verification():
    settings.ACCOUNT_EMAIL_VERIFICATION = True
    EmailHelper.send_activation_email = MagicMock()

    factory = APIRequestFactory()

    # register new user
    payload = {
        "username": "newuser",
        "password1": "password1",
        "password2": "password1",
    }
    request = factory.post('/api/v1/users/register', payload)
    view = EndWorkerRegistrationView.as_view()
    response = view(request)
    end_worker = EndWorker.objects.last()

    assert response.status_code == 201
    assert end_worker.username == "newuser"
    assert end_worker.email == ""
    assert response.data['id'] == end_worker.id
    assert response.data['username'] == end_worker.username
    assert response.data['token'] == str(end_worker.token)
    assert response.data['email'] == ""
    assert response.data['is_active'] == end_worker.is_active
    assert response.data['is_active'] is False

    token = ActivationToken.objects.get(user=end_worker)

    # check if email was sent
    EmailHelper.send_activation_email.assert_called_once_with(end_worker, token)

    # login not active
    payload = {
        "username": "newuser",
        "password": "password1",
    }

    client = Client()
    response = client.post('/api/v1/users/login', payload)
    assert response.status_code == 401
    assert response.data['detail'].code == "account_not_active"

    # activate token
    #
    payload = {
        "token": token.token
    }
    response = client.post('/api/v1/users/activate', payload)
    assert response.status_code == 204

    token = ActivationToken.objects.get(user=end_worker)
    assert token.token_used

    # login success
    payload = {
        "username": "newuser",
        "password": "password1",
    }
    client = Client()
    response = client.post('/api/v1/users/login', payload)
    assert response.status_code == 200


@pytest.mark.django_db
def test_multiple_tokens():
    settings.ACCOUNT_EMAIL_VERIFICATION = True
    EmailHelper.send_activation_email = MagicMock()

    factory = APIRequestFactory()

    # register new user
    payload = {
        "username": "newuser",
        "password1": "password1",
        "password2": "password1",
    }
    request = factory.post('/api/v1/users/register', payload)
    view = EndWorkerRegistrationView.as_view()
    view(request)
    end_worker = EndWorker.objects.last()

    client = Client()

    # activate wrong token
    token = ActivationToken.objects.get(user=end_worker)
    payload = {
        "token": "TEST"
    }
    response = client.post('/api/v1/users/activate', payload)
    assert response.status_code == 400
    assert response.data['detail'].code == "activation_token_wrong"

    # activate correct token
    payload = {
        "token": token.token
    }
    response = client.post('/api/v1/users/activate', payload)
    assert response.status_code == 204

    # activate used token
    payload = {
        "token": token.token
    }
    response = client.post('/api/v1/users/activate', payload)
    assert response.status_code == 400
    assert response.data['detail'].code == "activation_token_used"
