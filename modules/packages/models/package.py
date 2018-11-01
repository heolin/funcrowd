# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from sortedm2m.fields import SortedManyToManyField
from tasks.models.item import Item
from modules.packages.models.mission_packages import MissionPackages


class Package(models.Model):
    parent = models.ForeignKey(MissionPackages, on_delete=models.CASCADE, related_name="packages")
    items = SortedManyToManyField(Item)
    order = models.IntegerField(default=0)

    def __str__(self):
        return "Package {} {}".format(self.parent.mission.id, self.order)

    class Meta:
        ordering = ['order']
