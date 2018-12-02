from rest_framework import serializers


class AnnotationFormErrorSerializers(serializers.Serializer):
    name = serializers.CharField()
    field = serializers.CharField()
    message = serializers.CharField()

    class Meta:
        fields = ('name', 'field', 'message')
