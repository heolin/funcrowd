import json

import pytest
from rest_framework.test import APIRequestFactory, force_authenticate

from modules.achievements.models import UserAchievement, ItemDoneAchievement
from tasks.api.views.annotation import AnnotationDetail
from tasks.models import Item


@pytest.mark.django_db
def test_item_done_integration(setup_user1, setup_achievements):
    factory = APIRequestFactory()

    user = setup_user1
    achievement = ItemDoneAchievement.objects.first()
    user_achievement = UserAchievement.objects.create(user=user, achievement=achievement)
    user_achievement.update()
    assert user_achievement.value == 0

    item = Item.objects.first()
    payload = {
        'data': json.dumps({'output': '1'}),
    }
    request = factory.post('/api/v1/items/{0}/annotation'.format(item.id), payload)
    force_authenticate(request, user)
    view = AnnotationDetail.as_view()
    view(request, item.id)

    user_achievement = UserAchievement.objects.get(user=user, achievement=achievement)
    assert user_achievement.value == 1
