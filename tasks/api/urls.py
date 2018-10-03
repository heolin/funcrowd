from django.urls import path

from tasks.api.views.mission import MissionList, MissionDetail


urlpatterns = [
    path('missions', MissionList.as_view(), name='missions'),
    path('missions/<int:mission_id>', MissionDetail.as_view(), name="mission")
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
