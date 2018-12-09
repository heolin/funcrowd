# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models

from tasks.models.task import Task


class Bounty(models.Model):
    annotations_target = models.IntegerField(default=50)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="bounties")

    def __str__(self):
        return "Bounty (#{}): Task: {} - Target: {}".format(
            self.id, self.task, self.annotations_target)
