from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from modules.packages.api.views import (
    PackageSearchAggregatedStatsView, NextPackageView,
    MissionDumpView, CreatePackageView, PackageView,
    PackageNextItemView, PackageProgressView,
    PackagesProgressListView
)


urlpatterns = [
    path('missions/<int:mission_id>/next_package/', NextPackageView.as_view(), name='mission_next_package'),
    path('missions/<int:mission_id>/dump/<str:file_name>/', MissionDumpView.as_view(), name='mission_data_dump'),
    path('missions/<int:mission_id>/search/stats/', PackageSearchAggregatedStatsView.as_view(),
         name='search_package_aggregation'),
    path('missions/<int:mission_id>/create_package/', CreatePackageView.as_view(), name='create_package'),
    path('packages/<int:package_id>/items/next/', PackageNextItemView.as_view(), name='package_next_item'),
    path('packages/<int:package_id>/', PackageView.as_view(), name='package_details'),
    path('packages/<int:package_id>/status/', PackageProgressView.as_view(), name='package_status'),
    path('packages/status/', PackagesProgressListView.as_view(), name='package_status'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
