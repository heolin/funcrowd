from django.urls import path

from tasks.api.views.mission import MissionList, MissionDetail
from tasks.api.views.mission_progress import UserMissionProgressList, UserMissionProgressDetail, AddBonusExpView
from tasks.api.views.task import TaskDetail, MissionTasksList
from tasks.api.views.item import TaskNextItem, TaskNextItemWithPrevious
from tasks.api.views.annotation import AnnotationDetail
from tasks.api.views.task_progress import UserTaskProgressList, UserTaskProgressDetail

urlpatterns = [
    path('missions/', MissionList.as_view(), name='missions'),
    path('missions/progress/', UserMissionProgressList.as_view(), name='missions_progress'),
    path('missions/<int:mission_id>/', MissionDetail.as_view(), name="mission"),
    path('missions/<int:mission_id>/progress/', UserMissionProgressDetail.as_view(), name='mission_progress'),
    path('missions/<int:mission_id>/bonus_exp/', AddBonusExpView.as_view(), name='bonus_exp_view'),
    path('missions/<int:mission_id>/tasks/', MissionTasksList.as_view(), name='mission_tasks_list'),
    path('missions/<int:mission_id>/tasks/progress/', UserTaskProgressList.as_view(), name='mission_tasks_progress'),

    path('tasks/<int:task_id>/', TaskDetail.as_view(), name='task_detail'),
    path('tasks/<int:task_id>/progress/', UserTaskProgressDetail.as_view(), name='task_progress'),
    path('tasks/<int:task_id>/next_item/', TaskNextItem.as_view(), name='task_next_item'),

    path('items/<int:item_id>/next_item/', TaskNextItemWithPrevious.as_view(), name='task_next_item_with_previous'),
    path('items/<int:item_id>/annotation/', AnnotationDetail.as_view(), name='annotation_detail'),
]
