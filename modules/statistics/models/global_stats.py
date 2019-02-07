# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models

import tasks as t
import users as u
from tasks.consts import FINISHED, VERIFICATION


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
        return t.models.document.Document.objects.count()

    @property
    def total_finished_documents(self):
        return t.models.document.Document.objects.filter(status__in=[VERIFICATION, FINISHED]).count()

    @property
    def total_tasks(self):
        return t.models.task.Task.objects.count()

    @property
    def total_missions(self):
        return t.models.mission.Mission.objects.count()
