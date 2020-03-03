from django.db import transaction

import modules.achievements as a


class EventsManager:
    def __init__(self):
        self._achievements = {}

    def register_achievements(self, achievement):
        for event_type in achievement.trigger_events:
            self._achievements.setdefault(event_type, [])
            self._achievements[event_type].append(achievement)

    def on_event(self, user, event):
        for A in self._achievements[event]:
            achievements_ids = A.objects.values("achievement_ptr_id")
            for user_achievement in a.models.UserAchievement.objects.filter(user=user,
                                                                            achievement__in=achievements_ids):
                current = user_achievement.value
                user_achievement.update()
                if current != user_achievement.value:
                    user_achievement.save()

    def update_all(self, user):
        for user_achievement in a.models.UserAchievement.objects.filter(user=user):
            current = user_achievement.value
            user_achievement.update()
            if current != user_achievement.value:
                user_achievement.save()
