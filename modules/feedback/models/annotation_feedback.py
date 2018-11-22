# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models

from tasks.models.annotation import Annotation


class AnnotationFeedback(models.Model):
    annotation = models.OneToOneField(Annotation)
    data = JSONField()
    created = models.DateTimeField(auto_now_add=True, on_delete=models.SET_NULL)
