import pytest

from tasks.models import Mission


@pytest.mark.django_db
def test_setup_tasks(setup_task_with_items):
    mission = Mission.objects.first()
    assert mission.packages.count() == 2

    package = mission.packages.all()[0]
    assert package.items.count() == 2

    item1, item2 = package.items.all()[0], package.items.all()[1]
    assert item1.data["value"] == "task1 item1"
    assert item2.data["value"] == "task2 item1"

    package = mission.packages.all()[1]
    assert package.items.count() == 2

    item1, item2 = package.items.all()[0], package.items.all()[1]
    assert item1.data["value"] == "task1 item2"
    assert item2.data["value"] == "task2 item2"
