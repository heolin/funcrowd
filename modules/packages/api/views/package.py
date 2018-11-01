# -*- coding: utf-8 -*-

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status

from tasks.models import Mission

from modules.packages.api.serializers.package import PackageSerializer


class NextPackage(GenericAPIView):
    serializer_class = PackageSerializer

    def get(self, request, mission_id, *args, **kwargs):
        mission = Mission.objects.filter(id=mission_id).first()
        if mission:
            next_package = mission.packages.next_package(request.user, None)
            if next_package:
                serializer = self.serializer_class(next_package)
                return Response(serializer.data)
            return Response(None, status.HTTP_204_NO_CONTENT)
        raise NotFound("No Task found for given id.")

