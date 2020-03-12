from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from modules.packages.api.views.dump import MissionDumpView
from modules.packages.api.views.package import NextPackageView
from modules.packages.api.views.search import PackageSearchAggregatedStatsView

urlpatterns = [
    path('missions/<int:mission_id>/next_package/', NextPackageView.as_view(), name='mission_next_package'),
    path('missions/<int:mission_id>/dump/<str:file_name>/', MissionDumpView.as_view(), name='mission_data_dump'),
    path('missions/<int:mission_id>/search/stats/', PackageSearchAggregatedStatsView.as_view(),
         name='search_package_aggregation'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
