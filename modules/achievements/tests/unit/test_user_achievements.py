import pytest

from modules.achievements.consts import Status
from modules.achievements.models import UserAchievement, Achievement


@pytest.mark.django_db
def test_creating_achievements(setup_user1, setup_achievements):
    user = setup_user1

    assert UserAchievement.objects.filter(user=user).count() == 0

    user_achievements = UserAchievement.get_user_achievements(user)
    assert user_achievements.count() == 4
    assert UserAchievement.objects.filter(user=user).count() == Achievement.objects.count()


@pytest.mark.django_db
def test_creating_missing_achievements(setup_user1, setup_achievements):
    user = setup_user1

    assert UserAchievement.objects.filter(user=user).count() == 0

    achievement = Achievement.objects.first()
    UserAchievement.objects.create(user=user, achievement=achievement)
    assert UserAchievement.objects.filter(user=user).count() == 1

    assert UserAchievement.get_user_achievements(user).count() == Achievement.objects.count()


@pytest.mark.django_db
def test_update_state(setup_user1, setup_achievements):
    user = setup_user1

    achievement = Achievement.objects.create(target=2)
    user_achievement = UserAchievement.objects.create(user=user, achievement=achievement)
    assert user_achievement.status == Status.NEW

    user_achievement.value = 1
    user_achievement.update()
    assert user_achievement.status == Status.IN_PROGRESS

    user_achievement.value = achievement.target
    user_achievement.update()
    assert user_achievement.status == Status.FINISHED

    user_achievement.close()
    assert user_achievement.status == Status.CLOSED
