import pytest

from tasks.models import Mission, Task


@pytest.mark.django_db
def test_achievements_count(achievements):
    mission = Mission.objects.get(id=1)
    assert mission.achievements_count == 4

    task = Task.objects.get(id=1)
    assert task.achievements_count == 1

    task = Task.objects.get(id=2)
    assert task.achievements_count == 1
