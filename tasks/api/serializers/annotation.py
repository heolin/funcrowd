from rest_framework import serializers

from tasks.models import Annotation


class AnnotationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Annotation
        fields = ('data',)
