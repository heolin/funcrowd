import pytest
from django.db import IntegrityError

from modules.statistics.models import MissionStats
from tasks.models import Mission


@pytest.mark.django_db
def test_multiple_create(setup_tasks):
    mission = Mission.objects.first()
    assert mission.stats

    with pytest.raises(IntegrityError):
        MissionStats.objects.create(mission=mission)


@pytest.mark.django_db
def test_mission_stats_no_data(setup_tasks):
    mission = Mission.objects.first()
    stats = mission.stats

    assert stats.total_finished_documents == 3
    assert stats.total_documents == 6
    assert stats.total_finished_items == 0
    assert stats.total_users == 0
    assert stats.total_tasks == 3


@pytest.mark.django_db
def test_mission_stats_task_data(setup_tasks_annotations):
    mission = Mission.objects.get(name="Test mission 4")
    stats = mission.stats

    assert stats.total_finished_documents == 10
    assert stats.total_finished_items == 10
    assert stats.total_documents == 10
    assert stats.total_users == 14
    assert stats.total_tasks == 1
