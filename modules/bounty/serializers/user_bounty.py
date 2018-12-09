from rest_framework import serializers

from modules.bounty.models import UserBounty


class UserBountySerializer(serializers.ModelSerializer):
    annotations_target = serializers.IntegerField('bounty.annotations_target')

    class Meta:
        model = UserBounty
        fields = ('id', 'bounty', 'status', 'progress', 'reward',
                  'annotations_done', 'annotations_target')
