from django.db import transaction

import modules.achievements as a


class EventsManager:
    def __init__(self):
        self._achievements = {}

    def register_achievements(self, achievement):
        for event_type in achievement.trigger_events:
            self._achievements.setdefault(event_type, [])
            self._achievements[event_type].append(achievement)

    @transaction.atomic
    def on_event(self, event):
        for A in self._achievements[event]:
            for user_achievement in a.models.UserAchievement.objects.filter(achievement__in=A.objects.all()):
                current = user_achievement.value
                user_achievement.update()
                if current != user_achievement.value:
                    user_achievement.save()
