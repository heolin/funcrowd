import pytest

from tasks.models import Mission


@pytest.mark.django_db
def test_mission(setup_task):
    assert Mission.objects.count() == 2
    assert Mission.objects.all()[0].tasks.count() == 1
    assert Mission.objects.all()[1].tasks.count() == 0


@pytest.mark.django_db
def test_create_mission():
    mission = Mission.objects.create(name="Test mission")
    assert mission.name == "Test mission"
    assert mission.description == ""

    mission = Mission.objects.create(name="Test mission other", description="Description")
    assert mission.name == "Test mission other"
    assert mission.description == "Description"


@pytest.mark.django_db
def test_missions_order():
    Mission.objects.create(name="Mission A", order=1)
    Mission.objects.create(name="Mission B", order=0)

    Mission.objects.first().name == "Mission B"
