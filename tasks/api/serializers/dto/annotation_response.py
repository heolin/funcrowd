from rest_framework import serializers
from tasks.api.serializers.annotation import AnnotationSerializer
from modules.validators.api.serializers.errors import AnnotationFormErrorSerializers


class AnnotationResponseSerializer(serializers.Serializer):
    annotation = AnnotationSerializer()
    is_verified = serializers.BooleanField()
    errors = AnnotationFormErrorSerializers(many=True)

    class Meta:
        fields = ('annotation', 'is_verified', 'errors')
