# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.db.models import Avg
from tasks.consts import VERIFICATION, FINISHED
import modules.packages as p
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
        return p.models.package.Package.objects.filter(parent__mission=self.mission).count()

    @property
    def total_finished_documents(self):
        return p.models.package.Package.objects.filter(parent__mission=self.mission).filter(
            status__in=[VERIFICATION, FINISHED]).count()

    @property
    def total_finished_items(self):
        packages = p.models.package.Package.objects.filter(parent__mission=self.mission).filter(
            status__in=[VERIFICATION, FINISHED])
        return t.models.item.Item.objects.filter(package__in=packages).count()

    @property
    def total_tasks(self):
        return self.mission.tasks.count()

    @property
    def total_annotations(self):
        return t.models.annotation.Annotation.objects.filter(
            item__task__mission_id=self.mission).count()

    @property
    def agreement_mean(self):
        return s.models.user_mission_stats.UserMissionStats.objects.filter(
            mission=self.mission).aggregate(Avg('high_agreement_percentage'))['high_agreement_percentage__avg']
