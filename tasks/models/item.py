# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.apps import apps
from django.contrib.postgres.fields import JSONField
from django.db import models

from modules.aggregation.aggregators import BaseAggregator
from modules.packages.models.package import Package
from tasks.consts import STATUSES, NEW, IN_PROGRESS, FINISHED, VERIFICATION
from tasks.models.annotation import Annotation


class Item(models.Model):
    data = JSONField()
    task = models.ForeignKey("Task", on_delete=models.CASCADE, related_name="items")
    package = models.ForeignKey(Package, null=True, blank=True,
                                on_delete=models.CASCADE, related_name="items")
    template = models.ForeignKey("ItemTemplate", on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[(v, v) for v in STATUSES], default=NEW)
    order = models.IntegerField(default=0)
    exp = models.IntegerField(default=0, blank=True, null=True)

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

    def get_default_annotation_data(self):
        data = {}
        for field in self.template.annotations_fields.all():
            default_value = ""
            if field.default_value:
                default_value = self.data.get(field.default_value.name, "")
            data[field.name] = default_value
        return data

    def get_or_create_annotation(self, user):
        annotation, created = None, False
        if not self.task.multiple_annotations:
            annotation = self.annotations.filter(item=self, user=user).first()
        else:
            annotation = self.annotations.filter(item=self, user=user, annotated=False).first()

        if not annotation:
            data = self.get_default_annotation_data()
            annotation = Annotation.objects.create(item=self, user=user, data=data)
            created = True

        return annotation, created

    def update_status(self):
        if not self.annotations.count():
            return

        ItemAggregation = apps.get_model("aggregation.ItemAggregation")

        if self.template.annotations_fields.count():
            BaseAggregator(self.task, self).aggregate()
            aggregation = ItemAggregation.objects.filter(item=self).first()

            max_annotations = self.task.max_annotations
            probability = aggregation.get_probability()
            annotations_count = aggregation.get_support()

            if self.status in [NEW, IN_PROGRESS]:
                if max_annotations == 0:
                    if annotations_count >= 1:
                        self.status = IN_PROGRESS
                        self.save()
                else:
                    if annotations_count >= int(max_annotations / 2) and probability > 0.5:
                        self.status = FINISHED
                        self.save()
                    elif annotations_count >= max_annotations:
                        self.status = VERIFICATION
                        self.save()
                    elif annotations_count >= 1:
                        self.status = IN_PROGRESS
                        self.save()

            if self.package:
                self.package.update_status()
