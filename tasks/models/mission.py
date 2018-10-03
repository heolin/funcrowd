# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models

"""
Mission are the base object used for story logic.
Each mission can store multiple tasks.
"""


class Mission(models.Model):
    name = models.CharField(max_length=100, default="")
    keywords = models.CharField(max_length=100, default="")
    description = models.TextField(default="", blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def get_next_task(self, task):
        return self.tasks.filter(order__gt=task.order).first()

    def __str__(self):
        return "{}({})".format(
            self.__class__.__name__,
            'name='+self.name,
            )
