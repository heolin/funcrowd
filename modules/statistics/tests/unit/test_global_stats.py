import pytest
from django.db import IntegrityError

from modules.statistics.models import GlobalStats


@pytest.mark.django_db
def test_multiple_create():
    GlobalStats.objects.create()

    with pytest.raises(IntegrityError):
        GlobalStats.objects.create()


@pytest.mark.django_db
def test_global_stats_no_data():
    stats = GlobalStats.objects.create()
    assert stats.total_finished_documents == 0
    assert stats.total_documents == 0
    assert stats.total_missions == 0
    assert stats.total_users == 0
    assert stats.total_tasks == 0


@pytest.mark.django_db
def test_global_stats_tasks_data(setup_user, setup_tasks):
    stats = GlobalStats.objects.create()
    assert stats.total_finished_documents == 6
    assert stats.total_documents == 13
    assert stats.total_missions == 3
    assert stats.total_users == 1
    assert stats.total_tasks == 6
