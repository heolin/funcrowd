import pytest
from django.test import Client

from modules.achievements.models import LoginCountAchievement, UserAchievement
from users.models import EndWorker


@pytest.mark.django_db
def test_login_count_integration(user1, achievements):
    achievement = LoginCountAchievement.objects.first()
    user_achievement = UserAchievement.objects.create(user=user1, achievement=achievement)
    user_achievement.update()
    assert user_achievement.value == 0

    client = Client()
    payload = {
        "email": "user1@mail.com",
        "password": "password",
    }
    response = client.post('/api/v1/users/login', payload)
    assert response.status_code == 200

    user_achievement = UserAchievement.objects.get(user=user1, achievement=achievement)
    assert user_achievement.value == 1



