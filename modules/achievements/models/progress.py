
from django.db import models
from modules.achievements.models.achievement import Achievement
from modules.achievements.events import Events
from tasks.models import Annotation, UserTaskProgress, UserMissionProgress


class ProgressAchievement(Achievement):
    trigger_events = [
        Events.ON_ITEM_DONE
    ]

    def update(self, user_achievement):
        if self.task:
            user_progress = UserTaskProgress.objects.filter(
                user=user_achievement.user, task=self.task).first()

        elif self.mission:
            user_progress = UserMissionProgress.objects.filter(
                user=user_achievement.user, task=self.mission).first()

        if user_progress:
            user_achievement.value = user_progress.progress

    def save(self, *args, **kwargs):
        if not self.task and not self.mission:
            raise ValueError("Required value for Task or Mission field")
        super(ProgressAchievement, self).save(*args, **kwargs)
