# -*- coding: utf-8 -*-

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from tasks.models import UserTaskProgress, Mission, Task

from tasks.api.serializers.task_progress import UserTaskProgressSerializer


class UserTaskProgressList(GenericAPIView):
    serializer_class = UserTaskProgressSerializer

    def get(self, request, mission_id, *args, **kwargs):
        mission = Mission.objects.filter(id=mission_id).first()
        if mission:
            for task in mission.tasks.all():
                request.user.get_task_progress(task)
            tasks_progress = UserTaskProgress.objects.filter(task__mission=mission, user=request.user)
            serializer = self.serializer_class(tasks_progress, many=True)
            return Response(serializer.data)
        raise NotFound("No Mission found for given id.")


class UserTaskProgressDetail(GenericAPIView):
    serializer_class = UserTaskProgressSerializer

    def get(self, request, task_id, *args, **kwargs):
        task = Task.objects.filter(id=task_id).first()
        if task:
            progress = request.user.get_task_progress(task)
            serializer = self.serializer_class(progress)
            return Response(serializer.data)
        raise NotFound("No Task with given id found in selected mission.")
