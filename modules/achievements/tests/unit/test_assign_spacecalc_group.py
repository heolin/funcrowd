import pytest
import random

from modules.achievements.models import UserAchievement
from tasks.models import Task, Annotation
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
def test_progress_logic(user3000, task_with_items):
    user = user3000
    assert user.profile == ProfileType.NORMAL

    random.seed(1)

    task = Task.objects.first()

    achievement = AssignSpaceCalcGroupAchievement.objects.create(
        order=0, task=task, exp=0, target=1)

    user_achievement = UserAchievement.objects.create(user=user, achievement=achievement)
    user_achievement.update()
    assert user_achievement.progress == 0

    task = Task.objects.get(id=1)
    for item in task.items.all():
        annotation = Annotation.objects.create(
            item=item,
            data={
                "met_2_age": 34,
            },
            annotated=True,
            user=user
        )
        annotation.save()
        user.on_annotation(annotation)

    user_achievement.update()
    assert user_achievement.progress == 1

    user_achievement.close()

    user = EndWorker.objects.get(id=user.id)
    assert user.profile == ProfileType.ELEARNING


@pytest.mark.django_db
def test_progress_logic_user_id_under_threshold(user1, task_with_items):
    """
    If user id is not above the hardcoded threshold his profile will not change
    """
    user = user1
    assert user.profile == ProfileType.NORMAL

    random.seed(1)

    task = Task.objects.first()

    achievement = AssignSpaceCalcGroupAchievement.objects.create(
        order=0, task=task, exp=0, target=1)

    user_achievement = UserAchievement.objects.create(user=user, achievement=achievement)
    user_achievement.update()
    assert user_achievement.progress == 0

    task = Task.objects.get(id=1)
    for item in task.items.all():
        annotation = Annotation.objects.create(
            item=item,
            data={
                "met_2_age": 34,
            },
            annotated=True,
            user=user
        )
        annotation.save()
        user.on_annotation(annotation)

    user_achievement.update()
    assert user_achievement.progress == 1

    user_achievement.close()

    user = EndWorker.objects.get(id=user.id)
    assert user.profile == ProfileType.NORMAL

