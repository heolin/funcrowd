# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from tasks.field_types import TYPES, STR
from sortedm2m.fields import SortedManyToManyField

"""
"""


class ItemTemplateField(models.Model):
    name = models.CharField(max_length=30)
    label = models.CharField(max_length=200, default="", blank=True)
    type = models.CharField(max_length=10, choices=TYPES, default=STR)
    widget = models.CharField(max_length=30)
    comment = models.CharField(max_length=30, default="", blank=True, null=True)

    editable = models.BooleanField(default=False)
    required = models.BooleanField(default=True)
    feedback = models.BooleanField(default=False)
    validate_data_source = models.BooleanField(default=True)

    data_source = models.ForeignKey("ItemTemplateField", on_delete=models.CASCADE,
                                    null=True, blank=True, related_name="+")
    default_value = models.ForeignKey("ItemTemplateField", on_delete=models.CASCADE,
                                      null=True, blank=True, related_name="+")

    def __str__(self):
        return "{}({}, {})".format(self.name, self.widget, self.comment)


class ItemTemplate(models.Model):
    name = models.CharField(max_length=100)
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
