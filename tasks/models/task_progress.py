# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models

from tasks.models import Task
from users.models.end_workers import EndWorker
from tasks.models.annotation import Annotation


class UserTaskProgress(models.Model):
    user = models.ForeignKey(EndWorker, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    items_done = models.IntegerField(default=0)

    def update(self):
        self.items_done = Annotation.objects.filter(
            item__task=self.task, user=self.user).values("item").distinct().count()
        self.save()

    @property
    def progress(self):
        if self.items_count:
            return self.items_done / self.items_count

    @property
    def items_count(self):
        return self.task.items.count()
