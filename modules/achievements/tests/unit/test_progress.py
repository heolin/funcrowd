import pytest

from modules.achievements.models import UserAchievement, ProgressAchievement
from tasks.models import Item


@pytest.mark.django_db
def test_progress_logic(setup_user1, setup_achievements):
    user = setup_user1

    achievement = ProgressAchievement.objects.filter(order=4).first()
    user_achievement = UserAchievement.objects.create(user=user, achievement=achievement)
    with pytest.raises(ValueError):
        user_achievement.update()

    achievement = ProgressAchievement.objects.filter(order=5).first()
    user_achievement = UserAchievement.objects.create(user=user, achievement=achievement)
    user_achievement.update()
    assert user_achievement.value == 0

    item = Item.objects.filter(task_id=1, order=1).first()
    annotation, _ = item.get_or_create_annotation(user)
    annotation.data = {"output": 1}
    annotation.save()
    user.on_annotation(annotation)

    user_achievement.update()
    assert user_achievement.value == 0.5

    achievement = ProgressAchievement.objects.filter(order=6).first()
    mission_user_achievement = UserAchievement.objects.create(user=user, achievement=achievement)
    mission_user_achievement.update()
    assert mission_user_achievement.value == 0

    item = Item.objects.filter(task_id=1, order=2).first()
    annotation, _ = item.get_or_create_annotation(user)
    annotation.data = {"output": 1}
    annotation.save()
    user.on_annotation(annotation)

    user_achievement.update()
    assert user_achievement.value == 1.0

    mission_user_achievement.update()
    assert mission_user_achievement.value == 0.5
