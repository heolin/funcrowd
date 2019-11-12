# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from users.api.serializers.password_token import ResetPasswordTokenSerializer
from users.api.views.errors import (
    PasswordTokenWrong, PasswordTokenUsed, PasswordTokenExpired,
    PasswordNotMatch)
from users.models import PasswordToken


class ResetPasswordTokenView(GenericAPIView):
    serializer_class = ResetPasswordTokenSerializer
    permission_classes = (AllowAny,)
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token = PasswordToken.objects.filter(token=serializer.data['token']).first()
            password1 = serializer.data['password1']
            password2 = serializer.data['password2']

            if not token:
                raise PasswordTokenWrong()
            if token.token_used:
                raise PasswordTokenUsed()
            if token.is_expired:
                raise PasswordTokenExpired()
            if password1 != password2:
                raise PasswordNotMatch()

            token.activate()
            end_worker = token.user
            end_worker.set_password(password1)
            end_worker.save()

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

