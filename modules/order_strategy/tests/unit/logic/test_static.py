import pytest


@pytest.mark.django_db
def test_static():
    assert 1 > 0
