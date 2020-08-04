# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models

from tasks.consts import MissionStatus, MISSION_STATUSES, TaskStatus
from tasks.models import Mission, UserTaskProgress, Annotation
from users.models.end_workers import EndWorker


class UserMissionProgress(models.Model):
    user = models.ForeignKey(EndWorker, on_delete=models.CASCADE)
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    tasks_done = models.IntegerField(default=0)
    status = models.CharField(choices=MISSION_STATUSES, max_length=32)
    exp = models.IntegerField(default=0)
    bonus_exp = models.IntegerField(default=0)

    def __str__(self):
        return f"UserMissionProgress({self.user}, {self.mission}, {self.status})"

    def save(self, *args, **kwargs):
        if not self.status:
            if self.mission.initial_status:
                self.status = self.mission.initial_status
            else:
                self.status = MissionStatus.LOCKED
        super(UserMissionProgress, self).save(*args, **kwargs)

    def update(self):
        self.tasks_done = UserTaskProgress.objects.filter(
            user=self.user, task__mission=self.mission,
            status__in=[TaskStatus.FINISHED, TaskStatus.PERMANENT]).count()

        self.update_status(False)
        self.update_exp(False)
        self.save()

    def update_exp(self, commit=True):
        last_exp = self.exp

        self.exp = Annotation.objects.filter(
            item__task__mission=self.mission, user=self.user
        ).aggregate(models.aggregates.Sum('exp'))['exp__sum']

        if self.exp and commit and last_exp != self.exp:
            self.save()

    def update_status(self, commit=True):
        parent_progress = self._get_parent_progress()
        if not parent_progress and self.mission.parent:
            return

        last_status = self.status

        if self.status == MissionStatus.LOCKED:
            if not parent_progress:
                self.status = MissionStatus.UNLOCKED
            elif parent_progress.status == MissionStatus.FINISHED:
                self.status = MissionStatus.UNLOCKED
        if self.status == MissionStatus.UNLOCKED:
            if self.tasks_done > 0:
                self.status = MissionStatus.IN_PROGRESS
        if self.status == MissionStatus.IN_PROGRESS:
            if self.tasks_done == self.tasks_count:
                self.status = MissionStatus.FINISHED

        if commit and last_status != self.status:
            self.save()

    def _get_parent_progress(self):
        parent_progress = None
        if self.mission.parent:
            parent_progress = UserMissionProgress.objects.filter(
                mission=self.mission.parent,
                user=self.user
            ).first()
        return parent_progress

    @property
    def progress(self):
        if self.tasks_count:
            return self.tasks_done / self.tasks_count

    @property
    def tasks_count(self):
        return self.mission.tasks.count()

    @property
    def total_exp(self):
        return self.exp + self.bonus_exp
