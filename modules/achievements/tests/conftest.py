import pytest

from modules.achievements.models import ItemDoneAchievement, LoginCountAchievement
from modules.achievements.models.progress import ProgressAchievement
from tasks.consts import MissionStatus
from tasks.models import (
    Mission, Task, Item, ItemTemplate, ItemTemplateField
)
from users.consts import ProfileType
from users.models import EndWorker

from modules.order_strategy.models import Strategy


@pytest.fixture
@pytest.mark.django_db
def user1():
    user = EndWorker.objects.create_superuser("user1@mail.com", "password", username="user1")
    user.profile = ProfileType.NORMAL
    user.save()
    return user


@pytest.fixture
@pytest.mark.django_db
def user2():
    user = EndWorker.objects.create_superuser("user2@mail.com", "password", username="user2")
    user.profile = ProfileType.NORMAL
    user.save()
    return user


@pytest.fixture
@pytest.mark.django_db
def task_with_items():
    Strategy.register_values()

    mission = Mission.objects.create(id=1, name="Test mission")
    strategy = Strategy.objects.get(name="StaticStrategyLogic")

    task = Task.objects.create(id=1, mission=mission, name="Test", strategy=strategy)

    template = ItemTemplate.objects.create(name="Template")
    input_field = ItemTemplateField.objects.create(name="input", widget="TextLabel")
    template.fields.add(input_field)
    annotation_field = ItemTemplateField.objects.create(name="output", widget="TextLabel",
                                                        required=True, editable=True)
    template.fields.add(annotation_field)

    Item.objects.create(task=task, template=template, order=1,
                        data={input_field.name: 1})
    Item.objects.create(task=task, template=template, order=2,
                        data={input_field.name: 2})

    task = Task.objects.create(id=2, mission=mission, name="Test", strategy=strategy)
    Item.objects.create(task=task, template=template, order=1,
                        data={input_field.name: 1})


@pytest.fixture
@pytest.mark.django_db
def missions_with_tasks():
    Strategy.register_values()
    strategy = Strategy.objects.get(name="StaticStrategyLogic")

    mission1 = Mission.objects.create(name="Test mission")
    Task.objects.create(mission=mission1, name="Test", strategy=strategy)
    Task.objects.create(mission=mission1, name="Test", strategy=strategy)

    mission2 = Mission.objects.create(name="Test mission")
    Task.objects.create(mission=mission2, name="Test", strategy=strategy)
    Task.objects.create(mission=mission2, name="Test", strategy=strategy)


@pytest.fixture
@pytest.mark.django_db
def hidden_mission(task_with_items):
    mission = Mission.objects.create(id=2, name="Other mission")
    mission.parent = mission
    mission.save()
    return mission


@pytest.fixture
@pytest.mark.django_db
def achievements(task_with_items):
    ItemDoneAchievement.objects.create(order=1, exp=10)
    ItemDoneAchievement.objects.create(order=2, mission_id=1, target=2, exp=10)
    ItemDoneAchievement.objects.create(order=3, task_id=2, exp=10)
    ProgressAchievement.objects.create(order=5, task_id=1, exp=0)
    ProgressAchievement.objects.create(order=6, mission_id=1, exp=10)
    LoginCountAchievement.objects.create(order=0, exp=10)


def compare_without_fields(dict1, dict2, excluded_fields=['id']):
    dict1 = {k: v for (k, v) in dict1.items() if k not in excluded_fields}
    dict2 = {k: v for (k, v) in dict2.items() if k not in excluded_fields}
    return dict1 == dict2
