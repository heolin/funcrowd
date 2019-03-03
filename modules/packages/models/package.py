# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models

from django.contrib.postgres.fields import JSONField

from tasks.consts import STATUSES, NEW
from modules.packages.models.mission_packages import MissionPackages


class Package(models.Model):
    parent = models.ForeignKey(MissionPackages, on_delete=models.CASCADE, related_name="packages")
    order = models.IntegerField(default=0)
    name = models.CharField(max_length=100, default="")
    status = models.CharField(max_length=20, choices=[(v, v) for v in STATUSES], default=NEW)
    metadata = JSONField(blank=True, null=True)

    def __str__(self):
        return "Package {} {} {}".format(self.parent.mission.id, self.name, self.order)

    class Meta:
        ordering = ['order']
