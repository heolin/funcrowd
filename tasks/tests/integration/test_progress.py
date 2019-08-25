import pytest
from rest_framework.test import APIRequestFactory, force_authenticate
from tasks.api.views.mission_progress import UserMissionProgressList, UserMissionProgressDetail
from tasks.api.views.task_progress import UserTaskProgressList, UserTaskProgressDetail


@pytest.mark.django_db
def test_task_progress(setup_task, setup_user):
    factory = APIRequestFactory()

    # Tasks progress list list
    mission_id = 1
    request = factory.get('/api/v1/missions/{0}/tasks/progress'.format(mission_id))
    force_authenticate(request, setup_user)
    view = UserTaskProgressList.as_view()
    response = view(request, mission_id)
    assert response.status_code == 200
    assert response.data == [
        {'id': 1, 'task': 1, 'items_done': 0, 'items_count': 0, 'progress': None}
    ]

    # Task progress detail, task found
    task_id = 1
    request = factory.get('/api/v1/tasks/{0}/progress'.format(task_id))
    force_authenticate(request, setup_user)
    view = UserTaskProgressDetail.as_view()
    response = view(request, task_id)
    assert response.status_code == 200
    assert response.data == {'id': 1, 'task': 1, 'items_done': 0, 'items_count': 0, 'progress': None}

    # Task progress detail, task not found
    task_id = 3
    request = factory.get('/api/v1/missions/{0}/progress'.format(task_id))
    force_authenticate(request, setup_user)
    view = UserTaskProgressDetail.as_view()
    response = view(request, task_id)
    assert response.status_code == 404
    assert response.data["detail"].code == "not_found"


@pytest.mark.django_db
def test_mission_progress(setup_task, setup_user):
    factory = APIRequestFactory()

    # Mission list
    request = factory.get('/api/v1/missions/progress')
    force_authenticate(request, setup_user)
    view = UserMissionProgressList.as_view()
    response = view(request)
    assert response.status_code == 200
    assert response.data == [
        {'id': 1, 'mission': 1, 'tasks_done': 0, 'tasks_count': 1, 'progress': 0.0},
        {'id': 2, 'mission': 2, 'tasks_done': 0, 'tasks_count': 0, 'progress': None}
    ]

    # Mission detail, mission found
    mission_id = 1
    request = factory.get('/api/v1/missions/{0}/progress'.format(mission_id))
    force_authenticate(request, setup_user)
    view = UserMissionProgressDetail.as_view()
    response = view(request, mission_id)
    assert response.status_code == 200
    assert response.data == {'id': 1, 'mission': 1, 'tasks_done': 0, 'tasks_count': 1, 'progress': 0.0}

    # Mission detail, mission not found
    mission_id = 3
    request = factory.get('/api/v1/missions/{0}/progress'.format(mission_id))
    force_authenticate(request, setup_user)
    view = UserMissionProgressDetail.as_view()
    response = view(request, mission_id)
    assert response.status_code == 404
    assert response.data["detail"].code == "not_found"
