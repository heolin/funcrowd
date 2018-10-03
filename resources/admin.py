from django.contrib import admin

from resources.models import ExcelFile, Image, Text

admin.site.register(ExcelFile)
admin.site.register(Image)
admin.site.register(Text)

