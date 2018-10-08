# -*- coding: utf-8 -*-

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from tasks.models import Item

from tasks.api.serializers.annotation import  AnnotationSerializer


class AnnotationDetail(APIView):
    serializer_class = AnnotationSerializer

    def get(self, request, item_id, *args, **kwargs):
        item = Item.objects.get(id=item_id)
        if item:
            annotation, created = item.get_or_create_annotation(request.user)
            serializer = self.serializer_class(annotation)
            return Response(serializer.data)
        raise NotFound("No Item found for given id.")


