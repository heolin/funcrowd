from rest_framework import serializers

from users.models.end_workers import EndWorker


class EndWorkerSerializer(serializers.ModelSerializer):
    token = serializers.CharField()

    class Meta:
        model = EndWorker
        fields = ('id', 'username', 'token', 'email', 'group', 'profile')


class EndWorkerSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = EndWorker
        fields = ('id', 'username', 'email', 'group', 'profile')
