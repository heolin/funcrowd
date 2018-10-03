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

    def check_fields(self):
        for field in self.item.task.template.annotations_fields:
            if field.name not in self.data:
                return False
        return True

    def check_done(self):
        self.is_done = True
        for field in self.item.template.annotations_fields:
            if field.required and not self.data[field.name]:
                self.is_done = False
                break
        return self.is_done

    def check_correct(self):
        self.is_correct = True
        reference = self.item.annotations.filter(user=None).first()
        if reference:
            for field, value in self.data.items():
                if reference.data[field] != value:
                    self.is_correct = False
                    break

        return self.is_correct

    def __str__(self):
        TEMPLATE = "Task {} (#{}) - Item: {} (#{}) - Annotation: #{} - User: {}"
        return TEMPLATE.format(self.item.task.order, self.item.task.id,
                               self.item.order, self.item.id, self.id, self.user)
