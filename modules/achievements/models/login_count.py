from modules.achievements.models.achievement import Achievement
from modules.achievements.events import Events


class LoginCountAchievement(Achievement):
    trigger_events = [
        Events.ON_LOGIN
    ]

    def update(self, user_achievement):
        user_achievement.value = user_achievement.user.login_count
