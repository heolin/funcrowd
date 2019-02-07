from rest_framework import serializers
from modules.statistics.models import UserMissionStats


class UserMissionStatsSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserMissionStats
        fields = ("mission_id", 'user_id')
