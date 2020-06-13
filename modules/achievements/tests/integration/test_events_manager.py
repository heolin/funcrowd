import pytest

from modules.achievements.events import Events
from modules.achievements.events_manager import EventsManager
from modules.achievements.models import ItemDoneAchievement, ProgressAchievement, LoginCountAchievement


@pytest.mark.django_db
def test_achievement_register():
    event_manager = EventsManager()
    assert len(event_manager._achievements) == 0

    event_manager.register_achievements(ItemDoneAchievement)
    assert len(event_manager._achievements) == 1
    assert Events.ON_ITEM_DONE in event_manager._achievements
    assert len(event_manager._achievements[Events.ON_ITEM_DONE]) == 1
    assert ItemDoneAchievement in event_manager._achievements[Events.ON_ITEM_DONE]

    event_manager.register_achievements(ProgressAchievement)
    assert len(event_manager._achievements) == 1
    assert Events.ON_ITEM_DONE in event_manager._achievements
    assert len(event_manager._achievements[Events.ON_ITEM_DONE]) == 2
    assert ItemDoneAchievement in event_manager._achievements[Events.ON_ITEM_DONE]

    event_manager.register_achievements(LoginCountAchievement)
    assert len(event_manager._achievements) == 2
    assert Events.ON_ITEM_DONE in event_manager._achievements
    assert len(event_manager._achievements[Events.ON_LOGIN]) == 1
    assert LoginCountAchievement in event_manager._achievements[Events.ON_LOGIN]

