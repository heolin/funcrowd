import pytest

from tasks.models import (
    Mission, Task, Item, ItemTemplate, ItemTemplateField, Annotation
)
from modules.feedback.models.feedback import (
    Feedback, FeedbackScoreField, FeedbackField
)
from tasks.field_types import LIST

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
def setup_users():
    user1 = EndWorker.objects.create_user("user1", "user@mail.com", "password")
    user2 = EndWorker.objects.create_user("user2", "user@mail.com", "password")
    user3 = EndWorker.objects.create_user("user3", "user@mail.com", "password")
    return user1, user2, user3


def add_annotation(item, field_name, value, user):
    annotation, _ = item.get_or_create_annotation(user)
    annotation.data[field_name] = value
    annotation.save()


@pytest.fixture
@pytest.mark.django_db
def setup_task_with_items(setup_users):
    FeedbackScoreField.register_values()
    FeedbackField.register_values()

    user1, user2, user3 = setup_users

    mission = Mission.objects.create(id=1, name="Test mission")
    strategy = Strategy.objects.get(name="StaticStrategyLogic")
    task = Task.objects.create(id=1, mission=mission, name="Add two digits", strategy=strategy)
    task.multiple_annotations = True
    task.save()

    feedback = Feedback.objects.create(task=task)
    feedback.fields.add(FeedbackField.objects.get(name="VoteRanking"))
    feedback.score_fields.add(FeedbackScoreField.objects.get(name="ReferenceScore"))
    feedback.score_fields.add(FeedbackScoreField.objects.get(name="VotingScore"))

    template = ItemTemplate.objects.create(name="Adding two")
    first_field = ItemTemplateField.objects.create(name="first", widget="TextLabel")
    template.fields.add(first_field)
    annotation_field = ItemTemplateField.objects.create(name="output", widget="TextLabel",
                                                        required=True, editable=True, feedback=True)
    template.fields.add(annotation_field)

    item = Item.objects.create(task=task, template=template, data={first_field.name: 1}, order=0)
    add_annotation(item, annotation_field.name, 2, user1)
    add_annotation(item, annotation_field.name, 2, user2)
    add_annotation(item, annotation_field.name, 1, user3)
    add_annotation(item, annotation_field.name, 2, None)

    item = Item.objects.create(task=task, template=template, data={first_field.name: 2}, order=1)
    add_annotation(item, annotation_field.name, 4, user1)
    add_annotation(item, annotation_field.name, 4, user2)
    add_annotation(item, annotation_field.name, 4, user3)
    add_annotation(item, annotation_field.name, 4, None)

    item =Item.objects.create(task=task, template=template, data={first_field.name: 3}, order=2)
    add_annotation(item, annotation_field.name, 6, user1)
    add_annotation(item, annotation_field.name, 3, user2)
    add_annotation(item, annotation_field.name, 9, user3)
    add_annotation(item, annotation_field.name, 9, None)
    add_annotation(item, annotation_field.name, 3, None)

    item = Item.objects.create(task=task, template=template, data={first_field.name: 4}, order=3)
    add_annotation(item, annotation_field.name, 12, user1)
    add_annotation(item, annotation_field.name, 12, user2)
    add_annotation(item, annotation_field.name, 9, user3)


@pytest.fixture
@pytest.mark.django_db
def setup_task_with_items_multiple_choice(setup_users):
    FeedbackScoreField.register_values()
    FeedbackField.register_values()

    user1, user2, user3 = setup_users

    mission = Mission.objects.create(id=1, name="Test mission")
    strategy = Strategy.objects.get(name="StaticStrategyLogic")
    task = Task.objects.create(id=1, mission=mission, name="Add two digits", strategy=strategy)
    task.multiple_annotations = True
    task.save()

    feedback = Feedback.objects.create(task=task)
    feedback.fields.add(FeedbackField.objects.get(name="VoteRanking"))
    feedback.score_fields.add(FeedbackScoreField.objects.get(name="ReferenceScore"))
    feedback.score_fields.add(FeedbackScoreField.objects.get(name="VotingScore"))

    template = ItemTemplate.objects.create(name="Adding two")
    first_field = ItemTemplateField.objects.create(name="first", widget="TextLabel")
    template.fields.add(first_field)
    annotation_field = ItemTemplateField.objects.create(name="output", widget="MultipleChoiceField",
                                                        required=True, editable=True, feedback=True,
                                                        type=LIST)
    template.fields.add(annotation_field)

    item = Item.objects.create(task=task, template=template, data={first_field.name: 1}, order=0)
    add_annotation(item, annotation_field.name, [2], user1)
    add_annotation(item, annotation_field.name, [2, 1], user2)
    add_annotation(item, annotation_field.name, [1], user3)
    add_annotation(item, annotation_field.name, [2], None)

    item = Item.objects.create(task=task, template=template, data={first_field.name: 2}, order=1)
    add_annotation(item, annotation_field.name, [4], user1)
    add_annotation(item, annotation_field.name, [4], user2)
    add_annotation(item, annotation_field.name, [4], user3)
    add_annotation(item, annotation_field.name, [4], None)

    item =Item.objects.create(task=task, template=template, data={first_field.name: 3}, order=2)
    add_annotation(item, annotation_field.name, [6, 3], user1)
    add_annotation(item, annotation_field.name, [3], user2)
    add_annotation(item, annotation_field.name, [9, 12], user3)
    add_annotation(item, annotation_field.name, [9], None)
    add_annotation(item, annotation_field.name, [3], None)

    item = Item.objects.create(task=task, template=template, data={first_field.name: 4}, order=3)
    add_annotation(item, annotation_field.name, [12], user1)
    add_annotation(item, annotation_field.name, [12], user2)
    add_annotation(item, annotation_field.name, [9], user3)


