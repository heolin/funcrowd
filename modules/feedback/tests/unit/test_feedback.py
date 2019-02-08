import pytest

from tasks.models import Task


@pytest.mark.django_db
def test_feedback(setup_task_with_items, setup_users):
    user1, user2, user3 = setup_users

    task = Task.objects.first()

    item = task.items.first()

    annotation = item.annotations.get(user=user1)
    feedback = task.feedback.create_feedback(annotation)

    assert len(feedback.values) == 1
    assert "output" in feedback.values
    assert round(feedback.values['output']['VoteRanking'][1], 2) == 0.33
    assert round(feedback.values['output']['VoteRanking'][2], 2) == 0.67

    assert len(feedback.scores) == 1
    assert "output" in feedback.scores
    assert feedback.scores['output']['ReferenceScore'] == 1.0
    assert round(feedback.scores['output']['VotingScore'], 2) == 0.67
