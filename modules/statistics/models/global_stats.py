# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from tasks.consts import FINISHED, VERIFICATION
import modules.packages as p
import tasks as t
import users as u


class GlobalStats(models.Model):

    def __str__(self):
        return "Global Stats"

    def save(self, *args, **kwargs):
        objects = self.__class__.objects.first()
        if objects:
            self.pk = objects.pk
        super().save(*args, **kwargs)

    @property
    def total_users(self):
        return u.models.end_workers.EndWorker.objects.count()

    @property
    def total_documents(self):
        return p.models.package.Package.objects.count()

    @property
    def total_finished_documents(self):
        return p.models.package.Package.objects.filter(status__in=[VERIFICATION, FINISHED]).count()

    @property
    def total_tasks(self):
        return t.models.task.Task.objects.count()

    @property
    def total_finished_items(self):
        packages = p.models.package.Package.objects.filter(status__in=[VERIFICATION, FINISHED])
        return t.models.item.Item.objects.filter(package__in=packages).count()

    @property
    def total_finished_items(self):
        packages = p.models.package.Package.objects.filter(status__in=[VERIFICATION, FINISHED])
        return t.models.item.Item.objects.filter(package__in=packages).count()

    @property
    def total_missions(self):
        return t.models.mission.Mission.objects.count()
