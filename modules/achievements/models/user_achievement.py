# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models

from modules.achievements.consts import Status
from modules.achievements.models.achievement import Achievement
from users.models import EndWorker


class UserAchievement(models.Model):
    status = models.CharField(default=Status.NEW, max_length=20)
    user = models.ForeignKey(EndWorker, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    value = models.FloatField(default=0)
    updated = models.DateTimeField(auto_now=True)

    def update(self):
        self.achievement.update(self)
        self._update_state()

    def _update_state(self):
        if self.status == Status.NEW:
            if self.value > 0:
                self.status = Status.IN_PROGRESS

        if self.status == Status.IN_PROGRESS:
            if self.value >= self.achievement.target:
                self.status = Status.FINISHED

    def close(self):
        if self.status == Status.FINISHED:
            self.status = Status.CLOSED
            self.save()
            self.achievement.on_close(self)

    @staticmethod
    def get_user_achievements(user):
        user_achievements = UserAchievement.objects.filter(user=user)
        achievements = Achievement.objects.exclude(id__in=user_achievements.values("achievement"))
        if achievements:
            UserAchievement.objects.bulk_create([
                UserAchievement(achievement=achievement, user=user) for achievement in achievements
            ])
        user_achievements = UserAchievement.objects.filter(user=user)
        return user_achievements

    @property
    def progress(self):
        return self.value / self.achievement.target

    @property
    def target(self):
        return self.achievement.target

    @property
    def order(self):
        return self.achievement.order
