import pytest

from tasks.consts import IN_PROGRESS, VERIFICATION, FINISHED
from tasks.models import (
    Mission, Task, Item, ItemTemplate, ItemTemplateField, Annotation,
    Document)
from users.models import EndWorker

from modules.order_strategy.models import Strategy


def add_annotation(item, user, value):
    return Annotation.objects.create(item=item, user=user,
                                     data={"output": value})


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
def setup_tasks():
    Strategy.register_values()
    strategy = Strategy.objects.get(name="StaticStrategyLogic")

    mission1 = Mission.objects.create(name="Test mission 1")
    mission2 = Mission.objects.create(name="Test mission 2")
    mission3 = Mission.objects.create(name="Test mission 2")

    Task.objects.create(mission=mission1, name="Task 1", strategy=strategy)
    Task.objects.create(mission=mission1, name="Task 2", strategy=strategy)
    Task.objects.create(mission=mission1, name="Task 3", strategy=strategy)

    Task.objects.create(mission=mission2, name="Task 4", strategy=strategy)
    Task.objects.create(mission=mission2, name="Task 5", strategy=strategy)

    Task.objects.create(mission=mission3, name="Task 6", strategy=strategy)

    Document.objects.create(name="Document 1", mission=mission1)
    Document.objects.create(name="Document 2", mission=mission1)
    Document.objects.create(name="Document 3", mission=mission1, status=IN_PROGRESS)
    Document.objects.create(name="Document 4", mission=mission1, status=VERIFICATION)
    Document.objects.create(name="Document 5", mission=mission1, status=FINISHED)
    Document.objects.create(name="Document 6", mission=mission1, status=FINISHED)

    Document.objects.create(name="Document 7", mission=mission2)
    Document.objects.create(name="Document 8", mission=mission2)
    Document.objects.create(name="Document 9", mission=mission2)
    Document.objects.create(name="Document 10", mission=mission2, status=IN_PROGRESS)

    Document.objects.create(name="Document 11", mission=mission3, status=VERIFICATION)
    Document.objects.create(name="Document 12", mission=mission3, status=FINISHED)
    Document.objects.create(name="Document 13", mission=mission3, status=FINISHED)


@pytest.fixture
@pytest.mark.django_db
def setup_tasks_items(setup_tasks):
    task1 = Task.objects.get(name="Task 1")
    task4 = Task.objects.get(name="Task 4")

    template = ItemTemplate.objects.create(name="Test template")
    first_field = ItemTemplateField.objects.create(name="first", widget="TextLabel")
    template.fields.add(first_field)
    annotation_field = ItemTemplateField.objects.create(name="output", widget="TextLabel",
                                                        required=True, editable=True)
    template.fields.add(annotation_field)

    for i in range(10):
        Item.objects.create(task=task1, template=template, order=i,
                            data={first_field.name: i})

        Item.objects.create(task=task4, template=template, order=i,
                            data={first_field.name: i})


@pytest.fixture
@pytest.mark.django_db
def setup_tasks_annotations(setup_user, setup_other_user, setup_tasks_items):

    user1, user2 = setup_user, setup_other_user

    task1 = Task.objects.get(name="Task 1")
    for item in task1.items.all():
        add_annotation(item, user1, "1")
        add_annotation(item, user2, "1")

    task2 = Task.objects.get(name="Task 1")
    for item in task2.items.all():
        add_annotation(item, user1, "1")
