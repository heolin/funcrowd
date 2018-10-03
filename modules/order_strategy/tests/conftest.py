import pytest

from tasks.models import (
    Mission, Task, Item, ItemTemplate, ItemTemplateField, Annotation
)



@pytest.fixture
@pytest.mark.django_db
def setup_task():
    mission = Mission.objects.create(id=1, name="Test mission")
    Task.objects.create(id=1, mission=mission, name="Add two digits")

    Mission.objects.create(id=2, name="Test mission other")
