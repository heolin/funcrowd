# -*- coding: utf-8 -*-

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from modules.ranking.api.serializers.ranking import RankingSerializer
from modules.ranking.models import AnnotationsRanking, ExpRanking


class RankingTop(GenericAPIView):
    RankingType = None
    serializer_class = RankingSerializer

    def get(self, request, *args, **kwargs):
        ranking = self.RankingType()

        size = int(request.GET.get('size', 10))
        page = int(request.GET.get('page', 0))

        results = ranking.top(size, page)
        serializer = self.serializer_class(results, many=True)
        return Response(serializer.data)


class RankingAround(GenericAPIView):
    RankingType = None
    serializer_class = RankingSerializer

    def get(self, request, user_id, *args, **kwargs):
        ranking = self.RankingType()

        size = int(request.GET.get('size', 2))

        results = ranking.around(user_id, size)
        serializer = self.serializer_class(results, many=True)
        return Response(serializer.data)


class AnnotationsRankingTop(RankingTop):
    RankingType = AnnotationsRanking


class AnnotationsRankingAround(RankingAround):
    RankingType = AnnotationsRanking


class ExpRankingTop(RankingTop):
    RankingType = ExpRanking


class ExpRankingAround(RankingAround):
    RankingType = ExpRanking
