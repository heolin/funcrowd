import pytest

from tasks.models import (
    Mission, Task, Item, ItemTemplate, ItemTemplateField, Annotation
)
from users.models import EndWorker

from modules.order_strategy.models import Strategy


@pytest.fixture
@pytest.mark.django_db
def user1():
    user = EndWorker.objects.create_superuser("user1@mail.com", "password", username="user1")
    return user


@pytest.fixture
@pytest.mark.django_db
def user2():
    user = EndWorker.objects.create_superuser("user2@mail.com", "password", username="user2")
    return user


@pytest.fixture
def setup_storage_data(setup_user):
    setup_user.set_storage("test1", {"test": 1})
    setup_user.set_storage("test2", {"test": 1})
