from rest_framework import serializers

from tasks.models import Annotation
from modules.feedback.api.serializers.feedback import AnnotationFeedbackSerializer


class AnnotationSerializer(serializers.ModelSerializer):
    feedback = AnnotationFeedbackSerializer()

    class Meta:
        model = Annotation
        fields = ('item_id', 'data', 'skipped', 'feedback')


class AnnotationDataSerializer(serializers.ModelSerializer):
    data = serializers.JSONField()

    class Meta:
        model = Annotation
        fields = ('data', "skipped")
