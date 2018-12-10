from rest_framework import serializers

from tasks.api.serializers.task import TaskSerializer
from modules.bounty.models import Bounty


class BountySerializer(serializers.ModelSerializer):
    task = TaskSerializer()

    class Meta:
        model = Bounty
        fields = ('id', 'task', 'annotations_target')
