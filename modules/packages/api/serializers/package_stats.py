
from rest_framework import serializers


class PackageAggregatedStatsSerializer(serializers.Serializer):
    field = serializers.CharField()
    value = serializers.CharField()
    package_status = serializers.DictField()
    user_status = serializers.DictField()
    total = serializers.IntegerField()
