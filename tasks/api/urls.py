from django.urls import path

from tasks.api.views.mission import MissionList, MissionDetail
from tasks.api.views.task import TaskDetail, MissionTasksList
from tasks.api.views.item import TaskNextItem, TaskNextItemWithPrevious
from tasks.api.views.annotation import AnnotationDetail


urlpatterns = [
    path('missions', MissionList.as_view(), name='missions'),
    path('missions/<int:mission_id>', MissionDetail.as_view(), name="mission"),
    path('missions/<int:mission_id>/tasks', MissionTasksList.as_view(), name='mission_tasks_list'),

    path('tasks/<int:task_id>', TaskDetail.as_view(), name='task_detail'),
    path('tasks/<int:task_id>/next_item', TaskNextItem.as_view(), name='task_next_item'),

    path('items/<int:item_id>/next_item', TaskNextItemWithPrevious.as_view(), name='task_next_item_with_previous'),
    path('items/<int:item_id>/annotation', AnnotationDetail.as_view(), name='annotation_detail'),
]

"""
urlpatterns = [
    url(r'tasks/(?P<task_id>[0-9]*)/items/(?P<item_id>[0-9]*)/annotations',
        TaskItemAnnotation.as_view(), name='task_annotations'),
    url(r'tasks/(?P<task_id>[0-9]*)/items/(?P<item_id>[0-9]*)$',
        TaskItemDetail.as_view(), name='task_item_detail'),
    url(r'tasks/(?P<task_id>[0-9]*)/next_item',
        TaskNextItem.as_view(), name='task_next_item'),
    url(r'tasks/(?P<task_id>[0-9]*)$',
        TaskDetail.as_view(), name='task_detail'),
]
"""
