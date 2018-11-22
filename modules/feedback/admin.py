# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from modules.feedback.models.feedback import Feedback
from modules.feedback.models.feedback_field import FeedbackField
from modules.feedback.models.feedback_score_field import FeedbackScoreField

admin.site.register(Feedback)
