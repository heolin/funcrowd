# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.contrib.auth import login

from users.models.utils.mturk import verify_worker_id

from users.models.end_workers import EndWorker
from users.api.serializers import (
    MturkRegistrationSerializer,
    EndWorkerSerializer
)


class MturkRegisterLoginView(GenericAPIView):
    serializer_class = MturkRegistrationSerializer
    permission_classes = (AllowAny,)
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            worker_id = data['worker_id']

            if verify_worker_id(worker_id) is False:
                raise ValidationError("WorkerID is not valid")

            end_worker = EndWorker.objects.filter(username=worker_id).first()
            if not end_worker:
                password = EndWorker.objects.make_random_password()
                end_worker = EndWorker.objects.create_user(worker_id, "{}@mturk".format(worker_id), password)
            login(request, end_worker)
            serializer = EndWorkerSerializer(end_worker)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
