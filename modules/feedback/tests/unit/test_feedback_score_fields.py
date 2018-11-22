import pytest

from tasks.models import Task

from modules.feedback.models.score_fields import (
    VotingScore, ReferenceScore
)


@pytest.mark.django_db
def test_reference_score(setup_task_with_items, setup_users):
    user1, user2, user3 = setup_users

    task = Task.objects.first()

    item = task.items.first()
    annotation_field = item.template.annotations_fields.first()

    scorer = ReferenceScore(annotation_field.name)

    item = task.items.get(order=0)
    scores = {user1: 1, user2: 1, user3: 0}
    for annotation in item.annotations.exclude(user=None):
        assert scorer.score(annotation) == scores[annotation.user]

    item = task.items.get(order=1)
    scores = {user1: 1, user2: 1, user3: 1}
    for annotation in item.annotations.exclude(user=None):
        assert scorer.score(annotation) == scores[annotation.user]

    item = task.items.get(order=2)
    scores = {user1: 0, user2: 0.5, user3: 0.5}
    for annotation in item.annotations.exclude(user=None):
        assert scorer.score(annotation) == scores[annotation.user]

    item = task.items.get(order=3)
    for annotation in item.annotations.exclude(user=None):
        assert scorer.score(annotation) is None


@pytest.mark.django_db
def test_voting_score(setup_task_with_items, setup_users):
    user1, user2, user3 = setup_users

    task = Task.objects.first()

    item = task.items.first()
    annotation_field = item.template.annotations_fields.first()

    scorer = VotingScore(annotation_field.name)

    item = task.items.get(order=0)
    scores = {user1: 0.5, user2: 0.5, user3: 0}
    for annotation in item.annotations.exclude(user=None):
        assert scorer.score(annotation) == scores[annotation.user]

    item = task.items.get(order=1)
    scores = {user1: 1, user2: 1, user3: 1}
    for annotation in item.annotations.exclude(user=None):
        assert scorer.score(annotation) == scores[annotation.user]

    item = task.items.get(order=2)
    scores = {user1: 0, user2: 0, user3: 0}
    for annotation in item.annotations.exclude(user=None):
        assert scorer.score(annotation) == scores[annotation.user]

    item = task.items.get(order=3)
    scores = {user1: 0.5, user2: 0.5, user3: 0}
    for annotation in item.annotations.exclude(user=None):
        assert scorer.score(annotation) == scores[annotation.user]
