# -*- coding: utf-8 -*-

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from tasks.models import Item, Task

from tasks.api.serializers.item import ItemSerializer


class TaskNextItem(APIView):
    serializer_class = ItemSerializer

    def get(self, request, task_id, *args, **kwargs):
        task = Task.objects.filter(id=task_id).first()
        if task:
            next_item = task.next_item(request.user, None)
            serializer = self.serializer_class(next_item)
            return Response(serializer.data)
        raise NotFound("No Task found for given id.")


class TaskNextItemWithPrevious(APIView):
    serializer_class = ItemSerializer

    def get(self, request, item_id, *args, **kwargs):
        item = Item.objects.items.filter(id=item_id).first()
        if item:
            next_item = item.task.next_item(request.user, item)
            serializer = self.serializer_class(next_item)
            return Response(serializer.data)
        raise NotFound("No Item found for given id.")

