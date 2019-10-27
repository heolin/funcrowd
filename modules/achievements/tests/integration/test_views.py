import json

import pytest
from rest_framework.test import APIRequestFactory, force_authenticate

from modules.achievements.api.views.user_achievement import AchievementsList, MissionAchievementsList, \
    TaskAchievementsList, UnclosedAchievementsList
from modules.achievements.models import ItemDoneAchievement, UserAchievement, Achievement
from modules.achievements.tests.conftest import compare_without_fields
from tasks.api.views.annotation import AnnotationDetail
from tasks.models import Item


@pytest.mark.django_db
def test_achievements_list_view(setup_user1, setup_achievements, setup_wrong_progress_achievement):
    factory = APIRequestFactory()

    user = setup_user1

    # all achievements list
    achievements = Achievement.objects.all()

    request = factory.get('/api/v1/achievements')
    force_authenticate(request, user)
    view = AchievementsList.as_view()
    response = view(request)
    expected_data = [
        {
            'order': 0,
            'status': 'NEW',
            'value': 0.0,
            'target': 1.0,
            'progress': 0.0,
            'metadata': {}
        },
        {
            'order': 1,
            'status': 'NEW',
            'value': 0.0,
            'target': 1.0,
            'progress': 0.0,
            'metadata': {}
        },
        {
            'order': 2,
            'status': 'NEW',
            'value': 0.0,
            'target': 2.0,
            'progress': 0.0,
            'metadata': {}
        },
        {
            'order': 3,
            'status': 'NEW',
            'value': 0.0,
            'target': 1.0,
            'progress': 0.0,
            'metadata': {}
        },
        {
            'order': 4,
            'status': 'NEW',
            'value': 0.0,
            'target': 1.0,
            'progress': 0.0,
            'metadata': {}
        },
        {
            'order': 5,
            'status': 'NEW',
            'value': 0.0,
            'target': 1.0,
            'progress': 0.0,
            'metadata': {}
        },
        {
            'order': 6,
            'status': 'NEW',
            'value': 0.0,
            'target': 1.0,
            'progress': 0.0,
            'metadata': {}
        },
    ]
    for received, expected in zip(response.data, expected_data):
        assert compare_without_fields(received, expected, excluded_fields=['id', 'updated'])

    # mission achievements list
    mission_id = 1
    achievements = Achievement.objects.filter(mission_id=mission_id)

    request = factory.get('/api/v1/achievements/mission/1')
    force_authenticate(request, user)
    view = MissionAchievementsList.as_view()
    response = view(request, mission_id)
    expected_data = [
        {
            'id': achievements[0].id,
            'order': 2,
            'status': 'NEW',
            'value': 0.0,
            'target': 2.0,
            'progress': 0.0,
            'metadata': {}
        },
        {
            'id': achievements[1].id,
            'order': 6,
            'status': 'NEW',
            'value': 0.0,
            'target': 1.0,
            'progress': 0.0,
            'metadata': {}
        },
    ]
    for received, expected in zip(response.data, expected_data):
        assert compare_without_fields(received, expected, excluded_fields=['id', 'updated'])

    # task achievements list
    task_id = 1
    achievements = Achievement.objects.filter(task_id=task_id)

    request = factory.get('/api/v1/achievements/task/1')
    force_authenticate(request, user)
    view = TaskAchievementsList.as_view()
    response = view(request, task_id)
    expected_data = [
        {
            'id': achievements[0].id,
            'order': 5,
            'status': 'NEW',
            'value': 0.0,
            'target': 1.0,
            'progress': 0.0,
            'metadata': {}
        },
    ]
    for received, expected in zip(response.data, expected_data):
        assert compare_without_fields(received, expected, excluded_fields=['id', 'updated'])


@pytest.mark.django_db
def test_unclosed_achievements_list(setup_user1, setup_achievements):
    factory = APIRequestFactory()

    user = setup_user1

    achievement = ItemDoneAchievement.objects.first()
    UserAchievement.objects.create(user=user, achievement=achievement)

    request = factory.get('/api/v1/achievements/unclosed')
    force_authenticate(request, user)
    view = UnclosedAchievementsList.as_view()
    response = view(request)
    assert len(response.data) == 0

    # annotate one item
    item = Item.objects.first()
    payload = {
        'data': json.dumps({'output': '1'}),
    }
    request = factory.post('/api/v1/items/{0}/annotation'.format(item.id), payload)
    force_authenticate(request, user)
    view = AnnotationDetail.as_view()
    view(request, item.id)

    # achievement done
    request = factory.get('/api/v1/achievements/unclosed')
    force_authenticate(request, user)
    view = UnclosedAchievementsList.as_view()
    response = view(request)

    expected_data = [
        {
            'id': achievement.id,
            'order': achievement.order,
            'status': 'FINISHED',
            'value': 1.0,
            'target': 1.0,
            'progress': 1.0,
            'metadata': {}
        },
    ]
    for received, expected in zip(response.data, expected_data):
        assert compare_without_fields(received, expected, excluded_fields=['id', 'updated'])

    user_achievement = UserAchievement.objects.get(user=user, achievement=achievement)
    user_achievement.close()

    # achievement closed
    request = factory.get('/api/v1/achievements/unclosed')
    force_authenticate(request, user)
    view = UnclosedAchievementsList.as_view()
    response = view(request)

    assert len(response.data) == 0