@pytest.fixture
@pytest.mark.django_db
def setup_task_with_items_data_source(setup_users):
    FeedbackScoreField.register_values()
    FeedbackField.register_values()

    user1, user2, user3 = setup_users

    mission = Mission.objects.create(id=1, name="Test mission")
    strategy = Strategy.objects.get(name="StaticStrategyLogic")
    task = Task.objects.create(id=1, mission=mission, name="Add two digits", strategy=strategy)
    task.multiple_annotations = True
    task.save()

    feedback = Feedback.objects.create(task=task)
    feedback.fields.add(FeedbackField.objects.get(name="VoteRanking"))
    feedback.score_fields.add(FeedbackScoreField.objects.get(name="ReferenceScore"))
    feedback.score_fields.add(FeedbackScoreField.objects.get(name="VotingScore"))

    template = ItemTemplate.objects.create(name="Adding two")
    values_field = ItemTemplateField.objects.create(name="values", widget="Hidden")
    template.fields.add(values_field)
    first_field = ItemTemplateField.objects.create(name="first", widget="TextLabel")
    template.fields.add(first_field)
    annotation_field = ItemTemplateField.objects.create(name="output", widget="TextLabel", data_source=values_field,
                                                        required=True, editable=True, feedback=True)
    template.fields.add(annotation_field)

    item = Item.objects.create(task=task, template=template,
                               data={first_field.name: 1, values_field.name: [1, 2]}, order=0)
    add_annotation(item, annotation_field.name, 3, user1)
    add_annotation(item, annotation_field.name, 2, user2)
    add_annotation(item, annotation_field.name, 1, user3)

    item = Item.objects.create(task=task, template=template,
                               data={first_field.name: 2, values_field.name: [1, 2]}, order=1)
    add_annotation(item, annotation_field.name, 4, user1)
    add_annotation(item, annotation_field.name, 4, user2)
    add_annotation(item, annotation_field.name, 4, user3)


@pytest.fixture
@pytest.mark.django_db
def setup_task_with_items_multiple_choice_data_source(setup_users):
    FeedbackScoreField.register_values()
    FeedbackField.register_values()

    user1, user2, user3 = setup_users

    mission = Mission.objects.create(id=1, name="Test mission")
    strategy = Strategy.objects.get(name="StaticStrategyLogic")
    task = Task.objects.create(id=1, mission=mission, name="Add two digits", strategy=strategy)
    task.multiple_annotations = True
    task.save()

    feedback = Feedback.objects.create(task=task)
    feedback.fields.add(FeedbackField.objects.get(name="VoteRanking"))
    feedback.score_fields.add(FeedbackScoreField.objects.get(name="ReferenceScore"))
    feedback.score_fields.add(FeedbackScoreField.objects.get(name="VotingScore"))

    template = ItemTemplate.objects.create(name="Adding two")
    values_field = ItemTemplateField.objects.create(name="values", widget="Hidden")
    template.fields.add(values_field)
    first_field = ItemTemplateField.objects.create(name="first", widget="TextLabel")
    template.fields.add(first_field)
    annotation_field = ItemTemplateField.objects.create(name="output", widget="TextLabel", data_source=values_field,
                                                        required=True, editable=True, feedback=True, type=LIST)
    template.fields.add(annotation_field)

    item = Item.objects.create(task=task, template=template,
                               data={first_field.name: 1, values_field.name: ["1", "2"]}, order=0)
    add_annotation(item, annotation_field.name, ["2"], user1)
    add_annotation(item, annotation_field.name, ["2", "1"], user2)
    add_annotation(item, annotation_field.name, ["1"], user3)
    add_annotation(item, annotation_field.name, ["2"], None)

    item = Item.objects.create(task=task, template=template,
                               data={first_field.name: 1, values_field.name: ["1", "2"]}, order=1)
    add_annotation(item, annotation_field.name, ["1"], user1)
    add_annotation(item, annotation_field.name, ["1", "2"], user2)
    add_annotation(item, annotation_field.name, ["1", "3"], user3)
