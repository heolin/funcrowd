import pytest

import funcrowd.settings as settings
from django.test import Client

from users.models.end_workers import EndWorker


@pytest.mark.django_db
def test_end_worker_view(user1, user2):
    # get user1 stats
    client = Client()
    client.force_login(user1)
    response = client.get('/api/v1/users/current/')
    assert response.status_code == 200
    assert response.data['id'] == user1.id
    assert response.data['username'] == user1.username
    assert response.data['token'] == str(user1.token)
    assert response.data['exp'] == 0

    # get user2 stats
    client.force_login(user2)
    response = client.get('/api/v1/users/current/')
    assert response.status_code == 200
    assert response.data['id'] == user2.id
    assert response.data['username'] == user2.username
    assert response.data['token'] == str(user2.token)


@pytest.mark.django_db
def test_end_worker_registration_not_verification():
    settings.ACCOUNT_EMAIL_VERIFICATION = False

    client = Client()

    # register new user
    payload = {
        "username": "newuser1",
        "password1": "password1",
        "password2": "password1",
        'email': 'newuser1@mail.com'
    }
    response = client.post('/api/v1/users/register/', payload)
    end_worker = EndWorker.objects.last()
    assert response.status_code == 201
    assert end_worker.username == "newuser1"
    assert end_worker.email == "newuser1@mail.com"
    assert response.data['id'] == end_worker.id
    assert response.data['username'] == end_worker.username
    assert response.data['token'] == str(end_worker.token)
    assert response.data['email'] == "newuser1@mail.com"
    assert response.data['is_active'] is True

    # register other user
    payload = {
        "username": "newuser2",
        "password1": "password1",
        "password2": "password1",
        'email': 'newuser2@mail.com'
    }
    response = client.post('/api/v1/users/register/', payload)
    end_worker = EndWorker.objects.last()
    assert response.status_code == 201
    assert end_worker.username == "newuser2"
    assert response.data['id'] == end_worker.id
    assert response.data['username'] == end_worker.username
    assert response.data['token'] == str(end_worker.token)
    assert response.data['email'] == end_worker.email

    # register user already used
    payload = {
        "username": "newuser1",
        "password1": "password1",
        "password2": "password1",
        'email': 'newuser3@mail.com'
    }
    response = client.post('/api/v1/users/register/', payload)

    assert response.data['detail'].code == "username_used"
    assert response.status_code == 400

    # register - email already used
    payload = {
        "username": "newuser4",
        "password1": "password1",
        "password2": "password1",
        'email': 'newuser1@mail.com'
    }
    response = client.post('/api/v1/users/register/', payload)

    assert response.data['detail'].code == "email_used"
    assert response.status_code == 400

    # register passwords not match
    payload = {
        "username": "newuser5",
        "password1": "password1",
        "password2": "password2",
        'email': 'newuser5@mail.com'
    }
    response = client.post('/api/v1/users/register/', payload)
    assert response.data['detail'].code == "password_not_match"
    assert response.status_code == 400


@pytest.mark.django_db
def test_end_worker_login(user1):
    user1.set_password("password")

    # login wrong password
    payload = {
        "email": "user1@mail.com",
        "password": "wrong_password",
    }

    client = Client()
    response = client.post('/api/v1/users/login/', payload)
    assert response.data['detail'].code == "not_authenticated"
    assert response.status_code == 403

    # login success
    payload = {
        "email": "user1@mail.com",
        "password": "password",
    }
    response = client.post('/api/v1/users/login/', payload)
    assert response.status_code == 200

    # get data of current user
    response = client.get('/api/v1/users/current/')
    end_worker = EndWorker.objects.last()
    assert response.status_code == 200
    assert end_worker.username == "user1"
    assert response.data['id'] == end_worker.id
    assert response.data['username'] == end_worker.username
    assert response.data['token'] == str(end_worker.token)


@pytest.mark.django_db
def test_end_worker_logout(user1):
    client = Client()

    # login success
    payload = {
        "email": "user1@mail.com",
        "password": "password",
    }
    response = client.post('/api/v1/users/login/', payload)
    assert response.status_code == 200

    # get data of current user
    response = client.get('/api/v1/users/current/')
    end_worker = EndWorker.objects.last()
    assert response.status_code == 200
    assert response.data['username'] == end_worker.username
    assert end_worker.username == "user1"

    client.get('/api/v1/users/logout/')

    # get data of current user
    response = client.get('/api/v1/users/current/')
    assert response.status_code == 401


@pytest.mark.django_db
def test_end_worker_status_view(user1):
    client = Client()
    client.force_login(user1)

    # get user1 stats
    response = client.get('/api/v1/users/status/')
    assert response.status_code == 200
    assert response.data['id'] == user1.id
    assert response.data['username'] == user1.username
    assert response.data['exp'] == 0
