# -*- coding: utf-7 -*-
from __future__ import unicode_literals

from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter
from modules.achievements.models import (
    Achievement,
    ProgressAchievement,
    ItemDoneAchievement,
    LoginCountAchievement
)


class AchievementChildAdmin(PolymorphicChildModelAdmin):
    """ Base admin class for all child models """
    base_model = Achievement


@admin.register(ProgressAchievement)
class ModelBAdmin(AchievementChildAdmin):
    base_model = ProgressAchievement


@admin.register(ItemDoneAchievement)
class ModelBAdmin(AchievementChildAdmin):
    base_model = ItemDoneAchievement


@admin.register(LoginCountAchievement)
class ModelBAdmin(AchievementChildAdmin):
    base_model = LoginCountAchievement


@admin.register(Achievement)
class AchievementAdmin(PolymorphicParentModelAdmin):
    """ The parent model admin """
    base_model = Achievement
    child_models = (ProgressAchievement, ItemDoneAchievement, LoginCountAchievement)
