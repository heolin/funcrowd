# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from sortedm2m.fields import SortedManyToManyField
from tasks.models.item import Item
from tasks.models.mission import Mission


class Package(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name="packages")
    items = SortedManyToManyField(Item)
    order = models.IntegerField(default=0)

    def __str__(self):
        return "Task {} (#{}) - Item {} - {} (#{}) - {}".format(self.task.order, self.task.id,
                                                                self.order, self.template.name,
                                                                self.id, self.task.mission.name)

    class Meta:
        ordering = ['order']

