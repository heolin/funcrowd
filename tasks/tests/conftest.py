import pytest

from tasks.models import (
    Mission, Task, Item, ItemTemplate, ItemTemplateField, Annotation
)

from modules.order_strategy.models import Strategy



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

    second_field = ItemTemplateField.objects.create(name="second", widget="TextLabel")
    template.fields.add(second_field)

    Item.objects.create(task=task, data={first_field.name: 1, second_field.name: 2}, template=template)
    Item.objects.create(task=task, data={first_field.name: 2, second_field.name: 2}, template=template)
