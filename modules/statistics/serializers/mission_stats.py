from rest_framework import serializers
from modules.statistics.models import MissionStats


class MissionStatsSerializer(serializers.ModelSerializer):

    class Meta:
        model = MissionStats
        fields = ("mission_id", 'total_documents', 'total_finished_documents',
                  'total_users', 'total_tasks')
