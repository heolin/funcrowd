import pytest

from modules.feedback.models import Feedback, FeedbackScoreField, FeedbackField
from modules.statistics.models.utils.update_users_statistics import update_user_stats
from tasks.consts import IN_PROGRESS, VERIFICATION, FINISHED
from tasks.controllers.annotation_controller import AnnotationController
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

    for i, document in enumerate(task1.mission.documents.all()):
        Item.objects.create(task=task1, template=template, order=i,
                            data={first_field.name: i}, document=document)

    for i, document in enumerate(task4.mission.documents.all()):
        Item.objects.create(task=task4, template=template, order=i,
                            data={first_field.name: i}, document=document)


@pytest.fixture
@pytest.mark.django_db
def setup_tasks_annotations():
    data = [[0, 0, 0, 0, 14],
            [0, 0, 0, 12, 2],
            [0, 0, 0, 8, 6],
            [0, 3, 9, 2, 0],
            [0, 0, 12, 1, 1],
            [12, 2, 0, 0, 0],
            [3, 10, 1, 0, 0],
            [14, 0, 0, 0, 0],
            [10, 0, 2, 2, 0],
            [0, 0, 13, 0, 1]]

    Strategy.register_values()
    strategy = Strategy.objects.get(name="StaticStrategyLogic")
    mission = Mission.objects.create(name="Test mission 4")
    task = Task.objects.create(mission=mission, name="Task 1", strategy=strategy)
    template = ItemTemplate.objects.create(name="Test template")
    first_field = ItemTemplateField.objects.create(name="first", widget="TextLabel")
    template.fields.add(first_field)
    annotation_field = ItemTemplateField.objects.create(name="output", widget="TextLabel",
                                                        required=True, editable=True, feedback=True)
    template.fields.add(annotation_field)

    FeedbackScoreField.register_values()
    FeedbackField.register_values()
    feedback = Feedback.objects.create(task=task)
    feedback.fields.add(FeedbackField.objects.get(name="VoteRanking"))
    feedback.score_fields.add(FeedbackScoreField.objects.get(name="VotingScore"))

    documents = {}
    for i in range(len(data)):
        documents[i] = Document.objects.create(name="Doc{}".format(i), mission=mission)

    users = {}
    for i in range(14):
        users[i] = EndWorker.objects.create_user("user{}".format(i),
                                                 "user{}@mail.com".format(i),
                                                 "password")
        users[i].stats  # creates user stast
        users[i].get_mission_stats(mission.id)

    for i, row in enumerate(data):
        item = Item.objects.create(task=task, template=template, document=documents[i],
                                   data={first_field.name: i}, order=i)
        counter = 0
        for j, count in enumerate(row):
            for _ in range(count):
                Annotation.objects.create(item=item,
                                          user=users[counter],
                                          data={annotation_field.name: j})
                counter += 1

    for annotation in Annotation.objects.all():
        AnnotationController().process(annotation)

    update_user_stats()


@pytest.fixture
@pytest.mark.django_db
def setup_two_missions(setup_tasks_items, setup_user):

    item1 = Item.objects.filter(task__name="Task 1").first()
    item4 = Item.objects.filter(task__name="Task 4").first()

    add_annotation(item1, setup_user, "A")
    add_annotation(item4, setup_user, "A")
