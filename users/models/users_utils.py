
from rest_framework.authtoken.models import Token

def setup_user(user):
    Token.objects.get_or_create(user=user)

