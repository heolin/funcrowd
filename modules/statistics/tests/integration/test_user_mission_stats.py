import pytest
from rest_framework.test import APIRequestFactory, force_authenticate

from modules.statistics.api.views import UserMissionStatsView
from tasks.models import Mission
from users.models import EndWorker


@pytest.mark.django_db
def test_user_mission_stats_view_tasks_data(setup_tasks_annotations):
    factory = APIRequestFactory()

    mission = Mission.objects.first()
    user = EndWorker.objects.get(username="user1")

    # User mission stats
    request = factory.get('/api/v1/stats/users/{}/missions/{}'.format(user.id, mission.id))
    view = UserMissionStatsView.as_view()
    response = view(request, user.id, mission.id)

    assert response.status_code == 200
    assert response.data == {
        'user_id': user.id,
        'mission_id': mission.id,
        'annotated_documents': 10,
        'high_agreement_count': 8,
        'agreement_ranking_position': 7,
        'agreement_ranking_percentage': 0.5
    }
