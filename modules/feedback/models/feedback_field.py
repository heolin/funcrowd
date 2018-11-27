# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models

from .fields import FIELDS


class FeedbackField(models.Model):
    name = models.CharField(max_length=30)

    @property
    def _logic(self):
        return FIELDS[self.name]

    def evaluate(self, field_name, annotation):
        return self._logic(field_name).evaluate(annotation)

    def __str__(self):
        return "{}({})".format(
            self.__class__.__name__,
            'name='+self.name,
            )

    def save(self, *args, **kwargs):
        objects = self.__class__.objects.filter(name=self.name)
        if objects:
            self.pk = objects.first().pk
        super().save(*args, **kwargs)

    @staticmethod
    def register_values():
        # register all strategy
        for field_name in FIELDS:
            FeedbackField.objects.get_or_create(name=field_name)

