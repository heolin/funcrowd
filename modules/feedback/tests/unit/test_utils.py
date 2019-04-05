import pytest

from modules.feedback.models.utils.voting import get_votings
from tasks.models import Task


@pytest.mark.django_db
def test_feedback(setup_task_with_items_multiple_choice_data_source, setup_users):
    user1, user2, user3 = setup_users

    task = Task.objects.first()
    field = task.items.first().template.fields.get(name='output')

    item = task.items.first()
    df_probs = get_votings(item.annotations.all(), field)
    reference = {
        "2": 0.6,
        "1": 0.4
    }
    for key, value in df_probs.to_dict().items():
        assert value == reference[key]

    reference = {
        "2": 0.25,
        "1": 0.5,
        '<OTHER>': 0.25
    }
    item = task.items.last()
    df_probs = get_votings(item.annotations.all(), field)
    for key, value in df_probs.to_dict().items():
        assert value == reference[key]

