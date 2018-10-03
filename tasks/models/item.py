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
    template = models.ForeignKey("ItemTemplate", on_delete=models.CASCADE)
    order = models.IntegerField(default=0)

    def __str__(self):
        return "Task {} (#{}) - Item {} - {} (#{}) - {}".format(self.task.order, self.task.id,
                                                                self.order, self.template.name,
                                                                self.id, self.task.mission.title)

    class Meta:
        ordering = ['task_id', 'order']

    def check_fields(self):
        template_fields = {field.name for field in self.template.items_fields.all()}
        item_fields = set(self.data.keys())
        return len(item_fields - template_fields) == 0

    @property
    def index(self):
        return self.task.items.filter(order__lte=self.order).count()

    @property
    def next_item(self):
        return self.task.get_next_item(self)

    @property
    def previous_item(self):
        return self.task.get_previous_item(self)

    def get_or_create_annotation(self, user):
        annotation = self.annotations.filter(item=self, user=user)
        annotation = annotation.first()
        created = False
        if not annotation:
            annotation = Annotation.objects.create(item=self,
                                                   user=user,
                                                   data={})
            created = True
        return annotation, created
