
from django.db import models
from modules.achievements.models.achievement import Achievement
from modules.achievements.events import Events
from tasks.models import Annotation


class ItemDoneAchievement(Achievement):
    trigger_events = [
        Events.ON_ITEM_DONE
    ]

    def update(self, user_achievement):
        annotations = Annotation.objects.filter(
            user=user_achievement.user, annotated=True).exclude(
            skipped=True).exclude(rejected=True)

        if self.mission:
            annotations = annotations.filter(item__task__mission=self.mission)

        if self.task:
            annotations = annotations.filter(item__task=self.task)

        user_achievement.value = annotations.values("item").distinct().count()
