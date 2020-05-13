# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from modules.order_strategy.models import Strategy
from tasks.models.mission import Mission


class MissionPackages(models.Model):
    mission = models.OneToOneField(Mission, on_delete=models.CASCADE, related_name="packages")
    max_annotations = models.IntegerField()
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)

    def __str__(self):
        return "MissionPackages {}".format(self.mission.id)

