import pytest
from rest_framework.test import APIRequestFactory
from tasks.api.views.mission import (
    MissionList, MissionDetail
)


@pytest.mark.django_db
def test_mission_list(setup_task):
    factory = APIRequestFactory()

    # Mission list
    request = factory.get('/api/v1/missions')
    view = MissionList.as_view()
    response = view(request)
    assert response.status_code == 200
    assert response.data == [
        {'id': 1, 'name': 'Test mission'},
        {'id': 2, 'name': 'Test mission other'}
    ]

    # Mission detail, mission found
    mission_id = 1
    request = factory.get('/api/v1/missions/{0}'.format(mission_id))
    view = MissionDetail.as_view()
    response = view(request, mission_id)
    assert response.status_code == 200
    assert response.data == {'id': 1, 'name': 'Test mission'}

    # Mission detail, mission not found
    mission_id = 3
    request = factory.get('/api/v1/missions/{0}'.format(mission_id))
    view = MissionDetail.as_view()
    response = view(request, mission_id)
    assert response.status_code == 404
    assert response.data["detail"].code == "not_found"
