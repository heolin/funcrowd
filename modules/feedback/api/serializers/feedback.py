from rest_framework import serializers

from modules.feedback.models.annotation_feedback import AnnotationFeedback


class AnnotationFeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnnotationFeedback
        fields = ('values', 'scores', 'score', 'type')
