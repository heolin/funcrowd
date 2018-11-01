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

    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name="tasks")
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)

    max_annotations = models.IntegerField(default=0)
    multiple_annotations = models.BooleanField(default=False)

    order = models.IntegerField(default=0)

    def next_item(self, user, item):
        return self.strategy.next(self, user, item)

    def prev_item(self, user, item):
        return self.strategy.prev(self, user, item)

    def exclude_items_with_user_annotations(self, user):
        return self.items.exclude(annotations__user=user)

    def annotate_annotations_done(self, items):
        return items.annotate(annotations_done=models.Count("annotations"))

    def exclude_max_annotations(self, items):
        return items.filter(annotations_done__lt=self.max_annotations)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return "{}({})".format(
            self.__class__.__name__,
            'name='+self.name,
        )
