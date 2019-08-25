# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models

from tasks.models import Mission, UserTaskProgress
from users.models.end_workers import EndWorker


class UserMissionProgress(models.Model):
    user = models.ForeignKey(EndWorker, on_delete=models.CASCADE)
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    tasks_done = models.IntegerField(default=0)

    def update(self):
        self.tasks_done = UserTaskProgress.objects.filter(user=self.user).annotate(
            items_count=models.Count('task__items')).annotate(
            progress=models.F('items_done') / models.F('items_count')).values(
            "progress").filter(progress=1).count()
        self.save()

    @property
    def progress(self):
        if self.tasks_count:
            return self.tasks_done / self.tasks_count


    @property
    def tasks_count(self):
        return self.mission.tasks.count()
