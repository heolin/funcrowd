from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token

from django.apps import apps
from funcrowd.settings import events_manager
from modules.achievements.events import Events
from modules.statistics.models import UserStats, UserMissionStats
from users.consts import ProfileType, ACHIEVEMENTS_PROFILES
from users.models.manager import EndWorkerManager
from users.models.storage import Storage
from users.models.utils.utils import get_group_number
from django.utils.translation import ugettext_lazy as _


import tasks as t


class EndWorker(AbstractUser):
    """
    Custom user model.
    """

    email = models.EmailField(_('email address'), unique=True)

    group = models.IntegerField(default=get_group_number)
    profile = models.IntegerField(default=ProfileType.NORMAL)

    login_count = models.IntegerField(default=0)
    exp = models.IntegerField(default=0)
    level = models.IntegerField(default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = EndWorkerManager()

    def __str__(self):
        return f"EndWorker(id={self.id}, username={self.username}, " \
               f"email={self.email}, profile={self.profile}, exp={self.exp})"

    @property
    def token(self):
        """
        Gets or create authentication Token.
        :return: Token
        """
        result, _ = Token.objects.get_or_create(user=self)
        return result

    @property
    def stats(self):
        stats, _ = UserStats.objects.get_or_create(user=self)
        return stats

    def create_activation_token(self):
        """
        Creates a new ActivationToken used for activating user's account after registration.
        If there is any previously created token, then it will disable it.
        :return: ActivationToken
        """

        ActivationToken = apps.get_model("users.ActivationToken")

        for token in ActivationToken.objects.filter(user=self):
            token.token_used = True
            token.save()
        return ActivationToken.objects.create(user=self)

    def create_password_token(self):
        """
        Creates a new PasswordToken used for resetting the user's password.
        If there is any previously created token, then it will disable it.
        :return: PasswordToken
        """
        PasswordToken = apps.get_model("users.PasswordToken")

        for token in PasswordToken.objects.filter(user=self):
            token.token_used = True
            token.save()
        return PasswordToken.objects.create(user=self)

    def get_storage(self, key: str):
        """
        Get or creates a storage objects for a certain key
        :param key: str
        :return: Storage
        """
        storage, _ = Storage.objects.get_or_create(user=self, key=key)
        return storage

    def set_storage(self, key, data):
        """
        Used to set the storage value for a selected key
        :param key: str
        :param data: dict
        """
        storage = self.get_storage(key)
        storage.data = data
        storage.save()

    def get_task_progress(self, task, update=True):
        # move this part to Task
        progress, _ = t.models.task_progress.UserTaskProgress.objects.get_or_create(
            task=task, user=self)
        if update:
            progress.update_status()
        return progress

    def get_mission_stats(self, mission_id):
        # move this part to Mission
        stats, _ = UserMissionStats.objects.get_or_create(user=self, mission_id=mission_id)
        return stats

    def get_mission_progress(self, mission, update=True):
        # move this part to Mission
        progress, _ = t.models.mission_progress.UserMissionProgress.objects.get_or_create(
            mission=mission, user=self)
        if update:
            progress.update_status()
        return progress

    def on_login(self):
        """
        Function run after each successful login.
        Updated total login_count and requests to update all achievements.
        """
        self.login_count += 1
        self.save()
        events_manager.update_all(self)

    def on_annotation(self, annotation):
        """
        Run after each annotation. Used to update progress of all objects that
        keeps track of annotations progress, such as:
        UserTaskProgress, UserMissionProgress, UserPackageProgress, and updates
        achievements events.
        :param annotation: Annotation
        """
        task_progress = self.get_task_progress(annotation.item.task)
        task_progress.update()

        mission_progress = self.get_mission_progress(annotation.item.task.mission)
        mission_progress.update()

        if annotation.item.package:
            package_progress = annotation.item.package.get_user_progress(self)
            package_progress.update()

        if self.profile in ACHIEVEMENTS_PROFILES:
            events_manager.on_event(self, Events.ON_ITEM_DONE)
            events_manager.on_event(self, Events.ALWAYS)

    def add_exp(self, exp: int):
        """
        Used to accumulate the total experience points of the player.
        :param exp: int
        """
        self.exp += exp
        self.save()


