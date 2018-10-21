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
def setup_task_one_variable():
    users = {}
    for i in range(14):
        users[i] = EndWorker.objects.create_user("user{}".format(i),
                                                 "user{}@mail.com".format(i),
                                                 "password")

    mission = Mission.objects.create(id=1, name="Test mission")
    strategy, _ = Strategy.objects.get_or_create(name="StaticStrategyLogic")
    task = Task.objects.create(id=1, mission=mission, name="Add two digits", strategy=strategy)

    template = ItemTemplate.objects.create(name="Test task")
    input_field = ItemTemplateField.objects.create(name="input", widget="TextLabel")
    template.fields.add(input_field)
    annotation_field = ItemTemplateField.objects.create(name="output", widget="TextLabel",
                                                        required=True, editable=True)
    template.fields.add(annotation_field)

    data = [[0, 0, 0, 0, 14],
            [0, 2, 6, 4, 2],
            [0, 0, 3, 5, 6],
            [0, 3, 9, 2, 0],
            [2, 2, 8, 1, 1],
            [7, 7, 0, 0, 0],
            [3, 2, 6, 3, 0],
            [2, 5, 3, 2, 2],
            [6, 5, 2, 1, 0],
            [0, 2, 2, 3, 7]]

    for i, row in enumerate(data):
        item = Item.objects.create(task=task, template=template,
                                   data={input_field.name: i}, order=i)
        counter = 0
        for j, count in enumerate(row):
            for _ in range(count):
                Annotation.objects.create(item=item,
                                          user=users[counter],
                                          data={annotation_field.name: j})
                counter += 1


@pytest.fixture
@pytest.mark.django_db
def setup_task_high_agreement():
    users = {}
    for i in range(14):
        users[i] = EndWorker.objects.create_user("user{}".format(i),
                                                 "user{}@mail.com".format(i),
                                                 "password")

    mission = Mission.objects.create(id=1, name="Test mission")
    strategy, _ = Strategy.objects.get_or_create(name="StaticStrategyLogic")
    task = Task.objects.create(id=1, mission=mission, name="Add two digits", strategy=strategy)

    template = ItemTemplate.objects.create(name="Test task")
    input_field = ItemTemplateField.objects.create(name="input", widget="TextLabel")
    template.fields.add(input_field)
    annotation_field = ItemTemplateField.objects.create(name="output", widget="TextLabel",
                                                        required=True, editable=True)
    template.fields.add(annotation_field)

    data = [[0, 0, 0, 0, 14],
            [0, 0, 0, 12, 2],
            [0, 0, 0, 5, 6],
            [0, 3, 9, 1, 0],
            [0, 0, 12, 1, 1],
            [12, 1, 0, 0, 0],
            [3, 10, 1, 0, 0],
            [14, 0, 0, 0, 0],
            [10, 0, 2, 1, 0],
            [0, 0, 13, 0, 1]]

    for i, row in enumerate(data):
        item = Item.objects.create(task=task, template=template,
                                   data={input_field.name: i}, order=i)
        counter = 0
        for j, count in enumerate(row):
            for _ in range(count):
                Annotation.objects.create(item=item,
                                          user=users[counter],
                                          data={annotation_field.name: j})
                counter += 1


@pytest.fixture
@pytest.mark.django_db
def setup_task_multiple_templates():
    mission = Mission.objects.create(id=1, name="Test mission")
    strategy, _ = Strategy.objects.get_or_create(name="StaticStrategyLogic")
    task = Task.objects.create(id=1, mission=mission, name="Add two digits", strategy=strategy)

    template1 = ItemTemplate.objects.create(name="Test task")
    template2 = ItemTemplate.objects.create(name="Test task")

    input_field = ItemTemplateField.objects.create(name="input", widget="TextLabel")
    template1.fields.add(input_field)
    template2.fields.add(input_field)

    annotation_field = ItemTemplateField.objects.create(name="output", widget="TextLabel",
                                                        required=True, editable=True)
    template1.fields.add(annotation_field)
    template2.fields.add(annotation_field)

    Item.objects.create(task=task, template=template1, data={input_field.name: 1}, order=1)
    Item.objects.create(task=task, template=template2, data={input_field.name: 1}, order=2)


@pytest.fixture
@pytest.mark.django_db
def setup_task_two_variables():
    users = {}
    for i in range(14):
        users[i] = EndWorker.objects.create_user("user{}".format(i),
                                                 "user{}@mail.com".format(i),
                                                 "password")

    mission = Mission.objects.create(id=1, name="Test mission")
    strategy, _ = Strategy.objects.get_or_create(name="StaticStrategyLogic")
    task = Task.objects.create(id=1, mission=mission, name="Add two digits", strategy=strategy)

    template = ItemTemplate.objects.create(name="Test task")
    input_field = ItemTemplateField.objects.create(name="input", widget="TextLabel")
    template.fields.add(input_field)
    annotation_field1 = ItemTemplateField.objects.create(name="output1", widget="TextLabel",
                                                        required=True, editable=True)
    template.fields.add(annotation_field1)
    annotation_field2 = ItemTemplateField.objects.create(name="output2", widget="TextLabel",
                                                        required=True, editable=True)
    template.fields.add(annotation_field2)

    data = [[0, 0, 0, 0, 14],
            [0, 2, 6, 4, 2],
            [0, 0, 3, 5, 6],
            [0, 3, 9, 2, 0],
            [2, 2, 8, 1, 1],
            [7, 7, 0, 0, 0],
            [3, 2, 6, 3, 0],
            [2, 5, 3, 2, 2],
            [6, 5, 2, 1, 0],
            [0, 2, 2, 3, 7]]

    for i, row in enumerate(data):
        item = Item.objects.create(task=task, template=template,
                                   data={input_field.name: i}, order=i)
        counter = 0
        for j, count in enumerate(row):
            for _ in range(count):
                Annotation.objects.create(item=item,
                                          user=users[counter],
                                          data={annotation_field1.name: j,
                                                annotation_field2.name: j})
                counter += 1


@pytest.fixture
@pytest.mark.django_db
def setup_task_missing_data():
    users = {}
    for i in range(14):
        users[i] = EndWorker.objects.create_user("user{}".format(i),
                                                 "user{}@mail.com".format(i),
                                                 "password")

    mission = Mission.objects.create(id=1, name="Test mission")
    strategy, _ = Strategy.objects.get_or_create(name="StaticStrategyLogic")
    task = Task.objects.create(id=1, mission=mission, name="Add two digits", strategy=strategy)

    template = ItemTemplate.objects.create(name="Test task")
    input_field = ItemTemplateField.objects.create(name="input", widget="TextLabel")
    template.fields.add(input_field)
    annotation_field = ItemTemplateField.objects.create(name="output", widget="TextLabel",
                                                        required=True, editable=True)
    template.fields.add(annotation_field)

    data = [[0, 0, 0, 0, 14],
            [0, 0, 0, 0, 1],
            [0, 0, 3, 5, 6],
            [0, 3, 9, 2, 0],
            [0, 0, 0, 1, 1],
            [7, 7, 0, 0, 0],
            [3, 2, 6, 3, 0],
            [2, 5, 3, 2, 2],
            [6, 5, 2, 1, 0],
            [0, 2, 2, 3, 7]]

    for i, row in enumerate(data):
        item = Item.objects.create(task=task, template=template,
                                   data={input_field.name: i}, order=i)
        counter = 0
        for j, count in enumerate(row):
            for _ in range(count):
                Annotation.objects.create(item=item,
                                          user=users[counter],
                                          data={annotation_field.name: j})
                counter += 1


