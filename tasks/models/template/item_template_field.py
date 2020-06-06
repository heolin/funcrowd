# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from tasks.field_types import TYPES, STR


class ItemTemplateField(models.Model):
    """

    """

    name = models.CharField(max_length=30)
    label = models.CharField(max_length=250, default="", blank=True)
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

