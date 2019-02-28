from rest_framework import serializers
from modules.statistics.models import UserMissionStats


class UserMissionStatsSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserMissionStats
        fields = ("mission_id", 'user_id', 'annotated_documents', 'high_agreement_count',
                  'high_agreement_percentage', 'agreement_ranking_position', 'agreement_ranking_percentage',)
