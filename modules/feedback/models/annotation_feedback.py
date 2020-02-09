# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models

from tasks.models.annotation import Annotation

from django.contrib.postgres.fields import JSONField


class AnnotationFeedback(models.Model):
    annotation = models.OneToOneField(Annotation, on_delete=models.CASCADE, related_name="feedback")
    values = JSONField(default=dict)
    scores = JSONField(default=dict)
    score = models.FloatField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
