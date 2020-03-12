# -*- coding: utf-8 -*-

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from modules.packages.api.exceptions import (
    MissingSearchGetParam, SearchGetParamMalformed,
    MissingAggregationGetParam)
from modules.packages.api.serializers.package_stats import PackageAggregatedStatsSerializer
from modules.packages.models import MissionPackages

from modules.packages.models.search.package_stats import PackageSearchStatsAggregator


def parse_search_params(search):
    params = search.split(':')
    if len(params) != 2:
        raise ValueError
    return {params[0]: params[1]}


class PackageSearchAggregatedStatsView(GenericAPIView):
    serializer_class = PackageAggregatedStatsSerializer

    def get(self, request, mission_id, *args, **kwargs):
        mp = MissionPackages.objects.filter(mission=mission_id).first()
        if mp:
            if "search" not in request.GET:
                raise MissingSearchGetParam()

            try:
                search = parse_search_params(request.GET["search"])
            except ValueError:
                raise SearchGetParamMalformed()

            if "aggregation" not in request.GET:
                raise MissingAggregationGetParam()

            aggregation = request.GET['aggregation']

            aggregator = PackageSearchStatsAggregator(mp, search)
            data = aggregator.get_aggregation(request.user, aggregation)
            serializer = self.serializer_class(data, many=True)
            return Response(serializer.data)
        raise NotFound("No Mission found for given id.")
