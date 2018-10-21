import pytest

from django.db import IntegrityError
from modules.order_strategy.models import Strategy


@pytest.mark.django_db
def test_create_only_one_per_name():
    Strategy.objects.create(name="SomeStrategy")

    with pytest.raises(IntegrityError):
        Strategy.objects.create(name="SomeStrategy")
