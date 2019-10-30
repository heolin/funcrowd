from django.urls import path

from modules.bounty.api.views.user_bounty import BountyStatusView, StartBountyView
from modules.bounty.api.views.bounty import BountyListView, BountyDetailsView


urlpatterns = [
    path('bounty/<int:bounty_id>/status', BountyStatusView.as_view(), name='bounty_status'),
    path('bounty/<int:bounty_id>/start', StartBountyView.as_view(), name='bounty_start'),
    path('bounty/<int:bounty_id>', BountyDetailsView.as_view(), name='bounty_view'),
    path('bounty/', BountyListView.as_view(), name='bounty_list'),
]
