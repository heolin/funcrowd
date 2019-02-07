# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.fields import ArrayField

from tasks.models.annotation import Annotation
from tasks.models.item_template import ItemTemplate

import json


class Item(models.Model):
    data = JSONField()
    task = models.ForeignKey("Task", on_delete=models.CASCADE, related_name="items")
    document = models.ForeignKey("Document", null=True, blank=True,
                                 on_delete=models.CASCADE, related_name="items")
    template = models.ForeignKey("ItemTemplate", on_delete=models.CASCADE)
    order = models.IntegerField(default=0)

    def __str__(self):
        return "Task {} (#{}) - Item {} - {} (#{}) - {}".format(self.task.order, self.task.id,
                                                                self.order, self.template.name,
                                                                self.id, self.task.mission.name)

    class Meta:
        ordering = ['task_id', 'order']

    @property
    def index(self):
        return self.task.items.filter(order__lte=self.order).count()

    @property
    def next_item(self):
        raise NotImplemented

    @property
    def previous_item(self):
        raise NotImplemented

    def verify_fields(self):
        items_fields = {field.name for field in self.template.items_fields.all()}
        data_fields = set(self.data.keys())
        return items_fields == data_fields

    def get_or_create_annotation(self, user):
        annotation, created = None, False
        if not self.task.multiple_annotations:
            annotation = self.annotations.filter(item=self, user=user)
            annotation = annotation.first()
        if not annotation:
            data = {field.name: "" for field in self.template.annotations_fields.all()}
            annotation = Annotation.objects.create(item=self, user=user, data=data)
            created = True
        return annotation, created
