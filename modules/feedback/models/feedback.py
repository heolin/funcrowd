# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models

from modules.feedback.consts import FeedbackTypes, FEEDBACK_TYPES
from tasks.models.task import Task
from .feedback_field import FeedbackField
from .feedback_score_field import FeedbackScoreField

from modules.feedback.models.annotation_feedback import AnnotationFeedback

import numpy as np


class Feedback(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE,
                                null=True, related_name="feedback")
    score_fields = models.ManyToManyField(FeedbackScoreField, blank=True)
    fields = models.ManyToManyField(FeedbackField, blank=True)
    type = models.CharField(max_length=32, choices=FEEDBACK_TYPES, default=FeedbackTypes.NONE)
    autoreject = models.BooleanField(default=False)

    def __str__(self):
        return "Feedback(#{} - {})".format(self.task.id, self.task.name)

    def score_field(self, field_name, annotation):
        result = {}
        for field in self.score_fields.all():
            result[field.name] = field.score(field_name, annotation)
        return result

    def score(self, annotation):
        result = {}
        for field in annotation.item.template.feedback_fields:
            result[field.name] = self.score_field(field.name, annotation)
        return result

    def evaluate_field(self, field_name, annotation):
        result = {}
        for field in self.fields.all():
            result[field.name] = field.evaluate(field_name, annotation)
        return result

    def evaluate(self, annotation):
        result = {}
        for field in annotation.item.template.feedback_fields:
            result[field.name] = self.evaluate_field(field.name, annotation)
        return result

    def aggregate_scores(self, scores):
        score_values = []
        for field_values in scores.values():
            field_score_values = np.average(list(field_values.values()))
            score_values.append(field_score_values)
        if score_values:
            return np.sum(score_values)
        return None

    def create_feedback(self, annotation):
        scores = self.score(annotation)
        values = self.evaluate(annotation)
        score_value = self.aggregate_scores(scores)

        feedback, _ = AnnotationFeedback.objects.get_or_create(feedback=self, annotation=annotation)
        feedback.scores = scores
        feedback.values = values
        feedback.score = score_value
        feedback.save()
        return feedback
