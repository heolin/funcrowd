from django.urls import path

from modules.statistics.api.views import (
    GlobalStatsView, UserMissionStatsView, MissionStatsView, UserStatsView
)


urlpatterns = [
    path('stats/missions/<int:mission_id>/', MissionStatsView.as_view(), name='mission_stats_view'),
    path('stats/users/<int:user_id>/missions/<int:mission_id>/', UserMissionStatsView.as_view(),
         name='user_mission_stats_view'),
    path('stats/users/<int:user_id>/', UserStatsView.as_view(), name='user_stats_view'),
    path('stats/', GlobalStatsView.as_view(), name='global_stats_view'),
]
