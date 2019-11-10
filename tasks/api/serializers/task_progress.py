from rest_framework import serializers

from tasks.models import UserTaskProgress


class UserTaskProgressSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserTaskProgress
        fields = ('id', 'task', 'items_done', 'items_count', 'progress', 'status')
