from unittest.mock import MagicMock

import pytest

from modules.achievements.consts import Status
from modules.achievements.models import UserAchievement, Achievement


@pytest.mark.django_db
def test_creating_achievements(user1, achievements):
    assert UserAchievement.objects.filter(user=user1).count() == 0

    user_achievements = UserAchievement.get_user_achievements(user1)
    assert user_achievements.count() == Achievement.objects.count()
    assert UserAchievement.objects.filter(user=user1).count() == Achievement.objects.count()


@pytest.mark.django_db
def test_creating_missing_achievements(user1, achievements):
    assert UserAchievement.objects.filter(user=user1).count() == 0

    achievement = Achievement.objects.first()
    UserAchievement.objects.create(user=user1, achievement=achievement)
    assert UserAchievement.objects.filter(user=user1).count() == 1

    assert UserAchievement.get_user_achievements(user1).count() == Achievement.objects.count()


@pytest.mark.django_db
def test_update_state(user1, achievements):
    achievement = Achievement.objects.create(target=2)
    user_achievement = UserAchievement.objects.create(user=user1, achievement=achievement)
    assert user_achievement.status == Status.NEW

    user_achievement.achievement.on_close = MagicMock()

    user_achievement.value = 1
    user_achievement.update()
    assert user_achievement.status == Status.IN_PROGRESS

    user_achievement.value = achievement.target
    user_achievement.update()
    assert user_achievement.status == Status.FINISHED

    user_achievement.close()
    assert user_achievement.status == Status.CLOSED

    user_achievement.achievement.on_close.assert_called_with(user_achievement)
