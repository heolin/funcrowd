import pytest
from rest_framework.test import APIRequestFactory, force_authenticate

from modules.bounty.api.views.bounty import BountyListView
from modules.bounty.api.views.user_bounty import BountyStatusView, FirstOrNextBountyView
from modules.bounty.consts import BountyStatus
from modules.bounty.models import Bounty, UserBounty
from modules.bounty.tests.unit.test_bounty import add_annotation
from tasks.models import Task

"""
    path('bounty/<int:bounty_id>/status', BountyStatusView.as_view(), name='bounty_status'),
    path('bounty/<int:bounty_id>/start', FirstOrNextBountyView.as_view(), name='bounty_next'),
    path('bounty/<int:bounty_id>', BountyDetailsView.as_view(), name='bounty_view'),
    path('bounty/', BountyListView.as_view(), name='bounty_list'),
"""

@pytest.mark.django_db
def test_user_bounty_views(setup_task_with_items, setup_user):
    user = setup_user
    task = Task.objects.first()

    bounty = Bounty.objects.create(task=task, annotations_target=5)

    factory = APIRequestFactory()

    # Getting bounty status creates user bounty
    request = factory.get('/api/v1/bounty/{}/status'.format(bounty.id))
    force_authenticate(request, user)
    view = BountyStatusView.as_view()
    response = view(request, bounty.id)

    user_bounty, _ = bounty.get_or_create_user_bounty(setup_user)

    # Check user bounty serialization format
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
def test_user_redo_bounty(setup_task_with_items, setup_user):
    user = setup_user
    task = Task.objects.first()

    bounty = Bounty.objects.create(task=task, annotations_target=5)

    factory = APIRequestFactory()

    # Start bounty
    request = factory.get('/api/v1/bounty/{}/bounty_next'.format(bounty.id))
    force_authenticate(request, user)
    view = FirstOrNextBountyView.as_view()
    view(request, bounty.id)

    _, created = bounty.get_or_create_user_bounty(setup_user)
    assert not created

    # Finish bounty and check status
    item = None
    for i in range(5):
        item = task.next_item(user, item)
        add_annotation(item, user, "A")

    request = factory.get('/api/v1/bounty/{}/status'.format(bounty.id))
    force_authenticate(request, user)
    view = BountyStatusView.as_view()
    response = view(request, bounty.id)
    assert response.data['status'] == BountyStatus.FINISHED
    assert response.data['reward'] is not None

    # Start next bounty
    prev_user_bounty_id = response.data['id']

    request = factory.get('/api/v1/bounty/{}/bounty_next'.format(bounty.id))
    force_authenticate(request, user)
    view = FirstOrNextBountyView.as_view()
    response = view(request, bounty.id)

    assert response.data['status'] == BountyStatus.NEW
    assert prev_user_bounty_id != response.data['id']
    assert len(response.data['rewards_list']) == 1
    assert response.data['reward'] is None
