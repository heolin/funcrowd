# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models

from tasks.models.task import Task


class Bounty(models.Model):
    annotations_target = models.IntegerField(default=50)
    closed = models.BooleanField(default=False)
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
            for bounty in Bounty.objects.filter(task=self.task, closed=False):
                bounty.close()
        return super(Bounty, self).save(*args, **kwargs)
