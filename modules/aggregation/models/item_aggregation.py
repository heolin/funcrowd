# -*- coding: utf-8 -*-annotationannotation

from __future__ import unicode_literals
from django.db import models
from django.contrib.postgres.fields import JSONField

from tasks.models.item import Item


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

