# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models


class UserStats(models.Model):
    items_done = models.IntegerField(default=0)
    user = models.OneToOneField("users.EndWorker", on_delete=models.CASCADE,
                                null=True, related_name="local_stats")

    def __str__(self):
        return "Stats (#{}): User: {}".format(
            self.id, self.user)

