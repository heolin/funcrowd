import pytest

from tasks.models import (
    Mission, Task, Item, ItemTemplate, ItemTemplateField, Annotation
)
from users.models import EndWorker

from modules.order_strategy.models import Strategy


@pytest.fixture
@pytest.mark.django_db
def setup_user():
    user = EndWorker.objects.create_superuser("user", "user@mail.com", "password")
    return user


@pytest.fixture
@pytest.mark.django_db
def setup_other_user():
    user = EndWorker.objects.create_superuser("other_user", "other_user@mail.com", "password")
    return user


@pytest.fixture
@pytest.mark.django_db
def setup_task():
    Strategy.register_values()

    mission = Mission.objects.create(id=1, name="Test mission")
    strategy = Strategy.objects.get(name="StaticStrategyLogic")
    Task.objects.create(id=1, mission=mission, name="Add two digits", strategy=strategy)

    Mission.objects.create(id=2, name="Test mission other")


@pytest.fixture
@pytest.mark.django_db
def setup_task_with_items():
    Strategy.register_values()

    mission = Mission.objects.create(id=1, name="Test mission")
    strategy = Strategy.objects.get(name="StaticStrategyLogic")
    task = Task.objects.create(id=1, mission=mission, name="Add two digits", strategy=strategy)

    template = ItemTemplate.objects.create(name="Adding two")
    first_field = ItemTemplateField.objects.create(name="first", widget="TextLabel")
    template.fields.add(first_field)
    annotation_field = ItemTemplateField.objects.create(name="output", widget="TextLabel",
                                                        required=True, editable=True)
    template.fields.add(annotation_field)

    for i in range(10):
        Item.objects.create(task=task, template=template, order=i,
                            data={first_field.name: i})
