import pytest

from tasks.field_types import LIST
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
    second_field = ItemTemplateField.objects.create(name="second", widget="TextLabel")
    template.fields.add(second_field)
    annotation_field = ItemTemplateField.objects.create(name="output", widget="TextLabel",
                                                        required=True, editable=True)
    template.fields.add(annotation_field)
    optional_annotation_field = ItemTemplateField.objects.create(name="optional", widget="TextLabel",
                                                                 required=False, editable=True)

    template.fields.add(optional_annotation_field)

    Item.objects.create(task=task, template=template, order=1,
                        data={first_field.name: 1, second_field.name: 2})
    Item.objects.create(task=task, template=template, order=2,
                        data={first_field.name: 2, second_field.name: 2})


@pytest.fixture
@pytest.mark.django_db
def setup_task_with_items_data_source():
    Strategy.register_values()

    mission = Mission.objects.create(id=1, name="Test mission")
    strategy = Strategy.objects.get(name="StaticStrategyLogic")
    task = Task.objects.create(id=1, mission=mission, name="Add two digits", strategy=strategy)

    template = ItemTemplate.objects.create(name="Adding two")
    first_field = ItemTemplateField.objects.create(name="first", widget="TextLabel")
    template.fields.add(first_field)
    source_field = ItemTemplateField.objects.create(name="ALL_VALUES", widget="Hidden")
    template.fields.add(source_field)
    annotation_field = ItemTemplateField.objects.create(name="output", widget="TextLabel",
                                                        required=True, editable=True,
                                                        data_source=source_field)
    template.fields.add(annotation_field)

    Item.objects.create(task=task, template=template, order=1,
                        data={first_field.name: 1, source_field.name: ["A", "B"]})


@pytest.fixture
@pytest.mark.django_db
def setup_task_with_items_data_source_type_list():
    Strategy.register_values()

    mission = Mission.objects.create(id=1, name="Test mission")
    strategy = Strategy.objects.get(name="StaticStrategyLogic")
    task = Task.objects.create(id=1, mission=mission, name="Add two digits", strategy=strategy)

    template = ItemTemplate.objects.create(name="Adding two")
    first_field = ItemTemplateField.objects.create(name="first", widget="TextLabel")
    template.fields.add(first_field)
    source_field = ItemTemplateField.objects.create(name="ALL_VALUES", widget="Hidden")
    template.fields.add(source_field)
    annotation_field = ItemTemplateField.objects.create(name="output", widget="TextLabel",
                                                        required=True, editable=True, type=LIST,
                                                        data_source=source_field)
    template.fields.add(annotation_field)

    Item.objects.create(task=task, template=template, order=1,
                        data={first_field.name: 1, source_field.name: ["A", "B"]})
