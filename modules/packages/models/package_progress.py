# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from typing import Optional

from django.apps import apps
from django.db import models

from modules.packages.consts import UserPackageStatus, USER_PACKAGE_STATUSES
from modules.packages.models.utils import get_reward_token
from users.models.end_workers import EndWorker


class UserPackageProgress(models.Model):
    """
    Stores information about current progress of `EndWorker`'s annotation
    for selected `Package`.

    It generates `reward_token`, which is an unique token that can be used
    in mturk-like scenarios. If `EndWorker` finish annotations, the code will
    be available int the `reward` variable.
    """
    user = models.ForeignKey(EndWorker, on_delete=models.CASCADE)
    package = models.ForeignKey("Package", on_delete=models.CASCADE,
                                related_name="progress")
    items_done = models.IntegerField(default=0)
    status = models.CharField(choices=USER_PACKAGE_STATUSES,
                              default=UserPackageStatus.NONE,
                              max_length=32)

    reward_token = models.CharField(max_length=32, default=get_reward_token)

    def __str__(self):
        return f"UserPackageProgress({self.user}, {self.package}, {self.status})"

    def update(self):
        """
        Run after each annotation finished by the EndWorker.
        Updates `items_done` and `status`.
        """
        Annotation = apps.get_model("tasks.Annotation")

        self.items_done = Annotation.objects.filter(
            annotated=True, rejected=False,
            item__package=self.package, user=self.user
        ).values("item").distinct().count()

        self.update_status(False)
        self.save()

    def update_status(self, commit=True):
        """
        Updates status based on items annotated by the EndWorker.

        :param commit: if True, it will save changes to database
        """

        last_status = self.status
        if self.status == UserPackageStatus.NONE:
            if self.items_done > 0:
                self.status = UserPackageStatus.IN_PROGRESS
        if self.status == UserPackageStatus.IN_PROGRESS:
            if self.items_done == self.items_count:
                self.status = UserPackageStatus.FINISHED

        if commit and last_status != self.status:
            self.save()

    @property
    def progress(self):
        """
        Percentage value of how many items were already annotated by this user
        """
        if self.items_count:
            return self.items_done / self.items_count

    @property
    def items_count(self):
        return self.package.items.count()

    @property
    def reward(self) -> Optional[str]:
        """
        If the user finished annotation for this package, it will return an unique code.
        This code can be used to award the price in systems like `mturk`.
        """
        if self.progress >= 1.0:
            return self.reward_token
        return None

