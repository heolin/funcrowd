from rest_framework import serializers

from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('id', 'mission', 'name', 'description', 'instruction',
                  'keywords', 'metadata', 'total_exp', 'achievements_count')

