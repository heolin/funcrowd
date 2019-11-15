from rest_framework import serializers


class ChangeSettingsSerializer(serializers.Serializer):
    username = serializers.CharField()
