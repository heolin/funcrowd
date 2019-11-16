# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from users.api.serializers import ChangeSettingsSerializer, EndWorkerSerializer
from users.api.views.errors import UsernameUsed
from users.models import EndWorker


class ChangeSettingsView(GenericAPIView):
    serializer_class = ChangeSettingsSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            new_username = serializer.data['username']

            existing_user = EndWorker.objects.filter(username=new_username).first()
            if existing_user and existing_user != request.user:
                raise UsernameUsed()

            end_worker = request.user
            end_worker.username = new_username
            end_worker.save()

            serializer = EndWorkerSerializer(end_worker)
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

