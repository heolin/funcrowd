# -*- coding: utf-8 -*-

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status

from tasks.models import Item, Task

from tasks.api.serializers.item import ItemSerializer


class TaskNextItem(GenericAPIView):
    serializer_class = ItemSerializer

    def get(self, request, task_id, *args, **kwargs):
        task = Task.objects.filter(id=task_id).first()
        if task:
            next_item = task.next_item(request.user, None)
            if next_item:
                serializer = self.serializer_class(next_item)
                return Response(serializer.data)
            return Response(None, status.HTTP_204_NO_CONTENT)
        raise NotFound("No Task found for given id.")


class TaskNextItemWithPrevious(GenericAPIView):
    serializer_class = ItemSerializer

    def get(self, request, item_id, *args, **kwargs):
        item = Item.objects.filter(id=item_id).first()
        if item:
            next_item = item.task.next_item(request.user, item)
            if next_item:
                serializer = self.serializer_class(next_item)
                return Response(serializer.data)
            return Response(None, status.HTTP_204_NO_CONTENT)
        raise NotFound("No Item found for given id.")

