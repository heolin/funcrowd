import pytest
import random

from modules.achievements.models import UserAchievement, ProgressAchievement
from modules.achievements.models.unlock_mission_after_task import UnlockMissionAfterTaskAchievement
from tasks.consts import MissionStatus
from tasks.models import Item, Task, Annotation
from datetime import timedelta
from modules.achievements.models.assign_spacecalc_group import AssignSpaceCalcGroupAchievement

from users.consts import ProfileType
from users.models import EndWorker


@pytest.mark.django_db
def test_create_object(user1, task_with_items):
    # create achievement without the task or mission field
    with pytest.raises(ValueError):
        AssignSpaceCalcGroupAchievement.objects.create(order=5, exp=0)

    # create achievement with all required fields
    achievement = AssignSpaceCalcGroupAchievement.objects.create(
        order=5, task_id=1, exp=0)
    assert achievement


@pytest.mark.django_db
def test_progress_logic(user1, task_with_items):
    assert user1.profile == ProfileType.NORMAL

    random.seed(1)

    task = Task.objects.first()

    achievement = AssignSpaceCalcGroupAchievement.objects.create(
        order=0, task=task, exp=0, target=1)

    user_achievement = UserAchievement.objects.create(user=user1, achievement=achievement)
    user_achievement.update()
    assert user_achievement.progress == 0

    task = Task.objects.get(id=1)
    for item in task.items.all():
        annotation = Annotation.objects.create(
            item=item,
            data={"output": 1},
            annotated=True,
            user=user1
        )
        annotation.save()
        user1.on_annotation(annotation)

    user_achievement.update()
    assert user_achievement.progress == 1

    user_achievement.close()

    user1 = EndWorker.objects.get(id=user1.id)
    assert user1.profile == ProfileType.ELEARNING
