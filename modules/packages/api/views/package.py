# -*- coding: utf-8 -*-

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status

from modules.packages.api.views.utils import get_search_query
from modules.packages.models.search.packages_search import PackagesSearch
from tasks.models import Mission

from modules.packages.api.serializers.package import PackageSerializer


class NextPackageView(GenericAPIView):
    serializer_class = PackageSerializer

    def get(self, request, mission_id, *args, **kwargs):
        mission = Mission.objects.filter(id=mission_id).first()
        if mission:
            search = get_search_query(request)
            searcher = PackagesSearch(mission.packages, search)

            next_package = searcher.next_package(request.user, None)
            if next_package:
                serializer = self.serializer_class(next_package)
                return Response(serializer.data)
            return Response(None, status.HTTP_204_NO_CONTENT)
        raise NotFound("No Mission found for given id.")

