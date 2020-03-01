import pytest

from modules.achievements.models import UserAchievement, TasksDoneAchievement
from tasks.consts import TaskStatus
from tasks.models import Mission


@pytest.mark.django_db
def test_item_done_logic(user1, missions_with_tasks):
    achievement = TasksDoneAchievement.objects.create(order=1, target=2)
    assert achievement

    user_achievement = UserAchievement.objects.create(user=user1, achievement=achievement)
    user_achievement.update()
    assert user_achievement.value == 0

    mission1 = Mission.objects.first()

    task1 = mission1.tasks.all()[0]
    task2 = mission1.tasks.all()[1]

    progress = user1.get_task_progress(task1)
    progress.status = TaskStatus.FINISHED
    progress.save()

    user_achievement.update()
    assert user_achievement.progress == 0.5

    progress = user1.get_task_progress(task2)
    progress.status = TaskStatus.FINISHED
    progress.save()

    user_achievement.update()
    assert user_achievement.progress == 1.0
