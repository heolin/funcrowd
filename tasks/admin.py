# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from tasks.models import (
    Task, ItemTemplate, ItemTemplateField, Item, Annotation, Mission
)

admin.site.register(Mission)
admin.site.register(Task)
admin.site.register(ItemTemplateField)
admin.site.register(ItemTemplate)
admin.site.register(Annotation)
admin.site.register(Item)
