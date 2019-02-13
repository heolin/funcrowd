# -*- coding: utf-8 -*-

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from modules.bounty.models import Bounty, UserBounty
from modules.bounty.serializers.user_bounty import UserBountySerializer


class BountyStatusView(GenericAPIView):
    serializer_class = UserBountySerializer

    def get(self, request, bounty_id, *args, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        if bounty:
            user_bounty, _ = UserBounty.get_or_create(bounty, request.user)
            if user_bounty:
                user_bounty.update()
            serializer = self.serializer_class(user_bounty)
            return Response(serializer.data)
        raise NotFound("No Bounty found for given id.")