# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate
from rest_framework.exceptions import NotAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from users.api.serializers import ChangePasswordSerializer
from users.api.views.errors import (
    PasswordNotMatch)


class ChangePasswordView(GenericAPIView):
    serializer_class = ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            old_password = serializer.data['old_password']
            password1 = serializer.data['new_password1']
            password2 = serializer.data['new_password2']

            end_worker = authenticate(email=request.user.email, password=old_password)
            if end_worker is None:
                raise NotAuthenticated()
            if password1 != password2:
                raise PasswordNotMatch()

            end_worker.set_password(password1)
            end_worker.save()

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

