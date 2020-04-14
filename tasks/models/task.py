# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.db.models import IntegerField
from django.contrib.postgres.fields import JSONField

from tasks.consts import TASK_STATUSES
from tasks.models.mission import Mission

from modules.order_strategy.models import Strategy
import modules.achievements as a
import tasks as t
from django.db.models import Q


"""
Tasks are the base object for core logic of the platform
"""


class Task(models.Model):
    name = models.CharField(max_length=300)
    keywords = models.CharField(max_length=100, default="", blank=True)
    description = models.CharField(max_length=1000, default="", blank=True)
    instruction = models.TextField(default="", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('Task', blank=True, null=True, on_delete=models.CASCADE)
    initial_status = models.CharField(blank=True, null=True,
                                      choices=TASK_STATUSES, max_length=32)
    metadata = JSONField(blank=True, default=dict)

    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name="tasks")
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)

    max_annotations = models.IntegerField(default=0)
    multiple_annotations = models.BooleanField(default=False)
    permanent_task = models.BooleanField(default=False)

    order = models.IntegerField(default=0)

    def next_item(self, user, item):
        return self.strategy.next(self, user, item)

    def prev_item(self, user, item):
        return self.strategy.prev(self, user, item)

    def exclude_items_with_user_annotations(self, items, user):
        q = items.filter(Q(annotations__user=user) & Q(annotations__annotated=True))
        return items.exclude(id__in=q)

    def annotate_annotations_done(self, items):
        return items.annotate(
            annotations_done=models.Count(models.Case(
                models.When(
                    Q(annotations__annotated=True) &
                    Q(annotations__skipped=False) &
                    Q(annotations__rejected=False),
                    then=1
                ),
                output_field=IntegerField(),
            ))
        )

    def exclude_max_annotations(self, items):
        return items.filter(annotations_done__lt=self.max_annotations)

    @property
    def achievements_count(self):
        Achievement = a.models.Achievement
        return Achievement.objects.filter(task=self).count()

    @property
    def total_exp(self):
        Item = t.models.Item
        return Item.objects.filter(task=self).aggregate(models.Sum("exp"))['exp__sum']

    class Meta:
        ordering = ['order']

    def __str__(self):
        return "{}({})".format(
            self.__class__.__name__,
            'name='+self.name,
        )
