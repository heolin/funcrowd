# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
import tasks as t
from modules.statistics.models.utils.agreement_ranking import get_agreement_ranking_mission
from modules.statistics.models.utils.high_agreement_helper import get_high_agreement_count


class UserMissionStats(models.Model):
    user = models.ForeignKey("users.EndWorker", on_delete=models.CASCADE, null=True,
                             related_name="+")
    mission = models.ForeignKey("tasks.Mission", on_delete=models.CASCADE, null=True,
                                related_name='+')
    high_agreement_count = models.IntegerField(default=0)
    agreement_ranking_position = models.IntegerField(default=0)
    agreement_ranking_percentage = models.FloatField(default=0)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Stats (#{}): Mission: {}".format(
            self.id, self.mission)

    @property
    def annotated_documents(self):
        return t.models.Annotation.objects.filter(user=self.user).filter(item__task__mission=self.mission)\
            .values("item__document").distinct().count()

    def update_high_agreement_count(self):
        self.high_agreement_count = get_high_agreement_count(self.user, self.mission)
        self.save()

    def update_agreement_ranking(self):
        self.agreement_ranking_position, self.agreement_ranking_percentage \
            = get_agreement_ranking_mission(self.mission, self.high_agreement_count)
        self.save()
