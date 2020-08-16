import pytest
from django.test import Client

from tasks.models import UserMissionProgress, Task, Mission


@pytest.mark.django_db
def test_task_progress(task, user1):
    task = Task.objects.get(order=1)

    client = Client()
    client.force_login(user1)

    # Tasks progress list list
    ut = user1.get_task_progress(task)
    response = client.get('/api/v1/missions/{0}/tasks/progress/'.format(task.mission.id))
    assert response.status_code == 200
    assert response.data == [
        {'id': ut.id, 'task': ut.task.id, 'items_done': 0, 'items_count': 0,
         'progress': None, 'status': "UNLOCKED", 'max_score':  None, 'score': None}
    ]

    # Task progress detail, task found.
    response = client.get('/api/v1/tasks/{0}/progress/'.format(task.id))
    assert response.status_code == 200
    assert response.data == {'id': ut.id, 'task': ut.task.id, 'items_done': 0,
                             'items_count': 0, 'progress': None, "status": "UNLOCKED",
                             'max_score': None, 'score': None}

    # Task progress detail, task not found
    task_id = 3
    response = client.get('/api/v1/tasks/{0}/progress/'.format(task_id))
    assert response.status_code == 404
    assert response.data["detail"].code == "not_found"


@pytest.mark.django_db
def test_mission_progress(task, user1):
    client = Client()
    client.force_login(user1)

    # Mission list
    response = client.get('/api/v1/missions/progress/')
    assert response.status_code == 200
    assert response.data == [
        {'id': u.id, 'mission': u.mission.id, 'tasks_done': 0,
         'tasks_count': u.mission.tasks_count, 'progress': u.progress, 'status': 'UNLOCKED'}
        for u in UserMissionProgress.objects.filter(user=user1)
    ]

    # Mission detail, mission found
    mission_id = 1
    um = UserMissionProgress.objects.get(user=user1, mission_id=mission_id)

    response = client.get('/api/v1/missions/{0}/progress/'.format(mission_id))
    assert response.status_code == 200
    assert response.data == {'id': um.id, 'mission': mission_id, 'tasks_done': 0,
                             'tasks_count': 1, 'progress': 0.0, 'status': 'UNLOCKED'}

    # Mission detail, mission not found
    mission_id = 3
    response = client.get('/api/v1/missions/{0}/progress/'.format(mission_id))
    assert response.status_code == 404
    assert response.data["detail"].code == "not_found"


@pytest.mark.django_db
def test_mission_progress(task, user1, user2):
    client = Client()
    client.force_login(user1)

    mission = Mission.objects.first()

    # Adding bonus exp - empty payload
    payload = {}
    response = client.post('/api/v1/missions/{0}/bonus_exp/'.format(mission.id), payload)
    assert response.status_code == 400

    # Adding bonus exp - missing mission
    payload = {}
    response = client.post('/api/v1/missions/{0}/bonus_exp/'.format(9), payload)
    assert response.status_code == 404

    # Adding bonus exp - correct value
    payload = {"bonus_exp": 10}
    response = client.post('/api/v1/missions/{0}/bonus_exp/'.format(mission.id), payload)
    assert response.status_code == 204

    ump = user1.get_mission_progress(mission)
    assert ump.bonus_exp == 10

    # Adding bonus exp - to other user
    payload = {"bonus_exp": 10, 'user_id': user2.id}
    response = client.post('/api/v1/missions/{0}/bonus_exp/'.format(mission.id), payload)
    assert response.status_code == 204

    ump = user2.get_mission_progress(mission)
    assert ump.bonus_exp == 10
