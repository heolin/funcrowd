import pytest

from modules.achievements.models import ItemDoneAchievement, LoginCountAchievement
from modules.achievements.models.progress import ProgressAchievement
from tasks.models import (
    Mission, Task, Item, ItemTemplate, ItemTemplateField
)
from users.models import EndWorker

from modules.order_strategy.models import Strategy


@pytest.fixture
@pytest.mark.django_db
def setup_user1():
    return EndWorker.objects.create_superuser("user", "user@mail.com", "password")


@pytest.fixture
@pytest.mark.django_db
def setup_user2():
    return EndWorker.objects.create_superuser("other_user", "other_user@mail.com", "password")


@pytest.fixture
@pytest.mark.django_db
def setup_task_with_items():
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
def setup_achievements(setup_task_with_items):
    ItemDoneAchievement.objects.create(order=1)
    ItemDoneAchievement.objects.create(order=2, mission_id=1, target=2)
    ItemDoneAchievement.objects.create(order=3, task_id=2)
    ProgressAchievement.objects.create(order=5, task_id=1)
    ProgressAchievement.objects.create(order=6, mission_id=1)
    LoginCountAchievement.objects.create(order=0)


@pytest.fixture
@pytest.mark.django_db
def setup_wrong_progress_achievement():
    ProgressAchievement.objects.create(order=4)


def compare_without_fields(dict1, dict2, excluded_fields=['id']):
    dict1 = {k: v for (k, v) in dict1.items() if k not in excluded_fields}
    dict2 = {k: v for (k, v) in dict2.items() if k not in excluded_fields}
    return dict1 == dict2
