# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.postgres.fields import JSONField
from django.db import models

from tasks.models.annotation import Annotation


class AnnotationFeedback(models.Model):
    feedback = models.ForeignKey("Feedback", on_delete=models.CASCADE, null=True, blank=True)
    annotation = models.OneToOneField(Annotation, on_delete=models.CASCADE, related_name="feedback")
    values = JSONField(default=dict)
    scores = JSONField(default=dict)
    score = models.FloatField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def type(self):
        return self.feedback.type
