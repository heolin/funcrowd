from unittest.mock import MagicMock

import pytest
from django.contrib.auth import authenticate

import funcrowd.settings as settings

from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from django.test import Client

from modules.communication.email import EmailHelper
from users.api.views.auth import (
    EndWorkerView,
    EndWorkerRegistrationView,
    EndWorkerStatusView
)
from users.models.end_workers import EndWorker


@pytest.mark.django_db
def test_end_worker_view(setup_user, setup_other_user):
    factory = APIRequestFactory()

    # get user1 stats
    request = factory.get('/api/v1/users/current')
    force_authenticate(request, user=setup_user)
    view = EndWorkerView.as_view()
    response = view(request)
    assert response.status_code == 200
    assert response.data['id'] == setup_user.id
    assert response.data['username'] == setup_user.username
    assert response.data['token'] == str(setup_user.token)
    assert response.data['exp'] == 0

    # get user2 stats
    request = factory.get('/api/v1/users/current')
    force_authenticate(request, user=setup_other_user)
    view = EndWorkerView.as_view()
    response = view(request)
    assert response.status_code == 200
    assert response.data['id'] == setup_other_user.id
    assert response.data['username'] == setup_other_user.username
    assert response.data['token'] == str(setup_other_user.token)


@pytest.mark.django_db
def test_end_worker_registration_not_verification():
    settings.ACCOUNT_EMAIL_VERIFICATION = False
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
    assert response.data['is_active'] is True

    # register new user
    payload = {
        "username": "newuser2",
        "password1": "password1",
        "password2": "password1",
        'email': 'emil@com.sam'
    }
    request = factory.post('/api/v1/users/register', payload)
    view = EndWorkerRegistrationView.as_view()
    response = view(request)
    end_worker = EndWorker.objects.last()
    assert response.status_code == 201
    assert end_worker.username == "newuser2"
    assert response.data['id'] == end_worker.id
    assert response.data['username'] == end_worker.username
    assert response.data['token'] == str(end_worker.token)
    assert response.data['email'] == end_worker.email

    # register user already used
    payload = {
        "username": "newuser",
        "password1": "password1",
        "password2": "password2",
    }
    request = factory.post('/api/v1/users/register', payload)
    view = EndWorkerRegistrationView.as_view()
    response = view(request)

    assert response.data['detail'].code == "username_used"
    assert response.status_code == 400

    # register passwords not match
    payload = {
        "username": "newuser1",
        "password1": "password1",
        "password2": "password2",
    }
    request = factory.post('/api/v1/users/register', payload)
    view = EndWorkerRegistrationView.as_view()
    response = view(request)
    assert response.data['detail'].code == "password_not_match"
    assert response.status_code == 400


@pytest.mark.django_db
def test_end_worker_login(setup_user):
    # login wrong password
    payload = {
        "username": "user",
        "password": "wrong_password",
    }

    client = Client()
    response = client.post('/api/v1/users/login', payload)
    print(response.data)
    assert response.data['detail'].code == "not_authenticated"
    assert response.status_code == 403

    # login success
    payload = {
        "username": "user",
        "password": "password",
    }
    response = client.post('/api/v1/users/login', payload)
    assert response.status_code == 200

    # get data of current user
    response = client.get('/api/v1/users/current')
    end_worker = EndWorker.objects.last()
    assert response.status_code == 200
    assert end_worker.username == "user"
    assert response.data['id'] == end_worker.id
    assert response.data['username'] == end_worker.username
    assert response.data['token'] == str(end_worker.token)


@pytest.mark.django_db
def test_end_worker_logout(setup_user):
    # login success
    payload = {
        "username": "user",
        "password": "password",
    }
    client = Client()
    response = client.post('/api/v1/users/login', payload)
    assert response.status_code == 200

    # get data of current user
    response = client.get('/api/v1/users/current')
    end_worker = EndWorker.objects.last()
    assert response.status_code == 200
    assert response.data['username'] == end_worker.username
    assert end_worker.username == "user"

    client.get('/api/v1/users/logout')

    # get data of current user
    response = client.get('/api/v1/users/current')
    assert response.status_code == 401


@pytest.mark.django_db
def test_end_worker_status_view(setup_user):
    factory = APIRequestFactory()

    # get user1 stats
    request = factory.get('/api/v1/users/status')
    force_authenticate(request, user=setup_user)
    view = EndWorkerStatusView.as_view()
    response = view(request)
    assert response.status_code == 200
    assert response.data['id'] == setup_user.id
    assert response.data['username'] == setup_user.username
    assert response.data['exp'] == 0
