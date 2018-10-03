# -*- coding: utf-8 -*-

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from tasks.models import Mission

from tasks.api.serializers.item import ItemSerializer


class TaskNextItem(APIView):
    serializer_class = ItemSerializer

    def get(self, request, mission_id, task_id, *args, **kwargs):
        mission = Mission.objects.filter(id=mission_id).first()
        if mission:
            task = mission.tasks.filter(id=task_id).first()
            if task:
                item = task.get_next_item()
                serializer = self.serializer_class(item)
                return Response(serializer.data)
            raise NotFound("No Task found in selected mission, for given id.")
        raise NotFound("No Mission found for given id.")

