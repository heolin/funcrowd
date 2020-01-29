import pytest

from modules.achievements.models import UserAchievement, ProgressAchievement
from modules.achievements.models.unlock_mission_after_task import UnlockMissionAfterTaskAchievement
from tasks.models import Item


@pytest.mark.django_db
def test_progress_logic(user1, wrong_progress_achievement):
    achievement = ProgressAchievement.objects.filter(order=4).first()
    user_achievement = UserAchievement.objects.create(user=user1, achievement=achievement)
    with pytest.raises(ValueError):
        user_achievement.update()


@pytest.mark.django_db
def test_create_object(user1, task_with_items):
    # create achievement with only task
    with pytest.raises(ValueError):
        UnlockMissionAfterTaskAchievement.objects.create(order=5, task_id=1, exp=0)

    # create achievement for mission
    assert ProgressAchievement.objects.create(order=6, mission_id=1, exp=10)

    # create achievement without mission or task field
    with pytest.raises(ValueError):
        assert ProgressAchievement.objects.create(order=6, exp=10)


@pytest.mark.django_db
def test_progress_logic(user1, achievements):
    achievement = ProgressAchievement.objects.filter(order=5).first()
    user_achievement = UserAchievement.objects.create(user=user1, achievement=achievement)
    user_achievement.update()
    assert user_achievement.value == 0

    item = Item.objects.filter(task_id=1, order=1).first()
    annotation, _ = item.get_or_create_annotation(user1)
    annotation.data = {"output": 1}
    annotation.annotated = True
    annotation.save()
    user1.on_annotation(annotation)

    user_achievement.update()
    assert user_achievement.value == 0.5

    achievement = ProgressAchievement.objects.filter(order=6).first()
    mission_user_achievement = UserAchievement.objects.create(user=user1, achievement=achievement)
    mission_user_achievement.update()
    assert mission_user_achievement.value == 0

    item = Item.objects.filter(task_id=1, order=2).first()
    annotation, _ = item.get_or_create_annotation(user1)
    annotation.data = {"output": 1}
    annotation.annotated = True
    annotation.save()
    user1.on_annotation(annotation)

    user_achievement.update()
    assert user_achievement.value == 1.0

    mission_user_achievement.update()
    assert mission_user_achievement.value == 0.5
