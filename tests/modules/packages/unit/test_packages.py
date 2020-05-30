import pytest

from tasks.models import Mission


@pytest.mark.django_db
def test_setup_tasks(task_with_items_in_packages):
    mission = Mission.objects.first()
    assert mission.packages is not None

    mp = mission.packages
    assert mp.packages.count() == 5

    package = mp.packages.all()[0]
    assert package.items.count() == 2
    item1, item2 = package.items.all()[0], package.items.all()[1]
    assert item1.data["data_field"] == "task1 item1"
    assert item2.data["data_field"] == "task2 item1"

    package = mp.packages.all()[1]
    item1, item2 = package.items.all()[0], package.items.all()[1]
    assert item1.data["data_field"] == "task1 item2"
    assert item2.data["data_field"] == "task2 item2"
