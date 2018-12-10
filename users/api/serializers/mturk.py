from rest_framework import serializers


class MturkRegistrationSerializer(serializers.Serializer):
    worker_id = serializers.CharField()

