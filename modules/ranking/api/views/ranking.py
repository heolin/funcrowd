# -*- coding: utf-8 -*-
from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from modules.packages.models import MissionPackages
from modules.ranking.api.serializers.ranking import RankingSerializer, MPRankingSerializer
from modules.ranking.models import AnnotationsRanking, ExpRanking
from modules.ranking.models.mission_packages_ranking import MissionPackagesRanking


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


# Annotations Ranking
class AnnotationsRankingTop(RankingTop):
    RankingType = AnnotationsRanking


class AnnotationsRankingAround(RankingAround):
    RankingType = AnnotationsRanking


# Exp Ranking
class ExpRankingTop(RankingTop):
    RankingType = ExpRanking


class ExpRankingAround(RankingAround):
    RankingType = ExpRanking


# Mission Package ranking
class MissionPackagesRankingTop(RankingTop):
    RankingType = MissionPackagesRanking
    serializer_class = MPRankingSerializer

    def get(self, request, mission_id, *args, **kwargs):
        mp = MissionPackages.objects.get(mission_id=mission_id)
        if mp:
            ranking = self.RankingType(mp)

            size = int(request.GET.get('size', 10))
            page = int(request.GET.get('page', 0))

            results = ranking.top(size, page)
            serializer = self.serializer_class(results, many=True)
            return Response(serializer.data)
        else:
            return NotFound("Mission with this id not found")


class MissionPackagesRankingAround(RankingAround):
    RankingType = MissionPackagesRanking
    serializer_class = MPRankingSerializer

    def get(self, request, mission_id, user_id, *args, **kwargs):
        mp = MissionPackages.objects.get(mission_id=mission_id)
        if mp:
            ranking = self.RankingType(mp)

            size = int(request.GET.get('size', 2))

            results = ranking.around(user_id, size)
            serializer = self.serializer_class(results, many=True)
            return Response(serializer.data)
        else:
            return NotFound("Mission with this id not found")
