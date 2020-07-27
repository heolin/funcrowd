# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from modules.packages.api.serializers import (
    PackageSerializer
)
from modules.packages.models import Package
from tasks.api.serializers.item import ItemSerializer


class PackageView(GenericAPIView):
    serializer_class = PackageSerializer

    def get(self, request, package_id, *args, **kwargs):
        package = Package.objects.filter(id=package_id).first()
        if package:
            serializer = self.serializer_class(package)
            return Response(serializer.data)
        raise NotFound("No Package found for given id.")


class PackageNextItemView(GenericAPIView):
    serializer_class = ItemSerializer

    def get(self, request, package_id, *args, **kwargs):
        package = Package.objects.filter(id=package_id).first()
        if package:
            item = package.get_user_next_item(request.user)
            if item:
                item.get_or_create_annotation(request.user)
                serializer = self.serializer_class(item)
                return Response(serializer.data)
            return Response(None, status.HTTP_204_NO_CONTENT)
        raise NotFound("No Package found for given id.")


