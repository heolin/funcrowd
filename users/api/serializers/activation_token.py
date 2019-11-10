from rest_framework import serializers


class ActivationTokenSerializer(serializers.Serializer):
    token = serializers.CharField()

