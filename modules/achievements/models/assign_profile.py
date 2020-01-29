
from django.db import models
from modules.achievements.models.achievement import Achievement
from modules.achievements.events import Events
from tasks.models import Annotation, UserTaskProgress, UserMissionProgress
from users.consts import ProfileType
from users.models import EndWorker


class AssignProfileAchievement(Achievement):
    trigger_events = [
        Events.ON_ITEM_DONE
    ]

    def update(self, user_achievement):
        if self.task:
            progress = UserTaskProgress.objects.filter(user=user_achievement.user,
                                                       task=self.task).first()
            if progress:
                user_achievement.value = progress.progress

        elif self.mission:
            progress = UserMissionProgress.objects.filter(user=user_achievement.user,
                                                          mission=self.mission).first()
            if progress:
                user_achievement.value = progress.progress

    def on_close(self, user_achievement):
        user = user_achievement.user
        profile2 = EndWorker.objects.filter(profile=ProfileType.GAMIFICATION).count()
        profile3 = EndWorker.objects.filter(profile=ProfileType.ELEARNING).count()

        if user.profile == ProfileType.NORMAL:
            if profile2 > profile3:
                user.profile = ProfileType.ELEARNING
            else:
                user.profile = ProfileType.GAMIFICATION
            user.save()

    def save(self, *args, **kwargs):
        if not self.task and not self.mission:
            raise ValueError("Required value for Task or Mission field")
        super(AssignProfileAchievement, self).save(*args, **kwargs)

