# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models


class Message(models.Model):
    name = models.CharField(max_length=30)
    subject = models.CharField(max_length=30)
    body = models.TextField()
