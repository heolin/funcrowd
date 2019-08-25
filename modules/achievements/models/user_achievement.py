# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from users.models import EndWorker


class UserAchievement(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    progress = models.FloatField()
    user = models.ForeignKey(EndWorker)
    status = models.CharField(default="NONE", max_length=20)
