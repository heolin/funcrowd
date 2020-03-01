
from modules.achievements.models.achievement import Achievement
from modules.achievements.events import Events
from tasks.consts import TaskStatus
from tasks.models import UserTaskProgress


class TasksDoneAchievement(Achievement):
    trigger_events = [
        Events.ON_ITEM_DONE
    ]

    def update(self, user_achievement):
        user_achievement.value = UserTaskProgress.objects.filter(
            user=user_achievement.user, status=TaskStatus.FINISHED).count()
