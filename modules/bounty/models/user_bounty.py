# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models

from users.models.end_workers import EndWorker
from modules.bounty.consts import BountyStatus, STATUSES
from modules.bounty.models.bounty import Bounty
from modules.bounty.models.utils import get_reward_token
import tasks.models as m


class UserBounty(models.Model):
    bounty = models.ForeignKey(Bounty, on_delete=models.CASCADE, related_name="user_bounties")
    user = models.ForeignKey(EndWorker, blank=True, null=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUSES, default=BountyStatus.NEW)

    annotations_initial = models.IntegerField(default=0)
    annotations_done = models.IntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    reward_token = models.CharField(max_length=32, default=get_reward_token)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return "UserBounty (#{}): Bounty: {} - User: {}".format(
            self.id, self.bounty, self.user)

    def get_annotations_count(self):
        return m.annotation.Annotation.objects.filter(
            item__task=self.bounty.task,
            annotated=True,
            skipped=False,
            user=self.user).count()

    def update(self):
        if self.bounty.closed:
            return

        annotations_count = self.get_annotations_count()
        self.annotations_done = min(annotations_count - self.annotations_initial, self.bounty.annotations_target)

        if self.status == BountyStatus.NEW and self.annotations_done > 0:
            self.status = BountyStatus.IN_PROGRESS
        if self.status == BountyStatus.IN_PROGRESS and self.annotations_done >= self.bounty.annotations_target:
            self.status = BountyStatus.FINISHED

        self.save()

    def finish(self):
        if self.status != BountyStatus.CLOSED:
            self.status = BountyStatus.FINISHED
            self.save()

    def close(self):
        self.status = BountyStatus.CLOSED
        self.save()

    @property
    def progress(self):
        return min(self.annotations_done / self.bounty.annotations_target, 1.0)

    @property
    def reward(self):
        if self.progress >= 1.0:
            return self.reward_token
        return None

