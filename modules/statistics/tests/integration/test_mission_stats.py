import pytest
from rest_framework.test import APIRequestFactory

from modules.statistics.api.views import MissionStatsView
from tasks.models import Mission


@pytest.mark.django_db
def test_mission_stats_view_tasks_data(setup_tasks_annotations):
    factory = APIRequestFactory()

    mission = Mission.objects.get(name="Test mission 4")

    # Mission stats
    request = factory.get('/api/v1/stats/missions/{}'.format(mission.id))
    view = MissionStatsView.as_view()
    response = view(request, mission.id)

    assert response.status_code == 200
    assert response.data == {
        'mission_id': mission.id,
        'total_documents': 10,
        'total_finished_documents': 10,
        'total_finished_items': 10,
        'total_tasks': 1,
        'total_users': 14,
        'agreement_mean': 0.814285714285714
    }
