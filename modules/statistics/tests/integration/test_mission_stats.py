import pytest
from django.test import Client

from tasks.models import Mission


@pytest.mark.django_db
def test_mission_stats_view_tasks_data(tasks_annotations):
    client = Client()

    mission = Mission.objects.get(name="Test mission 4")

    # Mission stats
    response = client.get('/api/v1/stats/missions/{}/'.format(mission.id))
    assert response.status_code == 200
    assert response.data == {
        'mission_id': mission.id,
        'total_documents': 10,
        'total_finished_documents': 10,
        'total_finished_items': 10,
        'total_tasks': 1,
        'total_active_users': 14,
        'total_annotations': 140,
        'agreement_mean': 0.814285714285714
    }
