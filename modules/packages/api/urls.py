from django.urls import path

from modules.packages.api.views.package import NextPackage


urlpatterns = [
    path('missions/<int:mission_id>/next_package', NextPackage.as_view(), name='mission_next_packaeg'),
]
