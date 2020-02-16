# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models

from modules.packages.models import Package
from modules.packages.consts import UserPackageStatus, USER_PACKAGE_STATUSES
from tasks.models import Annotation

from users.models.end_workers import EndWorker


class UserPackageProgress(models.Model):
    user = models.ForeignKey(EndWorker, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE,
                                related_name="progress")
    items_done = models.IntegerField(default=0)
    status = models.CharField(choices=USER_PACKAGE_STATUSES,
                              default=UserPackageStatus.NONE,
                              max_length=32)

    def __str__(self):
        return f"UserPackageProgress({self.user}, {self.package}, {self.status})"

    def update(self):
        self.items_done = Annotation.objects.filter(
            annotated=True, skipped=False, rejected=False,
            item__package=self.package, user=self.user
        ).values("item").distinct().count()

        self.update_status(False)
        self.save()

    def update_status(self, commit=True):
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
        if self.items_count:
            return self.items_done / self.items_count

    @property
    def items_count(self):
        return self.package.items.count()
