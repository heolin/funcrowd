# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from sortedm2m.fields import SortedManyToManyField

"""
"""


class ItemTemplateField(models.Model):
    name = models.CharField(max_length=30)
    widget = models.CharField(max_length=30)
    editable = models.BooleanField(default=False)
    required = models.BooleanField(default=True)
    data_source = models.ForeignKey("ItemTemplateField", on_delete=models.CASCADE, null=True, blank=True)


class ItemTemplate(models.Model):
    name = models.CharField(max_length=30)
    fields = SortedManyToManyField("ItemTemplateField", related_name="template")

    @property
    def annotations_fields(self):
        return self.fields.filter(editable=True)

    @property
    def items_fields(self):
        return self.fields.filter(editable=False)

    class Meta:
        ordering = ['id']