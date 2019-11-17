from django.urls import path

from modules.achievements.api.views.user_achievement import AchievementsList, MissionAchievementsList, \
    UnclosedAchievementsList, TaskAchievementsList


urlpatterns = [
    path('achievements/', AchievementsList.as_view(), name='achievements_list'),
    path('achievements/unclosed/', UnclosedAchievementsList.as_view(), name='unclosed_achievements_list'),
    path('achievements/mission/<int:mission_id>/', MissionAchievementsList.as_view(), name='mission_achievements_list'),
    path('achievements/task/<int:task_id>/', TaskAchievementsList.as_view(), name='tasks_achievements_list'),
]