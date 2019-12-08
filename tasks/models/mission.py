# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.postgres.fields import JSONField

import modules.statistics as s
import modules.achievements as a
import tasks as t

"""
Mission are the base object used for story logic.
Each mission can store multiple tasks.
"""


class Mission(models.Model):
    name = models.CharField(max_length=100, default="")
    description = models.TextField(default="", blank=True)
    instruction = models.TextField(default="", blank=True)
    metadata = JSONField(blank=True, default=dict)
    order = models.IntegerField(default=0)
    parent = models.ForeignKey('Mission', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['order']

    def get_next_task(self, task):
        return self.tasks.filter(order__gt=task.order).first()

    @property
    def stats(self):
        MissionStats = s.models.MissionStats
        stats, _ = MissionStats.objects.get_or_create(mission=self)
        return stats

    @property
    def tasks_count(self):
        return self.tasks.count()

    @property
    def achievements_count(self):
        Achievement = a.models.Achievement
        return Achievement.objects.filter(mission=self).count()

    @property
    def total_exp(self):
        Item = t.models.Item
        return Item.objects.filter(task__mission=self).aggregate(models.Sum("exp"))['exp__sum']

    def __str__(self):
        return "{}({})".format(
            self.__class__.__name__,
            'name='+self.name,
            )
