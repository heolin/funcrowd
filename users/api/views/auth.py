# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import funcrowd.settings as settings

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound, AuthenticationFailed, NotAuthenticated
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from django.contrib.auth import authenticate, login, logout

from modules.communication.email import EmailHelper
from users.api.views.errors import UsernameUsed, EmailUsed, PasswordNotMatch, AccountUnactive, EmailNotFound, \
    UsernameNotFound
from users.models.end_workers import EndWorker
from users.api.serializers import (
    EndWorkerRegistrationSerializer,
    EndWorkerLoginSerializer,
    EndWorkerSerializer,
    EndWorkerEmailInfoSerializer,
    EndWorkerUsernameInfoSerializer,
    EndWorkerSimpleSerializer,
    EndWorkerStatusSerializer)


class EndWorkerRegistrationView(GenericAPIView):
    serializer_class = EndWorkerRegistrationSerializer
    permission_classes = (AllowAny,)
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = EndWorkerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            username = data['username']
            password1 = data['password1']
            password2 = data['password2']
            email = data.get('email')

            if EndWorker.objects.filter(username=username).first():
                raise UsernameUsed()
            if EndWorker.objects.filter(email=email).first():
                raise EmailUsed()
            if password1 != password2:
                raise PasswordNotMatch()

            end_worker = EndWorker.objects.create_user(username, email, password1)

            if settings.ACCOUNT_EMAIL_VERIFICATION:
                token = end_worker.create_activation_token()
                EmailHelper.send_activation_email(end_worker, token)
                end_worker.is_active = False
                end_worker.save()
                return Response(status=status.HTTP_204_NO_CONTENT)

            end_worker.is_active = True
            end_worker.save()

            serializer = EndWorkerSerializer(end_worker)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EndWorkerLoginView(GenericAPIView):
    serializer_class = EndWorkerLoginSerializer
    permission_classes = (AllowAny,)
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = EndWorkerLoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            username = data['username']
            password = data['password']

            end_worker = EndWorker.objects.filter(username=username).first()
            if end_worker is None:
                raise NotAuthenticated()
            if not end_worker.is_active:
                raise AccountUnactive()

            end_worker = authenticate(username=username, password=password)
            if end_worker is None:
                raise NotAuthenticated()

            login(request, end_worker)
            end_worker.on_login()
            serializer = EndWorkerSerializer(end_worker)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EndWorkerView(GenericAPIView):
    serializer_class = EndWorkerSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)


class EndWorkerLogoutView(GenericAPIView):

    def get(self, request, *args, **kwargs):
        if not request.user.is_anonymous:
            logout(request)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)  # need to figure out correct error here


class EndWorkerEmailInfoView(GenericAPIView):
    serializer_class = EndWorkerEmailInfoSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            end_worker = EndWorker.objects.filter(email=email).first()
            if not end_worker:
                raise EmailNotFound()
            serializer = EndWorkerSimpleSerializer(end_worker)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EndWorkerUsernameInfoView(GenericAPIView):
    serializer_class = EndWorkerUsernameInfoSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.data['username']
            end_worker = EndWorker.objects.filter(username=username).first()
            if not end_worker:
                raise UsernameNotFound()

            serializer = EndWorkerSimpleSerializer(end_worker)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EndWorkerStatusView(GenericAPIView):
    serializer_class = EndWorkerStatusSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)


class EndWorkerResetPasswordView(GenericAPIView):

    def post(self, request, *args, **kwargs):
        end_worker = request.user
        token = end_worker.create_password_token()
        EmailHelper.send_reset_password_email(end_worker, token)
        return Response(status=status.HTTP_204_NO_CONTENT)
