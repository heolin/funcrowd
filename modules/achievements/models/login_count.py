from modules.achievements.models.achievement import Achievement
from modules.achievements.events import Events


class LoginCountAchievement(Achievement):
    trigger_events = [
        Events.ON_LOGIN
    ]
