# -*- coding: utf-8 -*-

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from modules.bounty.models import Bounty
from modules.bounty.api.serializers import BountySerializer


class BountyListView(GenericAPIView):
    serializer_class = BountySerializer

    def get(self, request, *args, **kwargs):
        bounties = Bounty.objects.filter(hidden=False)
        serializer = self.serializer_class(bounties, many=True, context={"request": request})
        return Response(serializer.data)


class BountyDetailsView(GenericAPIView):
    serializer_class = BountySerializer

    def get(self, request, bounty_id, *args, **kwargs):
        bounty = Bounty.objects.get(id=bounty_id)
        serializer = self.serializer_class(bounty, context={"request": request})
        return Response(serializer.data)

