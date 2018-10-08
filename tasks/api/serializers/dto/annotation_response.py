from rest_framework import serializers
from tasks.api.serializers.annotation import AnnotationSerializer


class AnnotationResponseSerializer(serializers.Serializer):
    annotation = AnnotationSerializer()
    is_verified = serializers.BooleanField()

    class Meta:
        fields = ('annotation', 'is_verified')
