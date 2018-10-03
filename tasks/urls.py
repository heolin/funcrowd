from django.urls import path, include

urlpatterns = [
]

"""
    url(r'tasks/(?P<task_id>[0-9]*)/items/(?P<item_id>[0-9]*)/next', NextItemView.as_view(), name='next_item_view'),
    url(r'tasks/(?P<task_id>[0-9]*)/items/(?P<item_id>[0-9]*)', ItemView.as_view(), name='item_view'),
    url(r'tasks/(?P<task_id>[0-9]*)', TaskView.as_view(), name='task_view'),
    url(r'missions/(?P<mission_id>[0-9]*)$', TasksListView.as_view(), name='tasks_list'),
]
"""
