from datetime import timedelta

import pytest
from django.test import Client

from modules.achievements.models import UserAchievement, UnlockMissionAfterTaskAchievement
from modules.achievements.consts import Status
from tasks.consts import MissionStatus
from tasks.models import Annotation


@pytest.mark.django_db
def test_unlock_mission_after_login(user1, hidden_mission):
    days = 30
    mission = hidden_mission
    progress = user1.get_mission_progress(mission)
    assert progress.status == MissionStatus.LOCKED

    achievement = UnlockMissionAfterTaskAchievement.objects.create(
        order=5, task_id=1, mission=hidden_mission, exp=0, target=days)

    user_achievement = UserAchievement.objects.create(user=user1, achievement=achievement)
    user_achievement.update()
    assert user_achievement.progress == 0

    task = achievement.task
    for item in task.items.all():
        annotation = Annotation.objects.create(
            item=item,
            data={"output": 1},
            annotated=True,
            user=user1
        )
        annotation.created = annotation.created - timedelta(days=days)
        annotation.save()
        user1.on_annotation(annotation)

    client = Client()
    payload = {
        "email": "user1@mail.com",
        "password": "password",
    }
    response = client.post('/api/v1/users/login/', payload)
    assert response.status_code == 200

    user_achievement = UserAchievement.objects.get(user=user1, achievement=achievement)
    assert user_achievement.progress == 1
    assert user_achievement.status == Status.FINISHED

    progress = user1.get_mission_progress(mission)
    assert progress.status == MissionStatus.UNLOCKED


@pytest.mark.django_db
def test_unlock_mission_after_list(user1, hidden_mission):
    days = 30
    mission = hidden_mission
    progress = user1.get_mission_progress(mission)
    assert progress.status == MissionStatus.LOCKED

    achievement = UnlockMissionAfterTaskAchievement.objects.create(
        order=5, task_id=1, mission=hidden_mission, exp=0, target=days)

    user_achievement = UserAchievement.objects.create(user=user1, achievement=achievement)
    user_achievement.update()
    assert user_achievement.progress == 0

    task = achievement.task
    for item in task.items.all():
        annotation = Annotation.objects.create(
            item=item,
            data={"output": 1},
            annotated=True,
            user=user1
        )
        annotation.created = annotation.created - timedelta(days=days)
        annotation.save()
        user1.on_annotation(annotation)

    client = Client()
    client.force_login(user1)
    response = client.get('/api/v1/achievements/')
    assert response.status_code == 200

    user_achievement = UserAchievement.objects.get(user=user1, achievement=achievement)
    assert user_achievement.progress == 1
    assert user_achievement.status == Status.FINISHED

    progress = user1.get_mission_progress(mission)
    assert progress.status == MissionStatus.UNLOCKED


