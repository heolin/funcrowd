import pytest
from rest_framework.test import APIRequestFactory, force_authenticate

from modules.statistics.api.views import UserStatsView


@pytest.mark.django_db
def test_user_mission_stats_view_tasks_data(setup_user, setup_tasks_annotations):
    factory = APIRequestFactory()

    # User mission stats
    request = factory.get('/api/v1/stats/users/{}'.format(setup_user.id))
    view = UserStatsView.as_view()
    force_authenticate(request, user=setup_user)
    response = view(request, setup_user.id)

    assert response.status_code == 200
    assert response.data == {
        'user_id': setup_user.id,
        'annotated_documents': 10,
        'high_agreement_count': 0,
        'agreement_ranking_position': 0,
        'agreement_ranking_percentage': 0.0
    }
