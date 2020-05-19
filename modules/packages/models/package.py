# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from typing import Tuple

from django.db import models

from django.contrib.postgres.fields import JSONField

from tasks.consts import STATUSES, NEW, IN_PROGRESS, FINISHED, VERIFICATION
from modules.packages.models.mission_packages import MissionPackages
import numpy as np

from users.models import EndWorker
from django.apps import apps


class Package(models.Model):
    """
    Packages are used to store multiple items in one group. Items within the package
    may come from one, or multiple Tasks.
    They provide a mechanism which allows to track progress of package completion
    by a certain EndWorker.
    """

    parent = models.ForeignKey(MissionPackages, on_delete=models.CASCADE, related_name="packages")
    order = models.IntegerField(default=0)
    name = models.CharField(max_length=100, default="")
    status = models.CharField(max_length=20, choices=[(v, v) for v in STATUSES], default=NEW)
    metadata = JSONField(blank=True, null=True)

    def __str__(self):
        return "Package(mission={}, name={}, order={})".format(self.parent.mission.id, self.name, self.order)

    class Meta:
        ordering = ['order']

    def _get_aggregations(self) -> Tuple[float, float]:
        ItemAggregation = apps.get_model("aggregation.ItemAggregation")
        aggregations = ItemAggregation.objects.filter(item__package=self)

        probabilities = [a.get_probability() for a in aggregations]

        support = np.max([a.get_support() for a in aggregations])
        probability = np.min(probability)
        return np.min(probabilities), np.min(support)

    def update_status(self):
        print("TO SIE W OGOLE DZIEJE?")
        print("xxxxxxxxx\n"*5)
        max_annotations = self.parent.max_annotations
        print([a.get_support() for a in aggregations])

        if self.status in [NEW, IN_PROGRESS]:
            if max_annotations == 0:
                if support >= 1:
                    self.status = IN_PROGRESS
                    self.save()
            else:
                if support >= int(max_annotations / 2) and probability > 0.5:
                    self.status = FINISHED
                    self.save()
                elif support >= max_annotations:
                    self.status = VERIFICATION
                    self.save()
                elif support >= 1:
                    self.status = IN_PROGRESS
                    self.save()

    def get_user_progress(self, user: EndWorker):
        """
        Gets or creates a UserBounty objects for this package and a given user.
        Object is created only if Bounty is still opened.

        :param user: EndWorker
        :return user_bounty: UserBounty
        """
        UserPackageProgress = apps.get_model("packages.UserPackageProgress")

        package_progress = UserPackageProgress.objects.filter(
            package=self,
            user=user
        ).first()

        # create user bounty only if bounty is not still opened
        if not package_progress and not self.parent.closed:
            package_progress = UserPackageProgress.objects.create(
                package=self,
                user=user
            )
        return package_progress

