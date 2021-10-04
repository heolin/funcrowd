# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from typing import Tuple

import numpy as np
from django.apps import apps
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models import Q

from modules.packages.consts import PACKAGE_STATUSES, PackageStatus
from modules.packages.models.mission_packages import MissionPackages
from users.models import EndWorker


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
    status = models.CharField(max_length=20, choices=PACKAGE_STATUSES, default=PackageStatus.NONE)
    metadata = JSONField(blank=True, null=True)

    def __str__(self):
        return f"Package(mission={self.parent.mission.id}, name={self.name}, order={self.order})"

    class Meta:
        ordering = ['order']

    def _get_aggregations(self) -> Tuple[float, int, int]:
        """
        Computes aggregated values of probability, support, annotations_count
        for whole package based on its items' ItemAggregation objects.
        """
        ItemAggregation = apps.get_model("aggregation.ItemAggregation")
        aggregations = ItemAggregation.objects.filter(item__package=self)

        probabilities = [a.get_probability() for a in aggregations]
        supports = [a.get_support() for a in aggregations]
        annotations_counts = [a.get_annotations_count() for a in aggregations]

        # adds missing values, for items with no annotations - and no ItemAggregation object
        for _ in range(self.items.count() - aggregations.count()):
            probabilities.append(0.0)
            supports.append(0)
            annotations_counts.append(0)

        return np.min(probabilities), min(supports), min(annotations_counts)

    def update_status(self):
        """
        Sets the status of the package based on the number of finished annotations
        and probability of the answers.
        """
        probability, support, annotations_count = self._get_aggregations()
        max_annotations = self.parent.max_annotations

        if self.status in [PackageStatus.NONE, PackageStatus.IN_PROGRESS]:
            if max_annotations == 0:
                if annotations_count >= 1:
                    self.status = PackageStatus.IN_PROGRESS
                    self.save()
            else:
                if annotations_count >= int(max_annotations / 2) and probability > 0.5:
                    self.status = PackageStatus.FINISHED
                    self.save()
                elif annotations_count >= max_annotations:
                    self.status = PackageStatus.VERIFICATION
                    self.save()
                elif annotations_count >= 1:
                    self.status = PackageStatus.IN_PROGRESS
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

    def get_user_next_item(self, user):
        items = self.items.all()
        # exclude items already annotated by this user
        q = items.filter(Q(annotations__user=user) & Q(annotations__annotated=True))
        item = items.exclude(id__in=q).order_by("order").first()
        return item

    def close(self):
        """
        Used to close all existing UserPackageProgress objects,
        and block creating new UserPackageProgress for this Package.

        Changes status to `CLOSED` only if Package is not `is_completed` yet.
        """
        UserPackageProgress = apps.get_model("packages.UserPackageProgress")
        for user_bounty in UserPackageProgress.objects.filter(package=self):
            user_bounty.close()

        if not self.is_completed:
            self.status = PackageStatus.CLOSED
            self.save()

    @property
    def is_completed(self):
        """
        If True, it means annotations for this Package should not be continued.
        """
        return self.status in \
               [PackageStatus.CLOSED, PackageStatus.FINISHED, PackageStatus.VERIFICATION]
