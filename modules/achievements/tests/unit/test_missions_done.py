import pytest

from modules.achievements.models import UserAchievement, MissionsDoneAchievement
from tasks.consts import MissionStatus
from tasks.models import Mission


@pytest.mark.django_db
def test_item_done_logic(user1, missions_with_tasks):
    achievement = MissionsDoneAchievement.objects.create(order=1, target=2)
    assert achievement

    user_achievement = UserAchievement.objects.create(user=user1, achievement=achievement)
    user_achievement.update()
    assert user_achievement.value == 0

    mission1 = Mission.objects.all()[0]
    mission2 = Mission.objects.all()[1]

    progress = user1.get_mission_progress(mission1)
    progress.status = MissionStatus.FINISHED
    progress.save()

    user_achievement.update()
    assert user_achievement.progress == 0.5

    progress = user1.get_mission_progress(mission2)
    progress.status = MissionStatus.FINISHED
    progress.save()

    user_achievement.update()
    assert user_achievement.progress == 1.0
