# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.postgres.fields import JSONField
from tasks.consts import STATUSES, NEW

"""
"""


class Document(models.Model):
    name = models.CharField(max_length=100, default="")
    mission = models.ForeignKey("Mission", on_delete=models.CASCADE, related_name="documents")
    status = models.CharField(max_length=20, choices=[(v, v) for v in STATUSES], default=NEW)
    metadata = JSONField(blank=True, null=True)

    def __str__(self):
        return "{}({}, {})".format(
            self.__class__.__name__,
            'name='+self.name,
            'mission='+self.mission
            )
