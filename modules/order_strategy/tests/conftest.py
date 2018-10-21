import pytest

from tasks.models import (
    Mission, Task, Item, ItemTemplate, ItemTemplateField, Annotation
)

from users.models import EndWorker
from modules.order_strategy.models import Strategy
from django.core.management import call_command


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'initial_data')


@pytest.fixture
@pytest.mark.django_db
def setup_db_random():
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute('''SELECT setseed(0)''')


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
    #Strategy.register_values()

    mission = Mission.objects.create(id=1, name="Test mission")
    strategy = Strategy.objects.get(name="StaticStrategyLogic")
    task = Task.objects.create(id=1, mission=mission, name="Add two digits", strategy=strategy)

    template = ItemTemplate.objects.create(name="Adding two")
    first_field = ItemTemplateField.objects.create(name="first", widget="TextLabel")
    template.fields.add(first_field)
    annotation_field = ItemTemplateField.objects.create(name="output", widget="TextLabel",
                                                        required=True, editable=True)
    template.fields.add(annotation_field)

    Item.objects.create(task=task, template=template, data={first_field.name: 1}, order=0)
    Item.objects.create(task=task, template=template, data={first_field.name: 2}, order=1)
    Item.objects.create(task=task, template=template, data={first_field.name: 3}, order=2)


@pytest.fixture
@pytest.mark.django_db
def setup_task_with_annotations(setup_other_user):
    user = setup_other_user
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

    item = Item.objects.create(task=task, template=template, data={first_field.name: 1}, order=0)
    annotation, _ = item.get_or_create_annotation(user)
    annotation.data[annotation_field.name] = 1
    annotation.save()

    Item.objects.create(task=task, template=template, data={first_field.name: 2}, order=1)
    Item.objects.create(task=task, template=template, data={first_field.name: 3}, order=2)