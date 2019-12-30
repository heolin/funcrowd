# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.timezone import now

from tasks.consts import EXP_BONUS_1, EXP_BONUS_3, EXP_BONUS_5
from users.models.end_workers import EndWorker


class Annotation(models.Model):
    data = JSONField()
    item = models.ForeignKey("Item", on_delete=models.CASCADE, related_name="annotations")
    user = models.ForeignKey(EndWorker, blank=True, null=True, on_delete=models.CASCADE)
    skipped = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    annotated = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    exp = models.IntegerField(default=0)

    def __str__(self):
        TEMPLATE = "Task {} (#{}) - Item: {} (#{}) - Annotation: #{} - User: {}"
        return TEMPLATE.format(self.item.task.order, self.item.task.id,
                               self.item.order, self.item.id, self.id, self.user)

    def get_feedback(self):
        if hasattr(self, "feedback"):
            return self.feedback

    def get_exp(self):
        # exp was already assigned to this annotation
        if self.exp > 0:
            return 0, 0

        exp, bonus = 0, 0

        # exp was not assigned
        feedback = self.get_feedback()
        feedback_score = 1.0

        if feedback and feedback.score is not None:
            feedback_score = feedback.score

        # task supports multiple annotations,
        #  but exp is assigned only for the first correct  annotation
        if self.item.task.multiple_annotations:
            prev_annotations = self.item.annotations.filter(
                user=self.user).exclude(id=self.id)

            first_correct = prev_annotations.filter(feedback__score__gt=0).count() == 0
            if first_correct and feedback_score > 0.0:
                exp = self.item.exp * feedback_score

                if prev_annotations.count() == 0:
                    bonus = exp + EXP_BONUS_1
                elif prev_annotations.count() <= 3:
                    bonus = exp + EXP_BONUS_3
                else:
                    bonus = exp + EXP_BONUS_5
        else:
            exp = self.item.exp * feedback_score

        if exp > 0:
            self.exp = exp + bonus
            self.save()

        return exp, bonus

    @property
    def attempt(self):
        return self.item.annotations.filter(user=self.user).count()
