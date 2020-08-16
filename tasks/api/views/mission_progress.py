# -*- coding: utf-8 -*-

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework import status

from tasks.models import UserMissionProgress, Mission

from tasks.api.serializers.mission_progress import UserMissionProgressSerializer, BonusExpSerializer
from users.models import EndWorker


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


class AddBonusExpView(GenericAPIView):
    serializer_class = BonusExpSerializer

    def post(self, request, mission_id):
        mission = Mission.objects.filter(id=mission_id).first()
        serializer = self.serializer_class(data=request.data)
        if mission:
            if serializer.is_valid():
                if 'user_id' in serializer.data:
                    user = EndWorker.objects.get(id=serializer.data['user_id'])
                else:
                    user = request.user
                ump = user.get_mission_progress(mission)
                bonus_exp = serializer.data['bonus_exp']
                ump.bonus_exp += bonus_exp
                ump.save()
                return Response(None, status.HTTP_204_NO_CONTENT)
            else:
                raise ValidationError("Mission field required field: 'bonus_exp'")
        raise NotFound("No Mission found for selected id.")
