# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.postgres.fields import JSONField

import modules.statistics as s
import modules.achievements as a

"""
Mission are the base object used for story logic.
Each mission can store multiple tasks.
"""


class Mission(models.Model):
    name = models.CharField(max_length=100, default="")
    description = models.TextField(default="", blank=True)
    metadata = JSONField(blank=True, default={})
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def get_next_task(self, task):
        return self.tasks.filter(order__gt=task.order).first()

    @property
    def stats(self):
        cls = s.models.MissionStats
        stats, _ = cls.objects.get_or_create(mission=self)
        return stats

    @property
    def tasks_count(self):
        return self.tasks.count()

    @property
    def achievements_count(self):
        cls = a.models.Achievement
        return cls.objects.filter(mission=self).count()

    def __str__(self):
        return "{}({})".format(
            self.__class__.__name__,
            'name='+self.name,
            )
