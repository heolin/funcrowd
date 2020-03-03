from modules.achievements.events import Events
from modules.achievements.models.achievement import Achievement

from users.consts import ProfileType
from users.models import EndWorker


def assign_user_profile(user):
    gamification = EndWorker.objects.filter(profile=ProfileType.GAMIFICATION).count()
    elearning = EndWorker.objects.filter(profile=ProfileType.ELEARNING).count()

    if gamification > elearning:
        user.profile = ProfileType.ELEARNING
    else:
        user.profile = ProfileType.GAMIFICATION
    user.save()


class AssignSpaceCalcGroupAchievement(Achievement):
    trigger_events = [
        Events.ON_ITEM_DONE,
        Events.ALWAYS
    ]

    def update(self, user_achievement):
        user_progress = user_achievement.user.get_task_progress(self.task)
        user_achievement.value = user_progress.progress

    def on_close(self, user_achievement):
        user = user_achievement.user
        if user.profile == ProfileType.NORMAL:
            assign_user_profile(user)

    def save(self, *args, **kwargs):
        if not self.task and not self.mission:
            raise ValueError("Required value for Task and Mission field")
        super(AssignSpaceCalcGroupAchievement, self).save(*args, **kwargs)

