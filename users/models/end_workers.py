from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token

from modules.statistics.models import UserStats, UserMissionStats
from users.models.utils.utils import get_group_number


class EndWorker(AbstractUser):
    group = models.IntegerField(default=get_group_number)

    @property
    def token(self):
        result, _ = Token.objects.get_or_create(user=self)
        return result

    @property
    def stats(self):
        if not self.my_stats:
            UserStats.objects.create(mission=self)
        return self.my_stats

    def get_mission_stats(self, mission_id):
        stats = self.my_mission_stats.filter(mission_id=mission_id).first()
        if not stats:
            stats, _ = UserMissionStats.objects.get_or_create(user=self, mission_id=mission_id)
        return stats
