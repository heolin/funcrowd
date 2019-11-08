import pytest
from rest_framework.test import APIRequestFactory, force_authenticate
from tasks.api.views.mission_progress import UserMissionProgressList, UserMissionProgressDetail
from tasks.api.views.task_progress import UserTaskProgressList, UserTaskProgressDetail
from tasks.models import UserMissionProgress, UserTaskProgress


@pytest.mark.django_db
def test_task_progress(setup_task, setup_user):
    factory = APIRequestFactory()

    # Tasks progress list list
    mission_id = 1
    task_id = 1
    request = factory.get('/api/v1/missions/{0}/tasks/progress'.format(mission_id))
    force_authenticate(request, setup_user)
    view = UserTaskProgressList.as_view()
    response = view(request, mission_id)

    ut = UserTaskProgress.objects.get(user=setup_user, task_id=task_id)

    assert response.status_code == 200
    assert response.data == [
        {'id': ut.id, 'task': ut.task.id, 'items_done': 0, 'items_count': 0, 'progress': None}
    ]

    # Task progress detail, task found
    request = factory.get('/api/v1/tasks/{0}/progress'.format(task_id))
    force_authenticate(request, setup_user)
    view = UserTaskProgressDetail.as_view()
    response = view(request, task_id)
    assert response.status_code == 200
    assert response.data == {'id': ut.id, 'task': ut.task.id, 'items_done': 0,
                             'items_count': 0, 'progress': None}

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
        {'id': u.id, 'mission': u.mission.id, 'tasks_done': 0,
         'tasks_count': u.mission.tasks_count, 'progress': u.progress, 'status': 'UNLOCKED'}
        for u in UserMissionProgress.objects.filter(user=setup_user)
    ]

    # Mission detail, mission found
    mission_id = 1
    request = factory.get('/api/v1/missions/{0}/progress'.format(mission_id))
    force_authenticate(request, setup_user)
    view = UserMissionProgressDetail.as_view()
    response = view(request, mission_id)

    um = UserMissionProgress.objects.get(user=setup_user, mission_id=mission_id)
    assert response.status_code == 200
    assert response.data == {'id': um.id, 'mission': mission_id, 'tasks_done': 0,
                             'tasks_count': 1, 'progress': 0.0, 'status': 'UNLOCKED'}

    # Mission detail, mission not found
    mission_id = 3
    request = factory.get('/api/v1/missions/{0}/progress'.format(mission_id))
    force_authenticate(request, setup_user)
    view = UserMissionProgressDetail.as_view()
    response = view(request, mission_id)
    assert response.status_code == 404
    assert response.data["detail"].code == "not_found"
