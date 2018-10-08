from rest_framework import serializers

from tasks.models import Annotation


class AnnotationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Annotation
        fields = ('item_id', 'data', 'is_done', 'is_skipped', )
