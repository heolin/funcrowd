# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.timezone import now

from users.models.end_workers import EndWorker


class Annotation(models.Model):
    data = JSONField()
    item = models.ForeignKey("Item", on_delete=models.CASCADE, related_name="annotations")
    user = models.ForeignKey(EndWorker, blank=True, null=True, on_delete=models.CASCADE)
    skipped = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    annotated = models.BooleanField(default=False)

    def __str__(self):
        TEMPLATE = "Task {} (#{}) - Item: {} (#{}) - Annotation: #{} - User: {}"
        return TEMPLATE.format(self.item.task.order, self.item.task.id,
                               self.item.order, self.item.id, self.id, self.user)

    def get_feedback(self):
        if hasattr(self, "feedback"):
            return self.feedback

    def get_exp(self):
        feedback = self.get_feedback()
        feedback_score = 1.0
        if feedback:
            feedback_score = feedback.score

        if self.item.task.multiple_annotations:
            # check if previous annotations were correct
            exp = self.item.exp * feedback_score
        else:
            exp = self.item.exp * feedback_score
        return exp
