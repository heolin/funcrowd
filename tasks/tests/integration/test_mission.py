import pytest
from rest_framework.test import APIRequestFactory, force_authenticate
from tasks.api.views.mission import (
    MissionList, MissionDetail
)


@pytest.mark.django_db
def test_mission_list(setup_task, setup_user):
    factory = APIRequestFactory()

    # Mission list
    request = factory.get('/api/v1/missions')
    force_authenticate(request, setup_user)
    view = MissionList.as_view()
    response = view(request)
    assert response.status_code == 200
    assert response.data == [
        {'id': 1, 'name': 'Test mission', 'description': '', 'tasks_count': 1, 'achievements_count': 0, 'metadata': {}},
        {'id': 2, 'name': 'Test mission other', 'description': '', 'tasks_count': 0, 'achievements_count': 0, 'metadata': {}},
    ]

    # Mission detail, mission found
    mission_id = 1
    request = factory.get('/api/v1/missions/{0}'.format(mission_id))
    force_authenticate(request, setup_user)
    view = MissionDetail.as_view()
    response = view(request, mission_id)
    assert response.status_code == 200
    assert response.data == {'id': 1, 'name': 'Test mission', 'description': '', 'tasks_count': 1, 'achievements_count': 0, 'metadata': {}}

    # Mission detail, mission not found
    mission_id = 3
    request = factory.get('/api/v1/missions/{0}'.format(mission_id))
    force_authenticate(request, setup_user)
    view = MissionDetail.as_view()
    response = view(request, mission_id)
    assert response.status_code == 404
    assert response.data["detail"].code == "not_found"
