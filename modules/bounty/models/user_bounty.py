# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models

from users.models.end_workers import EndWorker
from modules.bounty.consts import STATUSES, NEW, IN_PROGRESS, FINISHED, CLOSED
from modules.bounty.models.bounty import Bounty
from modules.bounty.models.utils import get_reward_token
from modules.bounty.exceptions import OnlyOneActiveBountyPerTask
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
        if UserBounty.objects.exclude(bounty=bounty
                                      ).filter(user=user,
                                               bounty__task=bounty.task,
                                               status__in=[NEW, IN_PROGRESS]).first():
            raise OnlyOneActiveBountyPerTask("This user has already an active bounty for Task {}".format(
                bounty.task.id))

        bounty, created = UserBounty.objects.get_or_create(user=user, bounty=bounty)
        if created:
            bounty.annotations_initial = bounty._get_annotations()
            bounty.save()
        return bounty, created

    def __str__(self):
        return "UserBounty (#{}): Bounty: {} - User: {}".format(
            self.id, self.bounty, self.user)

    def _get_annotations(self):
        return m.annotation.Annotation.objects.filter(
            item__task=self.bounty.task,
            user=self.user).count()

    def update(self):
        annotations_count = self._get_annotations()
        self.annotations_done = annotations_count - self.annotations_initial

        if self.status == NEW and self.annotations_done > 0:
            self.status = IN_PROGRESS
        if self.status == IN_PROGRESS and self.annotations_done >= self.bounty.annotations_target:
            self.status = FINISHED

        self.save()

    def close(self):
        self.status = CLOSED
        self.save()

    @property
    def progress(self):
        return self.annotations_done / self.bounty.annotations_target

    @property
    def reward(self):
        if self.progress >= 1.0:
            return self.reward_token
        return None

