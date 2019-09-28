import pytest

from modules.achievements.consts import Status
from modules.achievements.models import UserAchievement, Achievement, ItemDoneAchievement, LoginCountAchievement


@pytest.mark.django_db
def test_login_count_logic(setup_user1, setup_achievements):
    user = setup_user1

    achievement = LoginCountAchievement.objects.first()
    assert achievement

    user_achievement = UserAchievement.objects.create(user=user, achievement=achievement)
    user_achievement.update()
    assert user_achievement.value == 0

    user.login_count = 1
    user.save()

    user_achievement.update()
    assert user_achievement.value == 1
    assert user_achievement.status == Status.FINISHED
