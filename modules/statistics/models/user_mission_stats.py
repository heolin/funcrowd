# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from modules.statistics.models.utils.agreement_ranking import get_agreement_ranking_mission
import tasks as t
import modules.feedback as f

HIGH_AGREEMENT_THRESHOLD = 0.5


class UserMissionStats(models.Model):
    user = models.ForeignKey("users.EndWorker", on_delete=models.CASCADE, null=True,
                             related_name="+")
    mission = models.ForeignKey("tasks.Mission", on_delete=models.CASCADE, null=True,
                                related_name='+')
    agreement_ranking_position = models.IntegerField(default=0)
    agreement_ranking_percentage = models.FloatField(default=0)

    annotated_items = models.IntegerField(default=0)
    high_agreement_count = models.IntegerField(default=0)
    annotated_documents = models.IntegerField(default=0)
    high_agreement_percentage = models.FloatField(default=0)

    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Stats (#{}): Mission: {}".format(
            self.id, self.mission)

    def update(self):
        self.annotated_items = t.models.Annotation.objects.filter(
            user=self.user).filter(item__task__mission=self.mission).filter(
            skipped=False).values("item").distinct().count()

        self.annotated_documents = t.models.Annotation.objects.filter(
            user=self.user).filter(item__task__mission=self.mission).filter(
            skipped=False).values("item__package").distinct().count()

        self.high_agreement_count = f.models.annotation_feedback.AnnotationFeedback.objects.filter(
            annotation__item__task__mission=self.mission).filter(
            annotation__user=self.user).filter(
            annotation__skipped=False).filter(
            score__gte=HIGH_AGREEMENT_THRESHOLD).count()

        self.high_agreement_percentage = 0
        if self.annotated_items:
            self.high_agreement_percentage = self.high_agreement_count / self.annotated_items

        self.save()

    def update_agreement_ranking(self):
        self.agreement_ranking_position, self.agreement_ranking_percentage \
            = get_agreement_ranking_mission(self.mission, self.high_agreement_count)
        self.save()
