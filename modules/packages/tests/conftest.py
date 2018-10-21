import pytest

from tasks.models import (
    Mission, Task, Item, ItemTemplate, ItemTemplateField, Annotation
)
from users.models import EndWorker

from modules.packages.models import Package
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
def setup_task_with_items():
    Strategy.register_values()

    mission = Mission.objects.create(id=1, name="Test mission")
    strategy = Strategy.objects.get(name="StaticStrategyLogic")

    template = ItemTemplate.objects.create(name="task1")
    field = ItemTemplateField.objects.create(name="value", widget="TextLabel")
    template.fields.add(field)
    annotation_field = ItemTemplateField.objects.create(name="output", widget="TextLabel")
    template.fields.add(annotation_field)

    task1 = Task.objects.create(mission=mission, name="task1", strategy=strategy)
    task1_item1 = Item.objects.create(task=task1, template=template, order=1,
                        data={field.name: "task1 item1"})
    task1_item2 = Item.objects.create(task=task1, template=template, order=2,
                        data={field.name: "task1 item2"})

    task2 = Task.objects.create(mission=mission, name="task2", strategy=strategy)
    task2_item1 = Item.objects.create(task=task2, template=template, order=1,
                        data={field.name: "task2 item1"})
    task2_item2 = Item.objects.create(task=task2, template=template, order=2,
                        data={field.name: "task2 item2"})

    package = Package.objects.create(mission=mission, order=1)
    package.items.add(task1_item1)
    package.items.add(task2_item1)

    package = Package.objects.create(mission=mission, order=2)
    package.items.add(task1_item2)
    package.items.add(task2_item2)
