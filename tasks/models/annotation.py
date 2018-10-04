# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.postgres.fields import JSONField

from users.models.end_workers import EndWorker


class Annotation(models.Model):
    data = JSONField()
    item = models.ForeignKey("Item", on_delete=models.CASCADE, related_name="annotations")
    user = models.ForeignKey(EndWorker, blank=True, null=True, on_delete=models.CASCADE)
    feedback = models.TextField(default="", blank=True)
    is_done = models.BooleanField(default=False)
    is_correct = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    def verify_fields(self):
        annotations_fields = {field.name for field in self.item.template.annotations_fields.all()}
        data_fields = set(self.data.keys())
        return annotations_fields == data_fields

    def verify_done(self):
        self.is_done = True
        for field in self.item.template.annotations_fields:
            if field.required and not self.data[field.name]:
                self.is_done = False
                break
        return self.is_done

    def verify_correct(self):
        raise NotImplemented

    def __str__(self):
        TEMPLATE = "Task {} (#{}) - Item: {} (#{}) - Annotation: #{} - User: {}"
        return TEMPLATE.format(self.item.task.order, self.item.task.id,
                               self.item.order, self.item.id, self.id, self.user)
