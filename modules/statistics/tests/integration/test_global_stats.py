import pytest
from django.test import Client


@pytest.mark.django_db
def test_global_stats_view_tasks_data(user1, tasks):
    client = Client()

    # Global stats
    response = client.get('/api/v1/stats/')
    assert response.status_code == 200
    assert response.data == {
        'total_documents': 13,
        'total_finished_documents': 6,
        'total_finished_items': 0,
        'total_missions': 3,
        'total_tasks': 6,
        'total_active_users': 0,
        'total_annotations': 0,
        'total_users': 1
    }


@pytest.mark.django_db
def test_global_stats_view_tasks_data_annotations(user1, tasks_annotations):
    client = Client()

    # Global stats
    response = client.get('/api/v1/stats/')
    assert response.status_code == 200
    assert response.data == {
        'total_documents': 10,
        'total_finished_documents': 10,
        'total_finished_items': 10,
        'total_missions': 1,
        'total_tasks': 1,
        'total_active_users': 14,
        'total_annotations': 140,
        'total_users': 15
    }
