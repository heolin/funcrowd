import pytest

from tasks.models import Task, Annotation


@pytest.mark.django_db
def test_feedback(task_with_items, users):
    user1, user2, user3 = users

    task = Task.objects.first()

    item = task.items.first()

    annotation = item.annotations.get(user=user1)
    feedback = task.feedback.create_feedback(annotation)

    assert len(feedback.values) == 1
    assert "output" in feedback.values
    assert round(feedback.values['output']['VoteRanking'][1], 2) == 0.33
    assert round(feedback.values['output']['VoteRanking'][2], 2) == 0.67
    assert round(feedback.score, 2) == 0.83

    assert len(feedback.scores) == 1
    assert "output" in feedback.scores
    assert feedback.scores['output']['ReferenceScore'] == 1.0
    assert round(feedback.scores['output']['VotingScore'], 2) == 0.67


@pytest.mark.django_db
def test_feedback_with_multiple_annotation_fields(
        task_with_items_with_multiple_annotation_fields, users):
    user1, user2, user3 = users

    task = Task.objects.first()

    item = task.items.first()

    annotation = Annotation.objects.create(item=item, user=user1,
                                           data={
                                               "first": 1,
                                               "second": 1
                                           })

    feedback = task.feedback.create_feedback(annotation)
    assert feedback.score == 2.0

    annotation = Annotation.objects.create(item=item, user=user2,
                                           data={
                                               "first": 0,
                                               "second": 1
                                           })
    feedback = task.feedback.create_feedback(annotation)
    assert feedback.score == 1.0

    annotation = Annotation.objects.create(item=item, user=user3,
                                           data={
                                               "first": 0,
                                               "second": 0
                                           })
    feedback = task.feedback.create_feedback(annotation)
    assert feedback.score == 0.0
