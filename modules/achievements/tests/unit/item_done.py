import pytest

from modules.achievements.consts import Status
from modules.achievements.models import UserAchievement, ItemDoneAchievement
from tasks.models import Item


@pytest.mark.django_db
def test_item_done_logic(setup_user1, setup_achievements):

    user = setup_user1

    achievement = ItemDoneAchievement.objects.filter(order=1).first()
    assert achievement

    user_achievement = UserAchievement.objects.create(user=user, achievement=achievement)
    user_achievement.update()
    assert user_achievement.value == 0

    # annotate at least one item in any task
    item = Item.objects.filter(task__mission_id=1, order=1).first()
    annotation, _ = item.get_or_create_annotation(user)
    annotation.data = {"output": 1}
    annotation.save()

    user_achievement.update()
    assert user_achievement.value == 1
    assert user_achievement.status == Status.FINISHED

    # annotate two items in mission
    achievement = ItemDoneAchievement.objects.filter(order=2).first()
    user_achievement = UserAchievement.objects.create(user=user, achievement=achievement)
    user_achievement.update()
    assert user_achievement.value == 1
    assert user_achievement.status == Status.IN_PROGRESS

    item = Item.objects.filter(task__mission_id=1, order=2).first()
    annotation, _ = item.get_or_create_annotation(user)
    annotation.data = {"output": 1}
    annotation.save()

    user_achievement.update()
    assert user_achievement.value == 2
    assert user_achievement.status == Status.FINISHED

    # annotate one item from other task
    achievement = ItemDoneAchievement.objects.filter(order=3).first()
    user_achievement = UserAchievement.objects.create(user=user, achievement=achievement)
    user_achievement.update()
    assert user_achievement.value == 0
    assert user_achievement.status == Status.NEW

    item = Item.objects.filter(task_id=2, order=1).first()
    annotation, _ = item.get_or_create_annotation(user)
    annotation.data = {"output": 1}
    annotation.save()

    user_achievement.update()
    assert user_achievement.value == 1
    assert user_achievement.status == Status.FINISHED
