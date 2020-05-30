import pytest

from modules.feedback.consts import FeedbackTypes
from modules.feedback.models import FeedbackScoreField, Feedback
from modules.order_strategy.models import Strategy
from tasks.models import Mission, Task, Item, Annotation
from tests.utils import add_annotation


@pytest.fixture
@pytest.mark.django_db
def one_mission():
    Strategy.register_values()
    FeedbackScoreField.register_values()

    # create the mission
    mission = Mission.objects.create(name="Test mission")
    return mission


@pytest.fixture
@pytest.mark.django_db
def one_mission_one_task(one_mission):
    mission = one_mission

    # create the task
    task = Task.objects.create(
        mission=mission,
        name="Add two digits",
        strategy=Strategy.objects.get(name="DepthFirstStrategyLogic")
    )

    # attach feedback type to the task
    feedback = Feedback.objects.create(task=task, type=FeedbackTypes.BINARY)
    feedback.score_fields.add(
        FeedbackScoreField.objects.get(name="ReferenceScore")
    )
    return task


@pytest.fixture
@pytest.mark.django_db
def one_task_items_with_reference_annotation(
        one_mission_one_task, item_template_one_input_one_output):
    task = one_mission_one_task
    template = item_template_one_input_one_output

    # create items
    input_field = template.items_fields.first()
    output_field = template.annotations_fields.first()

    for index in range(3):
        item = Item.objects.create(task=task,
                                   template=template,
                                   data={input_field.name: 1},
                                   order=index)

        Annotation.objects.create(item=item,
                                  user=None,
                                  data={output_field.name: str(index)})

    return task


@pytest.fixture
@pytest.mark.django_db
def one_task_items_with_annotations_and_reference(
        one_mission_one_task, item_template_one_input_one_output, users):
    """
    A task with multiple items, each item
    will have 5 annotations with one from 3 possible values.
    Additionally item will have a reference annotation.
    """

    task = one_mission_one_task
    template = item_template_one_input_one_output

    # create items
    input_field = template.items_fields.first()
    output_field = template.annotations_fields.first()

    for index, (answers_counts, correct_answer) in enumerate([
        ({'0': 2, '1': 2, '2': 1}, 0),
        ({'0': 1, '1': 4, '2': 0}, 1),
        ({'0': 1, '1': 2, '2': 2}, 2),
        ({'0': 2, '1': 2, '2': 1}, 0),
        ({'0': 1, '1': 4, '2': 0}, 1),
        ({'0': 1, '1': 2, '2': 2}, 2),
    ]):
        item = Item.objects.create(task=task,
                                   template=template,
                                   data={input_field.name: index},
                                   order=index)

        # create a reference annotation
        Annotation.objects.create(item=item,
                                  user=None,
                                  data={output_field.name: correct_answer})

        # create annotations made by users
        user_index = 0
        for key, count in answers_counts.items():
            for _ in range(count):
                add_annotation(item=item,
                               user=users[user_index],
                               data={output_field.name: key})
                user_index += 1

    return task


@pytest.fixture
@pytest.mark.django_db
def one_task_items_with_list_annotations_and_reference(
        one_mission_one_task, item_template_one_input_one_list_output, users):
    """
    TODO
    """

    task = one_mission_one_task
    template = item_template_one_input_one_list_output

    # create items
    input_field = template.items_fields.first()
    output_field = template.annotations_fields.first()

    for index, (answers_counts, correct_answer) in enumerate([
        ({('1',): 2, ('1', '2'): 2, ('2',): 1}, ['1']),
        ({('1', '2'): 1, ('2',): 4, ('3',): 0}, ['1', '2']),
        ({('1', '2', '3'): 1, ('2',): 2, ('3',): 3}, ['2', '3']),
    ]):
        item = Item.objects.create(task=task, template=template,
                                   data={input_field.name: index}, order=index)

        # create a reference annotation
        Annotation.objects.create(item=item,
                                  user=None,
                                  data={output_field.name: correct_answer})

        # create annotations made by users
        user_index = 0
        for key, count in answers_counts.items():
            for _ in range(count):
                add_annotation(item=item,
                               user=users[user_index],
                               data={output_field.name: key})
                user_index += 1

    return task
