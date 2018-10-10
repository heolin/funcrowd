# -*- coding: utf-8 -*-

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from tasks.models import Mission

from tasks.api.serializers.mission import MissionSerializer


class MissionList(GenericAPIView):
    serializer_class = MissionSerializer

    def get(self, request, *args, **kwargs):
        missions = Mission.objects.all()
        serializer = self.serializer_class(missions, many=True)
        return Response(serializer.data)


class MissionDetail(GenericAPIView):
    serializer_class = MissionSerializer

    def get(self, request, mission_id, *args, **kwargs):
        mission = Mission.objects.filter(id=mission_id).first()
        if mission:
            serializer = self.serializer_class(mission)
            return Response(serializer.data)
        else:
            raise NotFound("No Mission found for given id.")
