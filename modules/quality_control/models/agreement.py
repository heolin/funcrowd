# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from .agreements import AGREEMENT_METRICS


class AgreementMetric(models.Model):
    name = models.CharField(max_length=30)

    def _logic(self, task):
        return AGREEMENT_METRICS[self.name](task)

    def evaluate(self, task):
        return self._logic(task).evaluate()

    class Meta:
        verbose_name_plural = "AgreementMetrics"

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
        # register all metrics
        for metric_name in AGREEMENT_METRICS:
            AgreementMetric.objects.get_or_create(name=metric_name)
