import json

import pytest
from django.db.models import Q
from django.test import Client

from modules.achievements.models import ItemDoneAchievement, UserAchievement, Achievement
from modules.achievements.tests.conftest import compare_without_fields
from tasks.models import Item
from users.models import EndWorker


@pytest.mark.django_db
def test_achievements_list_view(user1, achievements):
    client = Client()
    client.force_login(user1)

    # all achievements list
    response = client.get('/api/v1/achievements/')
    user_achievements = UserAchievement.get_user_achievements(user1)
    expected_data = [
        {
            'order': achievement.order,
            'status': achievement.status,
            'value': achievement.value,
            'target': achievement.target,
            'progress': achievement.progress,
            'exp': achievement.exp,
            'metadata': achievement.achievement.metadata
        } for achievement in user_achievements
    ]

    assert len(expected_data) == len(response.data)
    for received, expected in zip(response.data, expected_data):
        assert compare_without_fields(received, expected, excluded_fields=['id', 'updated'])

    # mission achievements list
    mission_id = 1
    user_achievements = UserAchievement.get_user_achievements(
        user1).filter(Q(achievement__mission_id=mission_id) | Q(achievement__task__mission_id=mission_id))

    response = client.get('/api/v1/achievements/mission/1/')
    expected_data = [
        {
            'order': achievement.order,
            'status': achievement.status,
            'value': achievement.value,
            'target': achievement.target,
            'progress': achievement.progress,
            'exp': achievement.exp,
            'metadata': achievement.achievement.metadata
        } for achievement in user_achievements
    ]

    assert len(expected_data) == len(response.data)

    for received, expected in zip(response.data, expected_data):
        assert compare_without_fields(received, expected, excluded_fields=['id', 'updated'])

    # task achievements list
    task_id = 1
    user_achievements = UserAchievement.get_user_achievements(user1).filter(achievement__task_id=task_id)

    response = client.get('/api/v1/achievements/task/1/')
    expected_data = [
        {
            'order': achievement.order,
            'status': achievement.status,
            'value': achievement.value,
            'target': achievement.target,
            'progress': achievement.progress,
            'exp': achievement.exp,
            'metadata': achievement.achievement.metadata
        } for achievement in user_achievements
    ]

    assert len(expected_data) == len(response.data)

    for received, expected in zip(response.data, expected_data):
        assert compare_without_fields(received, expected, excluded_fields=['id', 'updated'])


@pytest.mark.django_db
def test_unclosed_achievements_list(user1, achievements):
    client = Client()
    client.force_login(user1)

    achievement = ItemDoneAchievement.objects.first()
    UserAchievement.objects.create(user=user1, achievement=achievement)

    assert user1.exp == 0

    response = client.get('/api/v1/achievements/unclosed/')
    assert len(response.data) == 0

    # annotate one item
    item = Item.objects.first()
    payload = {
        'data': json.dumps({'output': '1'}),
    }
    client.post('/api/v1/items/{0}/annotation/'.format(item.id), payload)

    # achievement done
    response = client.get('/api/v1/achievements/unclosed/')

    expected_data = [
        {
            'id': achievement.id,
            'order': achievement.order,
            'status': 'CLOSED',
            'value': 1.0,
            'target': 1.0,
            'progress': 1.0,
            'exp': 10,
            'metadata': {}
        },
    ]

    assert len(response.data) == len(expected_data)
    for received, expected in zip(response.data, expected_data):
        assert compare_without_fields(received, expected, excluded_fields=['id', 'updated'])

    user1 = EndWorker.objects.get(id=user1.id)
    assert user1.exp == achievement.exp

    # achievement closed
    response = client.get('/api/v1/achievements/unclosed/')
    assert len(response.data) == 0
