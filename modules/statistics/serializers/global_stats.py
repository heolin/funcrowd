from rest_framework import serializers
from modules.statistics.models import GlobalStats


class GlobalStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalStats
        fields = ('total_users', 'total_documents',
                  'total_finished_documents', 'total_tasks', 'total_missions')
