# -*- coding: utf-8 -*-

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status

from tasks.models import Item, Mission

from tasks.api.serializers.item import ItemSerializer


class NextPackage(GenericAPIView):
    serializer_class = ItemSerializer

    def get(self, request, mission_id, *args, **kwargs):
        mission = Mission.objects.filter(id=mission_id).first()
        if mission:
            next_item = mission.next_package(request.user, None)
            if next_item:
                serializer = self.serializer_class(next_item)
                return Response(serializer.data)
            return Response(None, status.HTTP_204_NO_CONTENT)
        raise NotFound("No Task found for given id.")

