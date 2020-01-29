from modules.achievements.events import Events
from modules.achievements.models.achievement import Achievement
from tasks.consts import MissionStatus
from tasks.models import UserTaskProgress, Annotation, UserMissionProgress
from django.utils.timezone import now


class UnlockMissionAfterTaskAchievement(Achievement):
    trigger_events = [
        Events.ON_LOGIN
    ]

    def update(self, user_achievement):
        progress = UserTaskProgress.objects.filter(user=user_achievement.user,
                                                   task=self.task).first()
        if progress == 1.0:
            last_annotation = Annotation.objects.filter(user=user_achievement.user,
                                                        item__task=self.task).last()

            days = (now() - last_annotation.created).days
            user_achievement.value = min(days, self.target)

    def on_close(self, user_achievement):
        user = user_achievement.user
        progress = user.get_mission_progress(self.mission)
        if progress.status == MissionStatus.LOCKED:
            progress.status = MissionStatus.UNLOCKED
            progress.save()

    def save(self, *args, **kwargs):
        if not self.task or not self.mission:
            raise ValueError("Required value for Task and Mission field")
        super(UnlockMissionAfterTaskAchievement, self).save(*args, **kwargs)
