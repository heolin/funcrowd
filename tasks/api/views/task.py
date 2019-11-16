# -*- coding: utf-8 -*-

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from tasks.models import Mission, Task

from tasks.api.serializers.task import TaskSerializer


class MissionTasksList(GenericAPIView):
    serializer_class = TaskSerializer

    def get(self, request, mission_id, *args, **kwargs):
        mission = Mission.objects.filter(id=mission_id).first()
        if mission:
            serializer = self.serializer_class(mission.tasks.all(), many=True)
            return Response(serializer.data)
        raise NotFound("No Mission found for given id.")


class TaskDetail(GenericAPIView):
    serializer_class = TaskSerializer

    def get(self, request, task_id, *args, **kwargs):
        print("LOOL")
        print(Task.objects.all())
        print(task_id)
        task = Task.objects.filter(id=task_id).first()
        if task:
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        raise NotFound("No Task with given id found in selected mission.")

