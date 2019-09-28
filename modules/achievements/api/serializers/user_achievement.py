from rest_framework import serializers

from modules.achievements.models import UserAchievement


class UserAchievementSerializer(serializers.ModelSerializer):
    order = serializers.IntegerField(source='achievement.order', read_only=True)
    target = serializers.FloatField(source='achievement.target', read_only=True)
    metadata = serializers.JSONField(source='achievement.metadata', read_only=True)

    class Meta:
        model = UserAchievement
        fields = ('id', 'order', 'status', 'value', 'target', 'progress', 'metadata')
