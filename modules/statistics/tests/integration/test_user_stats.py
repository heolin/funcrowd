import pytest
from rest_framework.test import APIRequestFactory, force_authenticate

from modules.statistics.api.views import UserStatsView
from users.models import EndWorker


@pytest.mark.django_db
def test_user_mission_stats_view_tasks_data(setup_tasks_annotations):
    factory = APIRequestFactory()
    user = EndWorker.objects.get(username="user1")

    # User mission stats
    request = factory.get('/api/v1/stats/users/{}'.format(user.id))
    view = UserStatsView.as_view()
    response = view(request, user.id)

    assert response.status_code == 200
    assert response.data == {
        'user_id': user.id,
        'annotated_documents': 10,
        'high_agreement_count': 8,
        'high_agreement_percentage': 0.8,
        'agreement_ranking_position': 7,
        'agreement_ranking_percentage': 0.5,
        'annotated_missions': 1
    }
