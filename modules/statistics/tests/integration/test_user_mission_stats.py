import pytest
from django.test import Client

from tasks.models import Mission
from users.models import EndWorker


@pytest.mark.django_db
def test_user_mission_stats_view_tasks_data(tasks_annotations):
    client = Client()

    mission = Mission.objects.first()
    user1 = EndWorker.objects.get(email="user_1@mail.com")

    # User mission stats
    response = client.get('/api/v1/stats/users/{}/missions/{}/'.format(user1.id, mission.id))
    assert response.status_code == 200
    assert response.data == {
        'user_id': user1.id,
        'mission_id': mission.id,
        'annotated_documents': 10,
        'high_agreement_count': 8,
        'agreement_ranking_position': 7,
        'agreement_ranking_percentage': 0.5,
        'high_agreement_percentage': 0.8
    }
