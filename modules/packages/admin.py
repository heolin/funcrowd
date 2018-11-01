# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from modules.packages.models import (
    MissionPackages
)

admin.site.register(MissionPackages)
