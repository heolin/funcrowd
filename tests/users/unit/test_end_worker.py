from unittest.mock import MagicMock

import pytest

from funcrowd.settings import events_manager
from tasks.models import Mission
from tests.utils import add_annotation
from users.consts import ProfileType


@pytest.mark.django_db
@pytest.mark.parametrize("profile_type,events_calls_count",
                         [(ProfileType.NORMAL, 2), (ProfileType.MTURK, 0)])
def test_achievements_normal_profile(one_mission_two_tasks_with_items: Mission,
                                     profile_type, events_calls_count):
    task = one_mission_two_tasks_with_items.tasks.first()
    item = task.items.first()
    events_manager.on_event = MagicMock()

    from users.models import EndWorker
    user = EndWorker.objects.create_superuser(
        "user2@mail.com", "password", username="user2", profile=profile_type)

    add_annotation(item, user)
    assert events_manager.on_event.call_count == events_calls_count
