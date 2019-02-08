import pytest
from rest_framework.test import APIRequestFactory, force_authenticate

from modules.statistics.api.views import GlobalStatsView


@pytest.mark.django_db
def test_global_stats_view_tasks_data(setup_user, setup_tasks):
    factory = APIRequestFactory()

    # Global stats
    request = factory.get('/api/v1/stats')
    force_authenticate(request, setup_user)
    view = GlobalStatsView.as_view()
    response = view(request)

    assert response.status_code == 200
    assert response.data == {
        'total_documents': 13,
        'total_finished_documents': 6,
        'total_missions': 3,
        'total_tasks': 6,
        'total_users': 1
    }
