import pytest

from modules.achievements.consts import Status
from modules.achievements.models import UserAchievement, ItemDoneAchievement
from tasks.models import Item


@pytest.mark.django_db
def test_item_done_logic(user1, achievements):

    achievement = ItemDoneAchievement.objects.filter(order=1).first()
    assert achievement

    user_achievement = UserAchievement.objects.create(user=user1, achievement=achievement)
    user_achievement.update()
    assert user_achievement.value == 0

    # annotate at least one item in any task
    item = Item.objects.filter(task__mission_id=1, order=1).first()
    annotation, _ = item.get_or_create_annotation(user1)
    annotation.data = {"output": 1}
    annotation.save()

    # annotated=False rejected=False skipped=False
    user_achievement.update()
    assert user_achievement.value == 0
    assert user_achievement.status == Status.NEW

    # annotated=True rejected=True skipped=False
    annotation.annotated = True
    annotation.rejected = True
    annotation.save()

    user_achievement.update()
    assert user_achievement.value == 0

    # annotated=True rejected=False skipped=True
    annotation.rejected = False
    annotation.skipped = True
    annotation.save()

    user_achievement.update()
    assert user_achievement.value == 0

    # annotated=True rejected=False skipped=False
    annotation.annotated = True
    annotation.rejected = False
    annotation.skipped = False
    annotation.save()

    user_achievement.update()
    assert user_achievement.value == 1
    assert user_achievement.status == Status.FINISHED

    # annotate two items in mission
    achievement = ItemDoneAchievement.objects.filter(order=2).first()
    user_achievement = UserAchievement.objects.create(user=user1, achievement=achievement)
    user_achievement.update()
    assert user_achievement.value == 1
    assert user_achievement.status == Status.IN_PROGRESS

    item = Item.objects.filter(task__mission_id=1, order=2).first()
    annotation, _ = item.get_or_create_annotation(user1)
    annotation.annotated = True
    annotation.data = {"output": 1}
    annotation.save()

    user_achievement.update()
    assert user_achievement.value == 2
    assert user_achievement.status == Status.FINISHED

    # annotate one item from other task
    achievement = ItemDoneAchievement.objects.filter(order=3).first()
    user_achievement = UserAchievement.objects.create(user=user1, achievement=achievement)
    user_achievement.update()
    assert user_achievement.value == 0
    assert user_achievement.status == Status.NEW

    item = Item.objects.filter(task_id=2, order=1).first()
    annotation, _ = item.get_or_create_annotation(user1)
    annotation.data = {"output": 1}
    annotation.annotated = True
    annotation.save()

    user_achievement.update()
    assert user_achievement.value == 1
    assert user_achievement.status == Status.FINISHED
