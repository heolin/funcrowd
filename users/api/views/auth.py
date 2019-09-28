# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from django.contrib.auth import authenticate, login, logout

from funcrowd.settings import events_manager
from modules.achievements.events import Events
from users.models.end_workers import EndWorker
from users.api.serializers import (
    EndWorkerRegistrationSerializer,
    EndWorkerLoginSerializer,
    EndWorkerSerializer,
    EndWorkerEmailInfoSerializer,
    EndWorkerUsernameInfoSerializer,
    EndWorkerSimpleSerializer
)


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
                raise ValidationError("EndWorker will given username already exists")
            if password1 != password2:
                raise ValidationError("Passwords don't match")

            end_worker = EndWorker.objects.create_user(username, email, password1)
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

            end_worker = authenticate(username=username, password=password)
            if end_worker is not None:
                login(request, end_worker)
                end_worker.on_login()
                serializer = EndWorkerSerializer(end_worker)
                return Response(serializer.data)
            raise ValidationError("Username or password is not correct")
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
            if end_worker:
                serializer = EndWorkerSimpleSerializer(end_worker)
                return Response(serializer.data)
            raise NotFound("No EndWorker found for given email.")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EndWorkerUsernameInfoView(GenericAPIView):
    serializer_class = EndWorkerUsernameInfoSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.data['username']
            end_worker = EndWorker.objects.filter(username=username).first()
            if end_worker:
                serializer = EndWorkerSimpleSerializer(end_worker)
                return Response(serializer.data)
            raise NotFound("No EndWorker found for given username.")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
