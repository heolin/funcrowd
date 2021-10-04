import pytest

from users.consts import ProfileType
from users.models import EndWorker

from .item_templates import *
from .scenarios import *


@pytest.fixture
@pytest.mark.django_db
def user1():
    user = EndWorker.objects.create_user("user1@mail.com", "password", username="user")
    return user


@pytest.fixture
@pytest.mark.django_db
def user2():
    user = EndWorker.objects.create_superuser("user2@mail.com", "password", username="user2")
    return user


@pytest.fixture
@pytest.mark.django_db
def user3():
    user = EndWorker.objects.create_superuser("user3@mail.com", "password", username="user3")
    return user


@pytest.fixture
@pytest.mark.django_db
def user4():
    user = EndWorker.objects.create_superuser("user4@mail.com", "password", username="user4")
    return user


@pytest.fixture
@pytest.mark.django_db
def mturk_user():
    user = EndWorker.objects.create_superuser(
        "user2@mail.com", "password", username="user2", profile=ProfileType.MTURK)
    return user


@pytest.fixture
@pytest.mark.django_db
def users():
    users = []
    for i in range(10):
        user = EndWorker.objects.create_superuser(
            f"user{i}@mail.com", "password", username=f"user{i}")
        users.append(user)
    return users


@pytest.fixture
@pytest.mark.django_db
def db_random():
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute('''SELECT setseed(0)''')
