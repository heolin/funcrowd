from rest_framework import serializers
from tasks.api.serializers.annotation import AnnotationSerializer
from modules.validators.api.serializers.errors import AnnotationFormErrorSerializers


class AnnotationResponseSerializer(serializers.Serializer):
    annotation = AnnotationSerializer()
    next_item_id = serializers.IntegerField()
    is_verified = serializers.BooleanField()
    exp_base = serializers.IntegerField()
    exp_bonus = serializers.IntegerField()
    errors = AnnotationFormErrorSerializers(many=True)

    class Meta:
        fields = ('annotation', 'is_verified', 'exp_base', 'exp_bonus',
                  'errors', 'next_item_id')
