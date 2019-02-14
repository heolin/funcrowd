# -*- coding: utf-8 -*-

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from modules.statistics.serializers.user_stats import UserStatsSerializer
from users.models import EndWorker


class UserStatsView(GenericAPIView):
    serializer_class = UserStatsSerializer
    authentication_classes = []
    permission_classes = (AllowAny,)

    def get(self, request, user_id,  *args, **kwargs):
        user = EndWorker.objects.filter(id=user_id).first()
        if user:
            serializer = self.serializer_class(user.stats)
            return Response(serializer.data)
        return NotFound("No User find for given id.")

