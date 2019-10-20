from rest_framework import serializers

from modules.bounty.models import UserBounty


class UserBountySerializer(serializers.ModelSerializer):
    annotations_target = serializers.IntegerField(source='bounty.annotations_target')
    rewards_list = serializers.SerializerMethodField()

    class Meta:
        model = UserBounty
        fields = ('id', 'bounty', 'status', 'progress', 'reward',
                  'annotations_done', 'annotations_target', 'rewards_list')

    def get_rewards_list(self, obj):
        user_bounties = UserBounty.objects.filter(bounty=obj.bounty, user=obj.user)
        rewards = []
        for user_bounty in user_bounties:
            reward = user_bounty.reward
            if reward:
                rewards.append(reward)
        return rewards


class UserBountyElementSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserBounty
        fields = ('id', 'progress', 'status', 'annotations_done')
