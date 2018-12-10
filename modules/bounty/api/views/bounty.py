# -*- coding: utf-8 -*-

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from modules.bounty.models import Bounty
from modules.bounty.serializers.bounty import BountySerializer


class BountyListView(GenericAPIView):
    serializer_class = BountySerializer

    def get(self, request, *args, **kwargs):
        bounties = Bounty.objects.all()
        serializer = self.serializer_class(bounties, many=True)
        return Response(serializer.data)

