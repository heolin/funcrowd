import pytest
from rest_framework.test import APIRequestFactory, force_authenticate

from modules.statistics.api.views import MissionStatsView
from tasks.models import Mission


@pytest.mark.django_db
def test_mission_stats_view_tasks_data(setup_user, setup_tasks):
    factory = APIRequestFactory()

    mission = Mission.objects.first()

    # Mission stats
    request = factory.get('/api/v1/stats/missions/{}'.format(mission.id))
    force_authenticate(request, setup_user)
    view = MissionStatsView.as_view()
    response = view(request, mission.id)

    assert response.status_code == 200
    assert response.data == {
        'mission_id': mission.id,
        'total_documents': 6,
        'total_finished_documents': 3,
        'total_tasks': 3,
        'total_users': 0
    }
