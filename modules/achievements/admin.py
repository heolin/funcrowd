# -*- coding: utf-7 -*-
from __future__ import unicode_literals

from django.contrib import admin
from modules.achievements.models import (
    Achievement,
    ProgressAchievement,
    ItemDoneAchievement,
    LoginCountAchievement,
    AssignSpaceCalcGroupAchievement,
    UnlockMissionAfterTaskAchievement
)


admin.site.register(ProgressAchievement)
admin.site.register(ItemDoneAchievement)
admin.site.register(LoginCountAchievement)
admin.site.register(AssignSpaceCalcGroupAchievement)
admin.site.register(UnlockMissionAfterTaskAchievement)
