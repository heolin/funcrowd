# -*- coding: utf-8 -*-

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError

from tasks.models import Item

from tasks.api.serializers.annotation import AnnotationDataSerializer
from tasks.api.serializers.dto.annotation_response import AnnotationResponseSerializer
from tasks.controllers.annotation_controller import AnnotationController


class AnnotationDetail(GenericAPIView):
    serializer_class = AnnotationDataSerializer

    def get(self, request, item_id):
        item = Item.objects.filter(id=item_id).first()
        if item:
            # it won't work for multiple annotations
            annotation, created = item.get_or_create_annotation(request.user)
            annotation.reset_created()
            serializer = self.serializer_class(annotation)
            return Response(serializer.data)
        raise NotFound("No Item found for given id.")

    def post(self, request, item_id):
        item = Item.objects.filter(id=item_id).first()
        if item:
            annotation, created = item.get_or_create_annotation(request.user)
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                annotation.data = serializer.data['data']
                if not annotation.data:
                    annotation.data = item.get_default_annotation_data()
                annotation.skipped = serializer.data.get('skipped', False)
                response = AnnotationController().process(annotation)
                serializer = AnnotationResponseSerializer(response)
            else:
                raise ValidationError("Annotation data cannot be empty.")
            return Response(serializer.data)
        raise NotFound("No Item found for given id.")
