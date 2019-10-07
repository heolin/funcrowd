# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models

from users.models.end_workers import EndWorker
from modules.bounty.consts import STATUSES, NEW, IN_PROGRESS, FINISHED, CLOSED
from modules.bounty.models.bounty import Bounty
from modules.bounty.models.utils import get_reward_token
from modules.bounty.exceptions import OnlyOneActiveBountyPerTask, BountyFinished
import tasks.models as m


class UserBounty(models.Model):
    bounty = models.ForeignKey(Bounty, on_delete=models.CASCADE, related_name="user_bounties")
    user = models.ForeignKey(EndWorker, blank=True, null=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[(v, v) for v in STATUSES], default=NEW)
    annotations_initial = models.IntegerField(default=0)
    annotations_done = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    reward_token = models.CharField(max_length=32, default=get_reward_token)

    @staticmethod
    def get_or_create(bounty: Bounty, user: EndWorker):
        user_bounty = UserBounty.objects.filter(user=user, bounty=bounty).first()
        created = False

        if not UserBounty.objects.exclude(bounty=bounty).filter(
                user=user, bounty__task=bounty.task, status__in=[NEW, IN_PROGRESS]).first():
            if not user_bounty and not bounty.closed:
                user_bounty = UserBounty.objects.create(user=user, bounty=bounty)
                user_bounty.annotations_initial = user_bounty._get_annotations()
                user_bounty.save()
                created = True
        return user_bounty, created

    def __str__(self):
        return "UserBounty (#{}): Bounty: {} - User: {}".format(
            self.id, self.bounty, self.user)

    def _get_annotations(self):
        return m.annotation.Annotation.objects.filter(
            item__task=self.bounty.task,
            annotated=True,
            skipped=False,
            user=self.user).count()

    def update(self):
        if self.bounty.closed:
            return

        annotations_count = self._get_annotations()
        self.annotations_done = min(annotations_count - self.annotations_initial, self.bounty.annotations_target)

        if self.status == NEW and self.annotations_done > 0:
            self.status = IN_PROGRESS
        if self.status == IN_PROGRESS and self.annotations_done >= self.bounty.annotations_target:
            self.status = FINISHED

        self.save()

    def finish(self):
        if self.status != CLOSED:
            self.status = FINISHED
            self.save()

    def close(self):
        self.status = CLOSED
        self.save()

    @property
    def progress(self):
        return min(self.annotations_done / self.bounty.annotations_target, 1.0)

    @property
    def reward(self):
        if self.progress >= 1.0:
            return self.reward_token
        return None

