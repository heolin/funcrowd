# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from modules.packages.api.exceptions import PackageNotCreatedInsufficientItems
from modules.packages.api.serializers import (
    PackageSerializer, PackageItemsSerializer,
    CreatePackageSerializer)
from modules.packages.api.views.utils import get_search_query
from modules.packages.exceptions import InsufficientUnassignedItems
from modules.packages.models import MissionPackages
from modules.packages.models.search.packages_search import PackagesSearch


class NextPackageView(GenericAPIView):
    serializer_class = PackageItemsSerializer

    def get(self, request, mission_id, *args, **kwargs):
        mp = MissionPackages.objects.filter(mission_id=mission_id).first()
        if mp:
            search = get_search_query(request)
            searcher = PackagesSearch(mp, search)

            next_package = searcher.next_package(request.user, None)
            if next_package:
                serializer = self.serializer_class(next_package)
                return Response(serializer.data)
            return Response(None, status.HTTP_204_NO_CONTENT)
        raise NotFound("No Mission found for given id.")


class CreatePackageView(GenericAPIView):
    serializer_class = CreatePackageSerializer

    def post(self, request, mission_id, *args, **kwargs):
        mp = MissionPackages.objects.filter(mission_id=mission_id).first()
        if mp:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                try:
                    package = mp.create_package(
                        serializer.data['size'],
                        serializer.data['metadata']
                    )
                except InsufficientUnassignedItems:
                    raise PackageNotCreatedInsufficientItems()
                package_serializer = PackageSerializer(package)
                return Response(package_serializer.data)
            raise ValidationError("Field 'size' not provided")

        raise NotFound("No MissionPackages found for given id.")
