from rest_framework import serializers

from tasks.api.serializers.task import TaskSerializer
from modules.bounty.models import Bounty

from modules.bounty.api.serializers import UserBountyElementSerializer


class BountySerializer(serializers.ModelSerializer):
    task = TaskSerializer()
    user_bounty = serializers.SerializerMethodField()

    class Meta:
        model = Bounty
        fields = ('id', 'task', 'annotations_target', 'user_bounty', 'closed')

    def get_user_bounty(self, obj):
        user_bounty = obj.get_user_bounty(self.context['request'].user)
        if user_bounty:
            user_bounty.update()
            return UserBountyElementSerializer(user_bounty).data
        return None
