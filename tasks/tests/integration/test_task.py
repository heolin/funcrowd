import pytest
from django.test import Client


@pytest.mark.django_db
def test_task_list(task, user1):
    client = Client()
    client.force_login(user1)

    # Task list
    mission_id = 1
    response = client.get('/api/v1/missions/{0}/tasks'.format(mission_id))
    assert response.status_code == 200
    assert response.data == [
        {'id': 1, 'name': 'Add two digits', 'description': '',
         'instruction': '', 'keywords': '', 'metadata': {}, 'total_exp': None}
    ]

    # Task empty list
    mission_id = 2
    response = client.get('/api/v1/missions/{0}/tasks'.format(mission_id))
    assert response.status_code == 200
    assert response.data == []

    response = client.get('/api/v1/missions/{0}/tasks'.format(100))
    assert response.status_code == 404
    assert response.data["detail"].code == "not_found"


@pytest.mark.django_db
def test_task_details(task, user1):
    client = Client()
    client.force_login(user1)

    # Task details
    task_id = 1
    response = client.get('/api/v1/tasks/{0}'.format(task_id))
    assert response.status_code == 200
    assert response.data == {
        'id': 1, 'name': 'Add two digits', 'description': '',
        'instruction': '', 'keywords': '', 'metadata': {}, 'total_exp': None
    }

    # Task details, task not found
    response = client.get('/api/v1//tasks/{0}'.format(100))
    assert response.status_code == 404
    assert response.data["detail"].code == "not_found"


@pytest.mark.django_db
def test_task_details(task_with_items, user1):
    client = Client()
    client.force_login(user1)

    # Task details
    task_id = 1
    response = client.get('/api/v1/tasks/{0}'.format(task_id))
    assert response.status_code == 200
    assert response.data == {
        'id': 1, 'name': 'Add two digits', 'description': '',
        'instruction': '', 'keywords': '', 'metadata': {}, 'total_exp': 10
    }
