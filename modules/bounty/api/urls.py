from django.urls import path

from modules.bounty.api.views.user_bounty import BountyStatusView
from modules.bounty.api.views.bounty import BountyListView


urlpatterns = [
    path('bounty/<int:bounty_id>/status', BountyStatusView.as_view(), name='bounty_status'),
    path('bounty/', BountyListView.as_view(), name='bounty_list'),
]
