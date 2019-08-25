from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token

from modules.statistics.models import UserStats, UserMissionStats
from users.models.storage import Storage
from users.models.utils.utils import get_group_number

import tasks as t


class EndWorker(AbstractUser):
    group = models.IntegerField(default=get_group_number)

    @property
    def token(self):
        result, _ = Token.objects.get_or_create(user=self)
        return result

    @property
    def stats(self):
        stats, _ = UserStats.objects.get_or_create(user=self)
        return stats

    def get_mission_stats(self, mission_id):
        stats, _ = UserMissionStats.objects.get_or_create(user=self, mission_id=mission_id)
        return stats

    def get_storage(self, key):
        storage = Storage.objects.filter(user=self, key=key).first()
        if not storage:
            storage = Storage.objects.create(user=self, key=key)
        return storage

    def set_storage(self, key, data):
        storage = self.get_storage(key)
        storage.data = data
        storage.save()

    def get_task_progress(self, task):
        progress, _ = t.models.task_progress.UserTaskProgress.objects.get_or_create(task=task, user=self)
        return progress

    def get_mission_progress(self, mission):
        progress, _ = t.models.mission_progress.UserMissionProgress.objects.get_or_create(mission=mission, user=self)
        return progress

    def on_annotation(self, annotation):
        task_progress = self.get_task_progress(annotation.item.task)
        task_progress.update()
        mission_progress = self.get_mission_progress(annotation.item.task.mission)
        mission_progress.update()
