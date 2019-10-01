# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from polymorphic.models import PolymorphicModel
from django.contrib.postgres.fields import JSONField

from tasks.models import Mission, Task


class Achievement(PolymorphicModel):
    trigger_events = []

    order = models.IntegerField(default=0)
    metadata = JSONField(blank=True, default={})
    target = models.FloatField(default=1)

    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, null=True, blank=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Achievements"
        ordering = ('order',)

    def update(self, user_achievement):
        pass

    def on_close(self, user_achievement):
        pass
