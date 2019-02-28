# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.db.models import F, Avg
from tasks.consts import VERIFICATION, FINISHED
import tasks as t
import modules.statistics as s


class MissionStats(models.Model):
    mission = models.OneToOneField("tasks.Mission", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "Stats (#{}): Mission: {}".format(
            self.id, self.mission)

    @property
    def total_users(self):
        return t.models.annotation.Annotation.objects.filter(
            item__task__mission_id=self.mission).values('user').distinct().count()

    @property
    def total_documents(self):
        return t.models.document.Document.objects.filter(mission=self.mission).count()

    @property
    def total_finished_documents(self):
        return t.models.document.Document.objects.filter(mission=self.mission).filter(
            status__in=[VERIFICATION, FINISHED]).count()

    @property
    def total_tasks(self):
        return self.mission.tasks.count()

    @property
    def agreement_mean(self):
        return s.models.user_mission_stats.UserMissionStats.objects.filter(
            mission=self.mission).aggregate(Avg('high_agreement_percentage'))['high_agreement_percentage__avg']
