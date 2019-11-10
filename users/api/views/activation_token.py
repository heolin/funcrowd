# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from users.api.serializers import EndWorkerSerializer
from users.api.serializers.activation_token import ActivationTokenSerializer
from users.api.views.errors import ActivationTokenWrong, ActivationTokenUsed
from users.models.activation_token import ActivationToken
from django.contrib.auth import login


class ActivateTokenView(GenericAPIView):
    serializer_class = ActivationTokenSerializer
    permission_classes = (AllowAny,)
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token = ActivationToken.objects.filter(token=serializer.data['token']).first()
            if token:
                if not token.token_used:
                    token.activate()
                    end_worker = token.user
                    login(request, end_worker)
                    end_worker.on_login()
                    serializer = EndWorkerSerializer(end_worker)
                    return Response(serializer.data)
                raise ActivationTokenUsed()
            raise ActivationTokenWrong()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


