from rest_framework import serializers


class AgreementMetricResultSerializer(serializers.Serializer):
    name = serializers.CharField()
    value = serializers.FloatField()

    class Meta:
        fields = ('name', 'name')
