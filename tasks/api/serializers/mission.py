from rest_framework import serializers

from tasks.models import Mission


class MissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mission
        fields = ('id', 'name', 'description', 'instruction', 'tasks_count',
                  'achievements_count', 'metadata', 'total_exp')


