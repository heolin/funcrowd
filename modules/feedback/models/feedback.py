# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models

from tasks.models.task import Task
from .feedback_field import FeedbackField
from .feedback_score_field import FeedbackScoreField


class Feedback(models.Model):
    task = models.OneToOneField(Task, on_delete=models.SET_NULL,
                                null=True, related_name="feedback")
    score_fields = models.ManyToManyField(FeedbackScoreField)
    fields = models.ManyToManyField(FeedbackField)

    def __str__(self):
        return "Feedback(#{} - {})".format(self.task.id, self.task.name)

    def score(self, annotation):
        result = {}
        for field in self.score_fields:
            result[field.name] = field.score(annotation)
        return result

    def evaluate(self, annotation):
        result = {}
        for field in self.fields:
            result[field.name] = field.evaluate(annotation)
        return result
