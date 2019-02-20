# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
import tasks as t


class UserMissionStats(models.Model):
    user = models.ForeignKey("users.EndWorker", on_delete=models.CASCADE, null=True,
                             related_name="+")
    mission = models.ForeignKey("tasks.Mission", on_delete=models.CASCADE, null=True,
                                related_name='+')
    high_agreement_count = models.IntegerField(default=0)
    agreement_ranking_position = models.IntegerField(default=0)
    agreement_ranking_percentage = models.FloatField(default=0)

    def __str__(self):
        return "Stats (#{}): Mission: {}".format(
            self.id, self.task, self.annotations_target)

    @property
    def annotated_documents(self):
        return t.models.Annotation.objects.filter(user=self.user).filter(item__task__mission=self.mission)\
            .values("item__document").distinct().count()

    def update(self):
        pass
