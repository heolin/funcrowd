from django.urls import path

from modules.bounty.api.views.user_bounty import BountyStatusView


urlpatterns = [
    path('bounty/<int:bounty_id>/status', BountyStatusView.as_view(), name='bounty_status'),
]
