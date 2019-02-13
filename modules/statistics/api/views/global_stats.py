# -*- coding: utf-8 -*-

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from modules.statistics.models import GlobalStats
from modules.statistics.serializers.global_stats import GlobalStatsSerializer


class GlobalStatsView(GenericAPIView):
    permission_classes = (AllowAny,)
    authentication_classes = []
    serializer_class = GlobalStatsSerializer

    def get(self, request,  *args, **kwargs):
        stats, _ = GlobalStats.objects.get_or_create()
        serializer = self.serializer_class(stats)
        return Response(serializer.data)
