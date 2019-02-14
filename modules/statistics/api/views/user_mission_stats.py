# -*- coding: utf-8 -*-

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from modules.statistics.serializers.user_mission_stats import UserMissionStatsSerializer
from tasks.models import Mission
from users.models import EndWorker


class UserMissionStatsView(GenericAPIView):
    serializer_class = UserMissionStatsSerializer
    authentication_classes = []
    permission_classes = (AllowAny,)

    def get(self, request, user_id, mission_id,  *args, **kwargs):
        user = EndWorker.objects.filter(id=user_id).first()
        if user:
            mission = Mission.objects.filter(id=mission_id).first()
            if mission:
                stats = user.get_mission_stats(mission.id)
                serializer = self.serializer_class(stats)
                return Response(serializer.data)
            return NotFound("No Mission find for given id.")
        return NotFound("No User find for given id.")
