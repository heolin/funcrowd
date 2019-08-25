# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.postgres.fields import JSONField


class Achievement(models.Model):
    metadata = JSONField(blank=True, default={})
    created = models.DateTimeField(auto_now_add=True)
    target = models.FloatField()
    value = models.CharField(default="", max_length=20)

    class Meta:
        verbose_name_plural = "Achievements"
