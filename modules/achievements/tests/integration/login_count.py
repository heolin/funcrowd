import pytest
from django.test import Client

from modules.achievements.models import LoginCountAchievement, UserAchievement
from users.models import EndWorker


@pytest.mark.django_db
def test_login_count_integration(setup_user1, setup_achievements):
    user = setup_user1
    achievement = LoginCountAchievement.objects.first()
    user_achievement = UserAchievement.objects.create(user=user, achievement=achievement)
    user_achievement.update()
    assert user_achievement.value == 0

    client = Client()
    payload = {
        "username": "user",
        "password": "password",
    }
    response = client.post('/api/v1/users/login', payload)
    assert response.status_code == 200

    # get data of current user
    response = client.get('/api/v1/users/current')
    end_worker = EndWorker.objects.get(username="user")
    assert response.status_code == 200

    user_achievement = UserAchievement.objects.get(user=user, achievement=achievement)
    assert user_achievement.value == 1



