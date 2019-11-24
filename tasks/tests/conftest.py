import pytest

from modules.feedback.models import FeedbackScoreField, Feedback
from modules.feedback.models.fields import FeedbackField
from tasks.models import (
    Mission, Task, Item, ItemTemplate, ItemTemplateField, Annotation
)
from users.models import EndWorker

from modules.order_strategy.models import Strategy


@pytest.fixture
@pytest.mark.django_db
def user1():
    user = EndWorker.objects.create_superuser("user1@mail.com", "password", username="user1")
    return user


@pytest.fixture
@pytest.mark.django_db
def user2():
    user = EndWorker.objects.create_superuser("user2@mail.com", "password", username="user2")
    return user


@pytest.fixture
@pytest.mark.django_db
def task():
    Strategy.register_values()

    mission = Mission.objects.create(id=1, name="Test mission")
    strategy = Strategy.objects.get(name="StaticStrategyLogic")
    Task.objects.create(id=1, order=1, mission=mission, name="Add two digits", strategy=strategy)

    Mission.objects.create(id=2, name="Test mission other")


@pytest.fixture
@pytest.mark.django_db
def task_with_items():
    Strategy.register_values()

    mission = Mission.objects.create(id=1, name="Test mission", order=1)
    strategy = Strategy.objects.get(name="StaticStrategyLogic")
    task = Task.objects.create(id=1, order=1, mission=mission, name="Add two digits", strategy=strategy)

    template = ItemTemplate.objects.create(name="Adding two")
    first_field = ItemTemplateField.objects.create(name="first", widget="TextLabel")
    template.fields.add(first_field)
    second_field = ItemTemplateField.objects.create(name="second", widget="TextLabel")
    template.fields.add(second_field)
    annotation_field = ItemTemplateField.objects.create(name="output", widget="TextLabel",
                                                        required=True, editable=True, feedback=True)
    template.fields.add(annotation_field)
    optional_annotation_field = ItemTemplateField.objects.create(name="optional", widget="TextLabel",
                                                                 required=False, editable=True)

    template.fields.add(optional_annotation_field)

    Item.objects.create(task=task, template=template, order=1,
                        data={first_field.name: 1, second_field.name: 2}, exp=10)
    Item.objects.create(task=task, template=template, order=2,
                        data={first_field.name: 2, second_field.name: 2})
    Item.objects.create(task=task, template=template, order=3,
                        data={first_field.name: 2, second_field.name: 2})
    Item.objects.create(task=task, template=template, order=4,
                        data={first_field.name: 2, second_field.name: 2})

@pytest.fixture
@pytest.mark.django_db
def task_with_items_data_source():
    Strategy.register_values()

    mission = Mission.objects.create(id=1, name="Mission1")
    strategy = Strategy.objects.get(name="StaticStrategyLogic")
    task = Task.objects.create(id=1, mission=mission, name="Add two digits", strategy=strategy)

    template = ItemTemplate.objects.create(name="Adding two")
    first_field = ItemTemplateField.objects.create(name="first", widget="TextLabel")
    template.fields.add(first_field)
    source_field = ItemTemplateField.objects.create(name="ALL_VALUES", widget="Hidden")
    template.fields.add(source_field)
    annotation_field = ItemTemplateField.objects.create(name="output", widget="TextLabel",
                                                        required=True, editable=True, feedback=True,
                                                        data_source=source_field)
    template.fields.add(annotation_field)

    Item.objects.create(task=task, template=template, order=1,
                        data={first_field.name: 1, source_field.name: ["A", "B"]})


@pytest.fixture
@pytest.mark.django_db
def two_missions(task_with_items):
    mission1 = Mission.objects.get(order=1)
    mission2 = Mission.objects.create(id=2, name="Mission2", order=2, parent=mission1)
    Mission.objects.create(id=3, name="Mission3", order=3)

    strategy = Strategy.objects.get(name="StaticStrategyLogic")
    template = ItemTemplate.objects.get(name="Adding two")

    task1 = Task.objects.create(id=2, mission=mission2, name="Add two digits", strategy=strategy)
    Item.objects.create(task=task1, template=template, order=1, data={"test": 1}, exp=10)

    task2 = Task.objects.create(id=3, mission=mission2, name="Add two digits", strategy=strategy)
    Item.objects.create(task=task2, template=template, order=1, data={"test": 1}, exp=10)


@pytest.fixture
@pytest.mark.django_db
def task_with_items_with_multiple_annotation_fields():
    Strategy.register_values()
    FeedbackScoreField.register_values()

    mission = Mission.objects.create(id=1, name="Test mission")
    strategy = Strategy.objects.get(name="StaticStrategyLogic")
    task = Task.objects.create(id=1, mission=mission, name="Add two digits", strategy=strategy)
    task.multiple_annotations = True
    task.save()

    feedback = Feedback.objects.create(task=task)
    feedback.score_fields.add(FeedbackScoreField.objects.get(name="ReferenceScore"))

    template = ItemTemplate.objects.create(name="Adding two")
    annotation_field1 = ItemTemplateField.objects.create(name="first", widget="TextLabel",
                                                         required=True, editable=True, feedback=True)
    template.fields.add(annotation_field1)
    annotation_field2 = ItemTemplateField.objects.create(name="second", widget="TextLabel",
                                                         required=True, editable=True, feedback=True)
    template.fields.add(annotation_field2)

    item = Item.objects.create(task=task, template=template, data={}, order=0)
    Annotation.objects.create(item=item, user=None, data={
        annotation_field1.name: 1,
        annotation_field2.name: 1
    })

    item = Item.objects.create(task=task, template=template, data={}, order=1)
    Annotation.objects.create(item=item, user=None, data={
        annotation_field1.name: 1,
        annotation_field2.name: 1
    })

    item = Item.objects.create(task=task, template=template, data={}, order=2)
    Annotation.objects.create(item=item, user=None, data={
        annotation_field1.name: 1,
        annotation_field2.name: 1
    })


def add_annotation(item, user):
    annotation, created = item.get_or_create_annotation(user)
    annotation.data = {"output": "1"}
    annotation.annotated = True
    annotation.save()
    return annotation, created
