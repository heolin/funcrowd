# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.permissions import AllowAny

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from modules.communication.email import EmailHelper
from users.api.serializers.reset_password import ResetPasswordSerializer
from users.api.views.errors import EmailNotFound
from users.models.end_workers import EndWorker


class EndWorkerResetPasswordView(GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = (AllowAny,)
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            end_worker = EndWorker.objects.filter(email=serializer.data['email']).first()
            if not end_worker:
                raise EmailNotFound()

            token = end_worker.create_password_token()
            EmailHelper.send_reset_password_email(end_worker, token)
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
