import pytest

from tasks.models import (
    Task, Annotation
)

from modules.bounty.models import Bounty, UserBounty
from modules.bounty.consts import NEW, IN_PROGRESS, CLOSED, FINISHED
from modules.bounty.exceptions import OnlyOneActiveBountyPerTask


def add_annotation(item, user, value):
    annotation = Annotation.objects.create(item=item, user=user,
                                           data={"output": value})
    annotation.annotated = True
    annotation.save()
    return annotation


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
    annotation = add_annotation(item, user, "A")

    # annotation created but annotated=False
    annotation.annotated = False
    annotation.save()
    assert user_bounty._get_annotations() == 0

    # annotation created and annotated=True
    annotation.annotated = True
    annotation.save()

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


@pytest.mark.django_db
def test_one_active_bounty_per_task(setup_task_with_items, setup_user):
    user = setup_user
    task = Task.objects.first()

    bounty1 = Bounty.objects.create(task=task, annotations_target=5)
    bounty2 = Bounty.objects.create(task=task, annotations_target=3)

    user_bounty, created = UserBounty.get_or_create(bounty1, user)
    assert created

    _, created = UserBounty.get_or_create(bounty2, user)
    assert created is False

    item = None
    for i in range(5):
        item = task.next_item(user, item)
        add_annotation(item, user, "A")
    user_bounty.update()

    _, created = UserBounty.get_or_create(bounty2, user)
    assert created


@pytest.mark.django_db
def test_bounty_closed(setup_task_with_items, setup_user):
    user = setup_user
    task = Task.objects.first()

    bounty = Bounty.objects.create(task=task, annotations_target=5)
    bounty.close()

    user_bounty, created = UserBounty.get_or_create(bounty, user)
    assert created is False


@pytest.mark.django_db
def test_skipped(setup_task_with_items, setup_user):
    user = setup_user
    task = Task.objects.first()

    bounty = Bounty.objects.create(task=task, annotations_target=5)

    user_bounty, created = UserBounty.get_or_create(bounty, user)

    item = task.next_item(user, None)
    annotation = add_annotation(item, user, "A")

    assert user_bounty._get_annotations() == 1
    annotation.skipped = True
    annotation.save()
    assert user_bounty._get_annotations() == 0
    user_bounty.update()
    assert user_bounty.annotations_done == 0

    add_annotation(item, user, "A")
    user_bounty.update()
    assert user_bounty.annotations_done == 1


@pytest.mark.django_db
def test_automatic_finish_bounty(setup_task_with_items):
    task = Task.objects.first()

    bounty1 = Bounty.objects.create(task=task, annotations_target=1)
    assert bounty1.closed is False

    bounty2 = Bounty.objects.create(task=task, annotations_target=2)
    bounty1 = Bounty.objects.get(id=bounty1.id)
    assert bounty1.closed is True
    assert bounty2.closed is False


@pytest.mark.django_db
def test_bounty_finish_and_close(setup_task_with_items, setup_user):
    user = setup_user
    task = Task.objects.first()

    bounty = Bounty.objects.create(task=task, annotations_target=5)

    user_bounty, _ = UserBounty.get_or_create(bounty, user)
    assert user_bounty.status == NEW

    item = task.next_item(user, None)
    add_annotation(item, user, "A")
    user_bounty.update()
    assert user_bounty.status == IN_PROGRESS

    bounty.finish()
    user_bounty, _ = UserBounty.get_or_create(bounty, user)
    assert user_bounty.status == FINISHED

    bounty.close()
    user_bounty, _ = UserBounty.get_or_create(bounty, user)
    assert user_bounty.status == CLOSED

    bounty.finish()
    user_bounty, _ = UserBounty.get_or_create(bounty, user)
    assert user_bounty.status == CLOSED
