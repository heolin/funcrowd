from rest_framework import serializers

from tasks.models import UserMissionProgress


class UserMissionProgressSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserMissionProgress
        fields = ('id', 'mission', 'tasks_done', 'tasks_count', 'progress', 'status')


class BonusExpSerializer(serializers.Serializer):
    bonus_exp = serializers.IntegerField()
