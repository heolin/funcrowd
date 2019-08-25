# -*- coding: utf-8 -*-

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from tasks.models import UserMissionProgress, Mission

from tasks.api.serializers.mission_progress import UserMissionProgressSerializer


class UserMissionProgressList(GenericAPIView):
    serializer_class = UserMissionProgressSerializer

    def get(self, request, *args, **kwargs):
        for mission in Mission.objects.all():
            request.user.get_mission_progress(mission)
        mission_progress = UserMissionProgress.objects.filter(user=request.user)
        serializer = self.serializer_class(mission_progress, many=True)
        return Response(serializer.data)


class UserMissionProgressDetail(GenericAPIView):
    serializer_class = UserMissionProgressSerializer

    def get(self, request, mission_id, *args, **kwargs):
        mission = Mission.objects.filter(id=mission_id).first()
        if mission:
            progress = request.user.get_mission_progress(mission)
            serializer = self.serializer_class(progress)
            return Response(serializer.data)
        raise NotFound("No Mission found for selected id.")
