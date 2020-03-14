# -*- coding: utf-8 -*-

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from modules.packages.api.exceptions import MissingAggregationGetParam
from modules.packages.api.serializers.package_stats import PackageAggregatedStatsSerializer
from modules.packages.api.views.utils import get_search_query
from modules.packages.models import MissionPackages

from modules.packages.models.search.package_stats import PackageSearchStatsAggregator


class PackageSearchAggregatedStatsView(GenericAPIView):
    serializer_class = PackageAggregatedStatsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, mission_id, *args, **kwargs):
        mp = MissionPackages.objects.filter(mission=mission_id).first()
        if mp:
            search = get_search_query(request)

            if "aggregation" not in request.GET:
                raise MissingAggregationGetParam()

            aggregation = request.GET['aggregation']

            aggregator = PackageSearchStatsAggregator(mp, search)

            data = aggregator.get_aggregation(request.user, aggregation)
            serializer = self.serializer_class(data, many=True)
            return Response(serializer.data)
        raise NotFound("No Mission found for given id.")
