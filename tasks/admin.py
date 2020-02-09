# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from tasks.models import (
    Task, ItemTemplate, ItemTemplateField,
    Item, Annotation, Mission,
    UserTaskProgress, UserMissionProgress)


admin.site.register(Mission)
admin.site.register(Task)
admin.site.register(UserTaskProgress)
admin.site.register(UserMissionProgress)
admin.site.register(ItemTemplateField)
admin.site.register(ItemTemplate)
admin.site.register(Annotation)
admin.site.register(Item)
