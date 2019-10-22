import pytest

from tasks.models import (
    Mission, Task, Item, ItemTemplate, ItemTemplateField, Annotation
)
from users.models import EndWorker

from modules.order_strategy.models import Strategy


@pytest.fixture
@pytest.mark.django_db
def setup_users():
    return [
        EndWorker.objects.create(username="user1", email="user@mail.com", password="password", exp=10),
        EndWorker.objects.create(username="user2", email="user@mail.com", password="password", exp=20),
        EndWorker.objects.create(username="user3", email="user@mail.com", password="password", exp=30),
        EndWorker.objects.create(username="user4", email="user@mail.com", password="password", exp=40),
    ]



@pytest.fixture
@pytest.mark.django_db
def setup_task_annotations(setup_users):
    user1, user2, user3, user4 = setup_users
    Strategy.register_values()

    mission = Mission.objects.create(id=1, name="Test mission")
    strategy = Strategy.objects.get(name="StaticStrategyLogic")
    task = Task.objects.create(id=1, mission=mission, name="Add two digits", strategy=strategy)

    template = ItemTemplate.objects.create(name="Adding two")

    item1 = Item.objects.create(task=task, template=template, data={})
    item2 = Item.objects.create(task=task, template=template, data={})
    item3 = Item.objects.create(task=task, template=template, data={})

    Annotation.objects.create(user=user4, item=item1, data={}, annotated=True)
    Annotation.objects.create(user=user4, item=item2, data={}, annotated=True)
    Annotation.objects.create(user=user4, item=item3, data={}, annotated=True)

    Annotation.objects.create(user=user3, item=item1, data={}, annotated=True)
    Annotation.objects.create(user=user3, item=item2, data={}, annotated=True)

    Annotation.objects.create(user=user2, item=item1, data={}, annotated=True)
