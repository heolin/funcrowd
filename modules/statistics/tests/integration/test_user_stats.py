import pytest
from django.test import Client

from users.models import EndWorker


@pytest.mark.django_db
def test_user_mission_stats_view_tasks_data(tasks_annotations):
    user1 = EndWorker.objects.get(email="user_1@mail.com")

    client = Client()

    # User mission stats
    response = client.get('/api/v1/stats/users/{}/'.format(user1.id))
    assert response.status_code == 200
    assert response.data == {
        'user_id': user1.id,
        'annotated_documents': 10,
        'high_agreement_count': 8,
        'high_agreement_percentage': 0.8,
        'agreement_ranking_position': 7,
        'agreement_ranking_percentage': 0.5,
        'annotated_missions': 1
    }
