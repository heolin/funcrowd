from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token


class EndWorker(AbstractUser):
    @property
    def token(self):
        result, _ = Token.objects.get_or_create(user=self)
        return result
