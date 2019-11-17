from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from modules.packages.api.views.dump import MissionDumpView
from modules.packages.api.views.package import NextPackage


urlpatterns = [
    path('missions/<int:mission_id>/next_package/', NextPackage.as_view(), name='mission_next_package'),
    path('missions/<int:mission_id>/dump/<str:file_name>/', MissionDumpView.as_view(), name='mission_data_dump'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
