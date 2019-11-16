import pytest

from modules.achievements.consts import Status
from modules.achievements.models import UserAchievement, Achievement, ItemDoneAchievement, LoginCountAchievement


@pytest.mark.django_db
def test_login_count_logic(user1, achievements):
    achievement = LoginCountAchievement.objects.first()
    assert achievement

    user_achievement = UserAchievement.objects.create(user=user1, achievement=achievement)
    user_achievement.update()
    assert user_achievement.value == 0

    user1.login_count = 1
    user1.save()

    user_achievement.update()
    assert user_achievement.value == 1
    assert user_achievement.status == Status.FINISHED
