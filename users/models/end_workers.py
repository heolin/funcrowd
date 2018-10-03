from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token


class EndWorker(AbstractUser):

    def setup(self):
        print("CREATING TOKEN")
        Token.objects.get_or_create(user=self)

