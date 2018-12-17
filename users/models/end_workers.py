from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
from users.models.utils.utils import get_group_number


class EndWorker(AbstractUser):
    group = models.IntegerField(default=get_group_number)

    @property
    def token(self):
        result, _ = Token.objects.get_or_create(user=self)
        return result
