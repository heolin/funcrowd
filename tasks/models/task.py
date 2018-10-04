# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from tasks.models.mission import Mission

from modules.order_strategy.models import Strategy


"""
Tasks are the base object for core logic of the platform
"""


class Task(models.Model):
    name = models.CharField(max_length=300)

    description = models.CharField(max_length=500, default="", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    max_annotations = models.IntegerField(default=0)
    multiple_annotations = models.BooleanField(default=False)

    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name="tasks")
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)

    order = models.IntegerField(default=0)

    def get_next_item(self, item):
        raise NotImplemented
        return self.items.filter(order__gt=item.order).first()

    def get_previous_item(self, item):
        return self.items.filter(order__lt=item.order).last()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return "{}({})".format(
            self.__class__.__name__,
            'name='+self.name,
        )
