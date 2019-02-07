# -*- coding: utf-8 -*-

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from modules.statistics.serializers.user_stats import UserStatsSerializer
from users.models import EndWorker


class UserStatsView(GenericAPIView):
    serializer_class = UserStatsSerializer

    def get(self, request, user_id,  *args, **kwargs):
        user = EndWorker.objects.filter(id=user_id).first()
        if user:
            serializer = self.serializer_class(user.stats)
            return Response(serializer.data)
        return NotFound("No User find for given id.")

