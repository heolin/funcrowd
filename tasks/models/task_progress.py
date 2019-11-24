# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models

from tasks.consts import TaskStatus, TASK_STATUSES
from tasks.models import Task
from users.models.end_workers import EndWorker
from tasks.models.annotation import Annotation


class UserTaskProgress(models.Model):
    user = models.ForeignKey(EndWorker, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    items_done = models.IntegerField(default=0)
    status = models.CharField(default=TaskStatus.LOCKED, choices=TASK_STATUSES, max_length=32)

    def update(self):
        self.items_done = Annotation.objects.filter(
            annotated=True, skipped=False, rejected=False,
            item__task=self.task, user=self.user).values("item").distinct().count()

        self.update_status(False)
        self.save()

    def update_status(self, commit=True):
        parent_progress = self._get_parent_progress()

        last_status = self.status

        if self.status == TaskStatus.LOCKED:
            if not parent_progress:
                self.status = TaskStatus.UNLOCKED
            elif parent_progress.status == TaskStatus.FINISHED:
                self.status = TaskStatus.UNLOCKED
        if self.status == TaskStatus.UNLOCKED:
            if self.items_done > 0:
                self.status = TaskStatus.IN_PROGRESS
        if self.status == TaskStatus.IN_PROGRESS:
            if self.items_done == self.items_count:
                self.status = TaskStatus.FINISHED

        if commit and last_status != self.status:
            self.save()

    def _get_parent_progress(self):
        parent_progress = None
        if self.task.parent:
            parent_progress = UserTaskProgress.objects.filter(
                task=self.task.parent,
                user=self.user
            ).first()
        return parent_progress

    @property
    def progress(self):
        if self.items_count:
            return self.items_done / self.items_count

    @property
    def items_count(self):
        return self.task.items.count()

    @property
    def max_score(self):
        return self.task.items.filter(template__fields__editable=True, template__fields__required=True).annotate(
            annotations_fields=models.Count("template__fields")).aggregate(
            models.Sum("annotations_fields"))['annotations_fields__sum']

    @property
    def score(self):
        score_values = self.task.items.filter(annotations__user_id=self.user.id, annotations__annotated=True).values(
            "annotations__id", "annotations__item_id", "annotations__feedback__score").order_by("annotations__id")

        scores = {}
        for values in score_values:
            scores[values["annotations__item_id"]] = values["annotations__feedback__score"]

        if score_values:
            return sum(scores.values())
