
from modules.achievements.models.achievement import Achievement
from modules.achievements.events import Events
from tasks.consts import MissionStatus
from tasks.models import UserMissionProgress


class MissionsDoneAchievement(Achievement):
    trigger_events = [
        Events.ON_ITEM_DONE
    ]

    def update(self, user_achievement):
        user_achievement.value = UserMissionProgress.objects.filter(
            user=user_achievement.user, status=MissionStatus.FINISHED).count()
