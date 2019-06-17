# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models

from django.contrib.postgres.fields import JSONField

import modules.aggregation as a
from tasks.consts import STATUSES, NEW, IN_PROGRESS, FINISHED, VERIFICATION
from modules.packages.models.mission_packages import MissionPackages
import numpy as np


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

    def update_status(self):
        aggregations = a.models.ItemAggregation.objects.filter(item__package=self)

        probability = np.min([a.get_probability() for a in aggregations])
        support = np.max([a.get_support() for a in aggregations])

        if self.status in [NEW, IN_PROGRESS]:
            if support >= 4 and probability > 0.5:
                self.status = FINISHED
                self.save()
            elif support >= 7:
                self.status = VERIFICATION
                self.save()
            elif support >= 1:
                self.status = IN_PROGRESS
                self.save()
