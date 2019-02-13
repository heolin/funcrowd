# -*- coding: utf-8 -*-

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from modules.statistics.serializers.mission_stats import MissionStatsSerializer
from tasks.models import Mission


class MissionStatsView(GenericAPIView):
    permission_classes = (AllowAny,)
    authentication_classes = []
    serializer_class = MissionStatsSerializer

    def get(self, request, mission_id,  *args, **kwargs):
        mission = Mission.objects.filter(id=mission_id).first()
        if mission:
            serializer = self.serializer_class(mission.stats)
            return Response(serializer.data)
        return NotFound("No Mission find for given id.")
