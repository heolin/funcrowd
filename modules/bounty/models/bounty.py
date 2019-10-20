# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models

import modules.bounty as b

from modules.bounty.consts import NEW, IN_PROGRESS, FINISHED, CLOSED
from tasks.models.task import Task
from users.models import EndWorker
from modules.bounty.exceptions import OnlyOneActiveBountyPerTask


class Bounty(models.Model):
    annotations_target = models.IntegerField(default=50)
    closed = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="bounties")

    def __str__(self):
        return "Bounty (#{}): Task: {} - Target: {}".format(
            self.id, self.task, self.annotations_target)

    def close(self):
        self.closed = True
        self.save()
        for user_bounty in self.user_bounties.all():
            user_bounty.close()

    def finish(self):
        for user_bounty in self.user_bounties.all():
            user_bounty.finish()

    def save(self, *args, **kwargs):
        if not self.id:
            if Bounty.objects.filter(task=self.task, closed=False).first():
                raise OnlyOneActiveBountyPerTask
        return super(Bounty, self).save(*args, **kwargs)

    def _create_user_bounty(self, user: EndWorker):
        UserBounty = b.models.UserBounty
        user_bounty = UserBounty.objects.create(user=user, bounty=self)
        user_bounty.annotations_initial = user_bounty.get_annotations()
        user_bounty.save()
        return user_bounty

    def get_or_create_user_bounty(self, user: EndWorker):
        UserBounty = b.models.UserBounty
        user_bounty = UserBounty.objects.filter(user=user, bounty=self).first()
        created = False

        if not user_bounty and not self.closed:
            user_bounty = self._create_user_bounty(user)
            created = True

        return user_bounty, created

    def create_first_or_next_user_bounty(self, user: EndWorker):
        user_bounty, created = self.get_or_create_user_bounty(user)

        # Bounty closed and user bounty does not exist
        if self.closed and not created:
            return None, False

        # User bounty exist but not finished
        if user_bounty.status in [NEW, IN_PROGRESS]:
            return user_bounty, created

        # User bounty finished
        if user_bounty.status == FINISHED:
            user_bounty.status = CLOSED
            user_bounty.save()

        user_bounty = self._create_user_bounty(user)
        return user_bounty, True
