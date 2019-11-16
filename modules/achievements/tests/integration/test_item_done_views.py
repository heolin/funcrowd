import json

import pytest
from django.test import Client
from modules.achievements.models import UserAchievement, ItemDoneAchievement
from tasks.models import Item


@pytest.mark.django_db
def test_item_done_integration(user1, achievements):
    client = Client()
    client.force_login(user1)

    achievement = ItemDoneAchievement.objects.first()
    user_achievement = UserAchievement.objects.create(user=user1, achievement=achievement)
    user_achievement.update()
    assert user_achievement.value == 0

    item = Item.objects.first()
    payload = {
        'data': json.dumps({'output': '1'}),
    }
    client.post('/api/v1/items/{0}/annotation'.format(item.id), payload)

    user_achievement = UserAchievement.objects.get(user=user1, achievement=achievement)
    assert user_achievement.value == 1
