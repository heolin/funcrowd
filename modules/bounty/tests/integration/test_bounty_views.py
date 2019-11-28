import pytest
from django.test import Client

from modules.bounty.models import Bounty
from tasks.models import Task


@pytest.mark.django_db
def test_bounty_views(task_with_items, user1):
    task = Task.objects.first()
    bounty = Bounty.objects.create(task=task, annotations_target=5)

    client = Client()
    client.force_login(user1)

    # user bounty is not started so it is none
    response = client.get('/api/v1/bounty/')

    assert len(response.data) == 1
    assert response.data[0] == {
        'id': bounty.id,
        'task': {
            'id': task.id,
            'mission': task.mission.id,
            'name': task.name,
            'description': task.description,
            'instruction': task.instruction,
            'keywords': task.keywords,
            'metadata': task.metadata,
            'total_exp': 0
        },
        'closed': False,
        'annotations_target': bounty.annotations_target,
        'user_bounty': None
    }


@pytest.mark.django_db
def test_bounty_views_start(task_with_items, user1):
    task = Task.objects.first()
    bounty = Bounty.objects.create(task=task, annotations_target=5)

    client = Client()
    client.force_login(user1)

    # start selected bounty
    response = client.get('/api/v1/bounty/{0}/start/'.format(bounty.id))
    assert response.data['id'] == bounty.id
    assert response.data['user_bounty']['id'] == bounty.get_user_bounty(user1).id

    # see list of all bounties
    response = client.get('/api/v1/bounty/')

    assert len(response.data) == 1
    assert response.data[0] == {
        'id': bounty.id,
        'task': {
            'id': task.id,
            'mission': task.mission.id,
            'name': task.name,
            'description': task.description,
            'instruction': task.instruction,
            'keywords': task.keywords,
            'metadata': task.metadata,
            'total_exp': 0
        },
        'closed': False,
        'annotations_target': bounty.annotations_target,
        'user_bounty': {
            'id': 1,
            'progress': 0.0,
            'status': 'NEW',
            'annotations_done': 0,
        }
    }


@pytest.mark.django_db
def test_closed_bounty_views(task_with_items, user1):
    task = Task.objects.first()
    bounty = Bounty.objects.create(task=task, annotations_target=5)
    bounty.close()

    client = Client()
    client.force_login(user1)

    response = client.get('/api/v1/bounty/')

    assert len(response.data) == 1
    assert response.data[0]['user_bounty'] is None
