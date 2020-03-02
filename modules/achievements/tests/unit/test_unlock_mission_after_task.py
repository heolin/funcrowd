import pytest

from modules.achievements.models import UserAchievement
from modules.achievements.models.unlock_mission_after_task import UnlockMissionAfterTaskAchievement
from tasks.consts import MissionStatus
from tasks.models import Annotation
from datetime import timedelta


@pytest.mark.django_db
def test_create_object(user1, task_with_items):
    # create achievement with only task
    with pytest.raises(ValueError):
        UnlockMissionAfterTaskAchievement.objects.create(order=5, task_id=1, exp=0)

    # create achievement with only mission
    with pytest.raises(ValueError):
        assert UnlockMissionAfterTaskAchievement.objects.create(order=5, mission_id=1, exp=0)

    # create achievement with all required fields
    achievement = UnlockMissionAfterTaskAchievement.objects.create(
        order=5, task_id=1, mission_id=1, exp=0)
    assert achievement


@pytest.mark.django_db
def test_progress_logic(user1, hidden_mission):
    days = 30
    mission = hidden_mission
    progress = user1.get_mission_progress(mission)
    assert progress.status == MissionStatus.LOCKED

    achievement = UnlockMissionAfterTaskAchievement.objects.create(
        order=5, task_id=1, mission=hidden_mission, exp=0, target=days)

    user_achievement = UserAchievement.objects.create(user=user1, achievement=achievement)
    user_achievement.update()
    assert user_achievement.progress == 0

    task = achievement.task
    for item in task.items.all():
        annotation = Annotation.objects.create(
            item=item,
            data={"output": 1},
            annotated=True,
            user=user1
        )
        annotation.created = annotation.created - timedelta(days=days)
        annotation.save()
        user1.on_annotation(annotation)

    user_achievement.update()
    assert user_achievement.progress == 1

    user_achievement.close()

    progress = user1.get_mission_progress(mission)
    assert progress.status == MissionStatus.UNLOCKED
