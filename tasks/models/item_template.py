# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from tasks.field_types import TYPES, STR
from sortedm2m.fields import SortedManyToManyField

"""
"""


class ItemTemplateField(models.Model):
    name = models.CharField(max_length=30)
    widget = models.CharField(max_length=30)
    editable = models.BooleanField(default=False)
    required = models.BooleanField(default=True)
    feedback = models.BooleanField(default=False)
    type = models.CharField(max_length=10, choices=TYPES, default=STR)
    data_source = models.ForeignKey("ItemTemplateField", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return "{}({})".format(self.name, self.widget)


class ItemTemplate(models.Model):
    name = models.CharField(max_length=30)
    fields = SortedManyToManyField("ItemTemplateField", related_name="template")

    def __str__(self):
        return "{}".format(self.name)

    @property
    def annotations_fields(self):
        return self.fields.filter(editable=True)

    @property
    def feedback_fields(self):
        return self.fields.filter(feedback=True, editable=True)

    @property
    def items_fields(self):
        return self.fields.filter(editable=False)

    class Meta:
        ordering = ['id']
