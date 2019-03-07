# -*- coding: utf-8 -*-annotationannotation

from __future__ import unicode_literals
from django.db import models
from django.contrib.postgres.fields import JSONField

from tasks.models.item import Item
import numpy as np


class ItemAggregation(models.Model):
    data = JSONField(blank=True, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="aggregations")
    created = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=20, choices=None)

    class Meta:
        verbose_name_plural = "ItemAggregations"

    def __str__(self):
        return "{}({})".format(
            self.__class__.__name__,
            self.item
            )

    def get_probability(self):
        values = []
        for key, value in self.data.items():
            if not key.endswith("_prob"):
                continue
            if type(value) is str:
                values.extend(map(float, value.split(',')))
            else:
                values.append(value)

        if values:
            return np.average(values)

    def get_support(self):
        values = []
        for key, value in self.data.items():
            if not key.endswith("_support"):
                continue
            if type(value) is str:
                values.extend(map(int, value.split(',')))
            else:
                values.append(value)
        if values:
            return np.max(values)
