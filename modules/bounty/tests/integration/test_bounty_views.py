import pytest
from rest_framework.test import APIRequestFactory, force_authenticate

from modules.bounty.api.views.bounty import BountyListView, StartBountyView
from modules.bounty.models import Bounty
from tasks.models import Task


@pytest.mark.django_db
def test_bounty_views(setup_task_with_items, setup_user):
    user = setup_user
    task = Task.objects.first()

    bounty = Bounty.objects.create(task=task, annotations_target=5)

    factory = APIRequestFactory()

    # user bounty is not started so it is none
    request = factory.get('/api/v1/bounty/')
    force_authenticate(request, user)
    view = BountyListView.as_view()
    response = view(request)

    assert len(response.data) == 1
    assert response.data[0] == {
        'id': bounty.id,
        'task': {
            'id': task.id,
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
def test_bounty_views_start(setup_task_with_items, setup_user):
    user = setup_user
    task = Task.objects.first()

    bounty = Bounty.objects.create(task=task, annotations_target=5)

    factory = APIRequestFactory()

    # start selected bounty
    request = factory.get('/api/v1/bounty/start')
    force_authenticate(request, user)
    view = StartBountyView.as_view()
    response = view(request, bounty.id)
    assert response.data['id'] == bounty.id
    assert response.data['user_bounty']['id'] == bounty.get_user_bounty(user).id

    # see list of all bounties
    request = factory.get('/api/v1/bounty/')
    force_authenticate(request, user)
    view = BountyListView.as_view()
    response = view(request)

    assert len(response.data) == 1
    assert response.data[0] == {
        'id': bounty.id,
        'task': {
            'id': task.id,
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
def test_closed_bounty_views(setup_task_with_items, setup_user):
    user = setup_user
    task = Task.objects.first()

    bounty = Bounty.objects.create(task=task, annotations_target=5)
    bounty.close()

    factory = APIRequestFactory()

    request = factory.get('/api/v1/bounty/')
    force_authenticate(request, user)
    view = BountyListView.as_view()
    response = view(request)

    assert len(response.data) == 1
    assert response.data[0]['user_bounty'] is None


