import pytest

from tasks.models import (
    Task, Annotation
)

from modules.bounty.models import Bounty, UserBounty
from modules.bounty.consts import NEW, IN_PROGRESS, CLOSED, FINISHED


def add_annotation(item, user, value):
    return Annotation.objects.create(item=item, user=user,
                                     data={"output": value})


@pytest.mark.django_db
def test_bounty(setup_task_with_items, setup_user):
    user = setup_user
    task = Task.objects.first()

    bounty = Bounty.objects.create(task=task, annotations_target=5)

    user_bounty, created = UserBounty.get_or_create(bounty, user)
    assert created
    assert user_bounty.annotations_done == 0
    assert user_bounty.status == NEW
    assert len(user_bounty.reward_token) == 32

    user_bounty, created = UserBounty.get_or_create(bounty, user)
    assert created is False

    item = task.next_item(user, None)
    add_annotation(item, user, "A")

    assert user_bounty._get_annotations() == 1
    assert user_bounty.annotations_done == 0
    user_bounty.update()
    assert user_bounty.annotations_done == 1
    assert user_bounty.progress == 0.2
    assert user_bounty.status == IN_PROGRESS
    assert user_bounty.reward is None

    for i in range(4):
        item = task.next_item(user, item)
        add_annotation(item, user, "A")
    user_bounty.update()

    assert user_bounty.annotations_done == 5
    assert user_bounty.progress == 1.0
    assert user_bounty.status == FINISHED

    user_bounty.close()
    assert user_bounty.status == CLOSED
    assert user_bounty.reward is not None


@pytest.mark.django_db
def test_bounty_pre_annotations(setup_task_with_items, setup_user):
    user = setup_user
    task = Task.objects.first()

    item = task.next_item(user, None)
    add_annotation(item, user, "A")
    item = task.next_item(user, item)
    add_annotation(item, user, "A")

    bounty = Bounty.objects.create(task=task, annotations_target=5)

    user_bounty, created = UserBounty.get_or_create(bounty, user)
    assert user_bounty._get_annotations() == 2
    assert user_bounty.annotations_done == 0
    user_bounty.update()
    assert user_bounty.annotations_done == 0

    item = task.next_item(user, item)
    add_annotation(item, user, "A")
    user_bounty.update()
    assert user_bounty._get_annotations() == 3
    assert user_bounty.annotations_done == 1

    for i in range(4):
        item = task.next_item(user, item)
        add_annotation(item, user, "A")
    user_bounty.update()
    assert user_bounty.status == FINISHED

