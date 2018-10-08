import pytest
from rest_framework.test import APIRequestFactory


@pytest.mark.django_db
def test_item(setup_task):
    factory = APIRequestFactory()

