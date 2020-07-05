# -*- coding: utf-8 -*-
from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from modules.packages.models import MissionPackages
from modules.ranking.api.serializers.ranking import(
    RankingSerializer, MPRankingRowSerializer, MissionRankingSerializer
)
from modules.ranking.models import AnnotationsRanking, ExpRanking
from modules.ranking.models.mission_packages_ranking import MissionPackagesRanking
from django.core.paginator import Paginator


class RankingTop(GenericAPIView):
    rankingType = None
    serializer_class = RankingSerializer
    permission_classes = (AllowAny,)
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        ranking = self.rankingType()

        size = int(request.GET.get('size', 10))
        page = int(request.GET.get('page', 0))

        results = ranking.top(size, page)
        serializer = self.serializer_class(results, many=True)
        return Response(serializer.data)


class RankingAround(GenericAPIView):
    rankingType = None
    serializer_class = RankingSerializer

    def get(self, request, user_id, *args, **kwargs):
        ranking = self.rankingType()

        size = int(request.GET.get('size', 2))

        results = ranking.around(user_id, size)

        serializer = self.serializer_class(results, many=True)
        return Response(serializer.data)


# Annotations Ranking
class AnnotationsRankingTop(RankingTop):
    rankingType = AnnotationsRanking


class AnnotationsRankingAround(RankingAround):
    rankingType = AnnotationsRanking


# Exp Ranking
class ExpRankingTop(RankingTop):
    rankingType = ExpRanking


class ExpRankingAround(RankingAround):
    rankingType = ExpRanking


# Mission Package ranking
class MissionPackagesRankingTop(RankingTop):
    rankingType = MissionPackagesRanking
    serializer_class = MissionRankingSerializer
    permission_classes = (AllowAny,)
    authentication_classes = []

    def get(self, request, mission_id, *args, **kwargs):
        mp = MissionPackages.objects.get(mission_id=mission_id)
        if mp:
            ranking = self.rankingType(mp)

            size = int(request.GET.get('size', 10))
            page = int(request.GET.get('page', 0))

            results = ranking.top(size, page)
            rows = MPRankingRowSerializer(results, many=True).data

            result = {
                "mission_id": mission_id,
                "rows": rows
            }
            serializer = self.serializer_class(result)
            return Response(serializer.data)
        else:
            return NotFound("Mission with this id not found")


class MissionPackagesRankingAround(RankingAround):
    rankingType = MissionPackagesRanking
    serializer_class = MissionRankingSerializer
    permission_classes = (AllowAny,)
    authentication_classes = []

    def get(self, request, mission_id, user_id, *args, **kwargs):
        mp = MissionPackages.objects.get(mission_id=mission_id)
        if mp:
            ranking = self.rankingType(mp)

            size = int(request.GET.get('size', 2))

            rows_ranking = ranking.around(user_id, size)
            rows = MPRankingRowSerializer(rows_ranking, many=True).data

            result = {
                "mission_id": mission_id,
                "rows": rows
            }
            serializer = self.serializer_class(result)
            return Response(serializer.data)
        else:
            return NotFound("Mission with this id not found")


class MissionRankingList(RankingAround):
    rankingType = MissionPackagesRanking
    serializer_class = MissionRankingSerializer
    permission_classes = (AllowAny,)
    authentication_classes = []

    def get(self, request, user_id, *args, **kwargs):
        results = []

        list_size = int(request.GET.get('list_size', 0))
        list_page = int(request.GET.get('list_page', 1))
        size = int(request.GET.get('size', 0))

        mission_packages = MissionPackages.objects.all().order_by("mission_id")
        if list_size > 0:
            paginator = Paginator(mission_packages, list_size)
            mission_packages = paginator.get_page(list_page)
        else:
            mission_packages = mission_packages

        for mp in mission_packages:
            ranking = self.rankingType(mp)
            print(mp)

            rows_ranking = ranking.around(user_id, size)
            rows = MPRankingRowSerializer(rows_ranking, many=True).data

            results.append({
                "mission_id": mp.mission_id,
                "rows": rows
            })

        serializer = self.serializer_class(results, many=True)
        return Response(serializer.data)
