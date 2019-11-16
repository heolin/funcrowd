import pytest
from django.test import Client

from modules.bounty.consts import BountyStatus
from modules.bounty.models import Bounty
from modules.bounty.tests.unit.test_bounty import add_annotation
from tasks.models import Task


@pytest.mark.django_db
def test_user_bounty_views(task_with_items, user1):
    task = Task.objects.first()
    bounty = Bounty.objects.create(task=task, annotations_target=5)

    client = Client()
    client.force_login(user1)

    # Getting bounty status does not creates user bounty
    response = client.get('/api/v1/bounty/{}/status'.format(bounty.id))
    assert response.data is None
    assert response.status_code == 204

    user_bounty, _ = bounty.get_or_create_user_bounty(user1)

    # Check user bounty serialization format
    response = client.get('/api/v1/bounty/{}/status'.format(bounty.id))

    assert response.data == {
        'id': user_bounty.id,
        'bounty': bounty.id,
        'status': user_bounty.status,
        'progress': 0.0,
        'annotations_done': 0,
        'annotations_target': bounty.annotations_target,
        'reward': None,
        'rewards_list': []
    }


@pytest.mark.django_db
def test_user_redo_bounty(task_with_items, user1):
    task = Task.objects.first()
    bounty = Bounty.objects.create(task=task, annotations_target=5)

    client = Client()
    client.force_login(user1)

    # Start bounty
    client.get('/api/v1/bounty/{}/start'.format(bounty.id))

    _, created = bounty.get_or_create_user_bounty(user1)
    assert not created

    # Finish bounty and check status
    item = None
    for i in range(5):
        item = task.next_item(user1, item)
        add_annotation(item, user1, "A")

    response = client.get('/api/v1/bounty/{}/status'.format(bounty.id))
    assert response.data['status'] == BountyStatus.FINISHED
    assert response.data['reward'] is not None

    # Start next bounty
    prev_user_bounty_id = response.data['id']

    response = client.get('/api/v1/bounty/{}/start'.format(bounty.id))
    assert response.data['user_bounty']['status'] == BountyStatus.NEW
    assert prev_user_bounty_id != response.data['user_bounty']['id']

    # Check status
    response = client.get('/api/v1/bounty/{}/status'.format(bounty.id))
    assert response.data['status'] == BountyStatus.NEW
    assert response.data['reward'] is None
    assert len(response.data['rewards_list']) == 1
