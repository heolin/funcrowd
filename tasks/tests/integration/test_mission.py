import pytest
from django.test import Client


@pytest.mark.django_db
def test_mission_list(task, user1):
    client = Client()
    client.force_login(user1)

    # Mission list
    response = client.get('/api/v1/missions/')
    assert response.status_code == 200
    assert response.data == [
        {'id': 1, 'name': 'Test mission', 'description': '', 'instruction': '',
         'tasks_count': 1, 'achievements_count': 0, 'metadata': {}, 'total_exp': 10},
        {'id': 2, 'name': 'Test mission other', 'description': '', 'instruction': '',
         'tasks_count': None, 'achievements_count': 0, 'metadata': {}},
    ]

    # Mission detail, mission found
    mission_id = 1
    response = client.get('/api/v1/missions/{0}/'.format(mission_id))
    assert response.status_code == 200
    assert response.data == {'id': 1, 'name': 'Test mission', 'description': '', 'instruction': '',
                             'tasks_count': 1, 'achievements_count': 0, 'metadata': {}, 'total_exp': None}

    # Mission detail, mission not found
    mission_id = 3
    response = client.get('/api/v1/missions/{0}/'.format(mission_id))
    assert response.status_code == 404
    assert response.data["detail"].code == "not_found"


@pytest.mark.django_db
def test_mission_list(task_with_items, user1):
    client = Client()
    client.force_login(user1)

    # Mission detail, mission found
    mission_id = 1
    response = client.get('/api/v1/missions/{0}/'.format(mission_id))
    assert response.status_code == 200
    assert response.data == {'id': 1, 'name': 'Test mission', 'description': '', 'instruction': '',
                             'tasks_count': 1, 'achievements_count': 0, 'metadata': {}, 'total_exp': 10}
