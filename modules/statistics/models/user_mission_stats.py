# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models


class UserMissionStats(models.Model):
    items_done = models.IntegerField(default=0)
    user = models.OneToOneField("users.EndWorker", on_delete=models.CASCADE, null=True,
                                related_name="local_mission_stats")
    mission = models.OneToOneField("tasks.Mission", on_delete=models.CASCADE, null=True,
                                   related_name='+')

    def __str__(self):
        return "Stats (#{}): Mission: {}".format(
            self.id, self.task, self.annotations_target)

