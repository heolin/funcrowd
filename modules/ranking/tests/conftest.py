import pytest

from modules.packages.models import MissionPackages, Package
from tasks.models import (
    Mission, Task, Item, ItemTemplate, ItemTemplateField, Annotation
)
from users.models import EndWorker

from modules.order_strategy.models import Strategy


@pytest.fixture
@pytest.mark.django_db
def users():
    return [
        EndWorker.objects.create_user("user1@mail.com", "password", exp=1, username="user1"),
        EndWorker.objects.create_user("user2@mail.com", "password", exp=2, username="user2"),
        EndWorker.objects.create_user("user3@mail.com", "password", exp=3, username="user3"),
        EndWorker.objects.create_user("user@4mail.com", "password", exp=4, username="user4"),
    ]



@pytest.fixture
@pytest.mark.django_db
def task_annotations(users):
    user1, user2, user3, user4 = users
    Strategy.register_values()

    mission = Mission.objects.create(id=1, name="Test mission")
    strategy = Strategy.objects.get(name="StaticStrategyLogic")
    task = Task.objects.create(id=1, mission=mission, name="Add two digits", strategy=strategy)

    template = ItemTemplate.objects.create(name="Adding two")

    item1 = Item.objects.create(task=task, template=template, data={})
    item2 = Item.objects.create(task=task, template=template, data={})
    item3 = Item.objects.create(task=task, template=template, data={})

    mp = MissionPackages.objects.create(mission=mission, strategy=strategy)
    package1 = Package.objects.create(parent=mp, order=0)
    package1.items.add(item1)
    package1.items.add(item2)
    package1.save()

    package2 = Package.objects.create(parent=mp, order=1)
    package2.items.add(item3)
    package2.save()

    Annotation.objects.create(user=user4, item=item1, data={}, annotated=True)
    Annotation.objects.create(user=user4, item=item2, data={}, annotated=True)
    Annotation.objects.create(user=user4, item=item3, data={}, annotated=True)

    Annotation.objects.create(user=user3, item=item1, data={}, annotated=True)
    Annotation.objects.create(user=user3, item=item2, data={}, annotated=True)

    Annotation.objects.create(user=user2, item=item1, data={}, annotated=True)

    for user in users:
        stats = user.get_mission_stats(mission.id)
        stats.update()
