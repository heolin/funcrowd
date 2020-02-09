from rest_framework import serializers

from modules.feedback.models import Feedback
from modules.feedback.models.annotation_feedback import AnnotationFeedback


class AnnotationFeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnnotationFeedback
        fields = ('values', 'scores', 'score')


class FeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feedback
        fields = ('type', 'autoreject')
