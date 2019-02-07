from rest_framework import serializers
from modules.statistics.models import UserStats


class UserStatsSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserStats
        fields = ('user_id',)
