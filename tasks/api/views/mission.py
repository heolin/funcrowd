# -*- coding: utf-8 -*-

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from tasks.models import Mission

from tasks.api.serializers.mission import MissionSerializer


class MissionList(APIView):
    serializer_class = MissionSerializer

    def get(self, request, *args, **kwargs):
        missions = Mission.objects.all()
        serializer = self.serializer_class(missions, many=True)
        return Response(serializer.data)


class MissionDetail(APIView):
    serializer_class = MissionSerializer

    def get(self, request, mission_id, *args, **kwargs):
        mission = Mission.objects.filter(id=mission_id).first()
        if mission:
            serializer = self.serializer_class(mission)
            return Response(serializer.data)
        else:
            raise NotFound("No Mission found for given id.")


"""
from tasks.models import Task, Item, Annotation

import json
class TaskDetail(APIView):
    serializer_class = TaskSerializer

    def get(self, request, task_id, *args, **kwargs):
        task = Task.objects.get(id=task_id)
        serializer = TaskSerializer(task)
        return Response(serializer.data)


class TaskNextItem(APIView):
    serializer_class = ItemSerializer

    def get(self, request, task_id, *args, **kwargs):
        task = Task.objects.get(id=task_id)
        item = task.get_next_item()
        serializer = ItemSerializer(item)
        return Response(serializer.data)


class TaskItemDetail(APIView):
    serializer_class = ItemSerializer

    def get(self, request, task_id, item_id, *args, **kwargs):
        item = Item.objects.get(id=item_id, task_id=task_id)
        serializer = ItemSerializer(item)
        return Response(serializer.data)


class TaskItemAnnotation(APIView):
    serializer_class = AnnotationSerializer

    def get(self, request, task_id, item_id, *args, **kwargs):
        item = Item.objects.get(id=item_id, task_id=task_id)
        annotation = item.annotations.filter(user=request.user).first()
        if not annotation:
            annotation = Annotation.objects.create(item=item,
                                                   user=request.user, data={})
        serializer = AnnotationSerializer(annotation)
        return Response(serializer.data)

    def put(self, request, task_id, item_id, *args, **kwargs):
        item = Item.objects.get(id=item_id, task_id=task_id)

        data_json = dict(request.data)

        if isinstance(data_json['data'], list):
            data_json['data'] = json.loads(data_json['data'][0])

        serializer = AnnotationSerializer(data_json)

        if item.task.template.multiple_annotations:
            annotation = Annotation.objects.create(item=item,
                                                   user=request.user, data={})
        else:
            annotation = Annotation.objects.filter(item=item,
                                                   user=request.user).first()
            if not annotation:
                annotation = Annotation.objects.create(item=item,
                                                       user=request.user,
                                                       data={})

        annotation.data = serializer.data['data']

        fields_check = annotation.check_fields()

        done_check = False

        if fields_check:
            done_check = annotation.validate(False)
        annotation.save()

        result = done_check and fields_check

        request.user.stats.add_exp(annotation.exp)

        return Response({'fields': fields_check, 'done': done_check,
                         'skipped': annotation.skipped, 'result': result,
                         'score': annotation.score, 'exp': annotation.exp})
"""
