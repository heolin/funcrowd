from django.db import models
from django.utils import timezone

from funcrowd.settings import ACCOUNT_EMAIL_EXPIRATION_HOURS
from users.models.utils.utils import get_reward_token


class ActivationToken(models.Model):
    token = models.CharField(max_length=32, default=get_reward_token())
    user = models.ForeignKey("EndWorker", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    token_used = models.BooleanField(default=False)

    @property
    def is_expired(self):
        expiration_time = self.created + timezone.timedelta(hours=ACCOUNT_EMAIL_EXPIRATION_HOURS)
        return timezone.now() > expiration_time

    def activate(self):
        self.user.is_active = True
        self.user.save()
        self.token_used = True
        self.save()
