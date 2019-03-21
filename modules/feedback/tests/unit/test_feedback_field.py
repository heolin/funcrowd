import pytest

from tasks.models import Task

from modules.feedback.models.fields import (
    VoteRanking, AnnotationsCount, ReferenceValue
)


@pytest.mark.django_db
def test_vote_ranking(setup_task_with_items, setup_users):
    user1, user2, user3 = setup_users

    task = Task.objects.first()

    item = task.items.first()
    annotation_field = item.template.annotations_fields.first()

    field = VoteRanking(annotation_field.name)

    item = task.items.get(order=0)
    votes = {
        user1: {1: 0.33, 2: 0.67},
        user2: {1: 0.33, 2: 0.67},
        user3: {1: 0.33, 2: 0.67}
    }
    for annotation in item.annotations.exclude(user=None):
        for key, value in field.evaluate(annotation).items():
            assert round(value, 2) == votes[annotation.user][key]

    item = task.items.get(order=1)
    votes = {
        user1: {4: 1.0},
        user2: {4: 1.0},
        user3: {4: 1.0}
    }
    for annotation in item.annotations.exclude(user=None):
        for key, value in field.evaluate(annotation).items():
            assert round(value, 2) == votes[annotation.user][key]

    item = task.items.get(order=2)
    votes = {
        user1: {3: 0.33, 6: 0.33, 9: 0.33},
        user2: {3: 0.33, 6: 0.33, 9: 0.33},
        user3: {3: 0.33, 6: 0.33, 9: 0.33},
    }
    for annotation in item.annotations.exclude(user=None):
        for key, value in field.evaluate(annotation).items():
            assert round(value, 2) == votes[annotation.user][key]

    item = task.items.get(order=3)
    votes = {
        user1: {9: 0.33, 12: 0.67},
        user2: {9: 0.33, 12: 0.67},
        user3: {9: 0.33, 12: 0.67},
    }
    for annotation in item.annotations.exclude(user=None):
        for key, value in field.evaluate(annotation).items():
            assert round(value, 2) == votes[annotation.user][key]


@pytest.mark.django_db
def test_vote_ranking(setup_task_with_items_data_source, setup_users):
    user1, user2, user3 = setup_users

    task = Task.objects.first()

    item = task.items.first()
    annotation_field = item.template.annotations_fields.first()

    field = VoteRanking(annotation_field.name)

    item = task.items.get(order=0)
    votes = {
        user1: {1: 0.33, 2: 0.33, "<OTHER>": 0.33},
        user2: {1: 0.33, 2: 0.33, "<OTHER>": 0.33},
        user3: {1: 0.33, 2: 0.33, "<OTHER>": 0.33},
    }
    for annotation in item.annotations.exclude(user=None):
        for key, value in field.evaluate(annotation).items():
            assert round(value, 2) == votes[annotation.user][key]


@pytest.mark.django_db
def test_annotations_count(setup_task_with_items, setup_users):
    user1, user2, user3 = setup_users

    task = Task.objects.first()

    item = task.items.first()
    annotation_field = item.template.annotations_fields.first()

    field = AnnotationsCount(annotation_field.name)

    item = task.items.get(order=0)
    votes = {
        user1: 2,
        user2: 2,
        user3: 2,
    }
    for annotation in item.annotations.exclude(user=None):
        assert field.evaluate(annotation) == votes[annotation.user]

    item = task.items.get(order=1)
    votes = {
        user1: 2,
        user2: 2,
        user3: 2,
    }
    for annotation in item.annotations.exclude(user=None):
        assert field.evaluate(annotation) == votes[annotation.user]


@pytest.mark.django_db
def test_reference_value(setup_task_with_items, setup_users):
    user1, user2, user3 = setup_users

    task = Task.objects.first()

    item = task.items.first()
    annotation_field = item.template.annotations_fields.first()

    field = ReferenceValue(annotation_field.name)

    item = task.items.get(order=0)
    votes = {
        user1: [2],
        user2: [2],
        user3: [2],
    }
    for annotation in item.annotations.exclude(user=None):
        assert field.evaluate(annotation) == votes[annotation.user]

    item = task.items.get(order=1)
    votes = {
        user1: [4],
        user2: [4],
        user3: [4],
    }
    for annotation in item.annotations.exclude(user=None):
        assert field.evaluate(annotation) == votes[annotation.user]

    item = task.items.get(order=2)
    votes = {
        user1: set([3, 9]),
        user2: set([3, 9]),
        user3: set([3, 9]),
    }
    for annotation in item.annotations.exclude(user=None):
        assert set(field.evaluate(annotation)) == votes[annotation.user]
