# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging

from django.apps import apps
from django.db import models

from modules.order_strategy.models import Strategy
from tasks.models import Mission, Task

# -*- coding: utf-8 -*-
from modules.packages.exceptions import InsufficientUnassignedItems

log = logging.getLogger(__name__)


class MissionPackages(models.Model):
    """
    Mainly created for a purpose of creating HIT tasks on mturk.
    Bounties provide a mechanism to generate a reward code
    for completing annotations for one package.

    For each user that will be working on the Bounty, system
    will create an UserPackageProgress object. After user finish his annotation,
    UserPackageProgress.reward will return an unique token that can be displayed
    to the user, as a verification that he finished his worked.
    Then, user can copy the token to mturk's form.
    """
    mission = models.OneToOneField(Mission, on_delete=models.CASCADE,
                                   related_name="packages")
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)
    max_annotations = models.IntegerField()
    instruction = models.TextField(default="", blank=True)
    closed = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)

    def __str__(self):
        return f"MissionPackages(#{self.id}) - Mission(${self.mission.id})"

    def close(self):
        """
        Used to close all Packages and stop further annotation of its Packages.
        """
        for package in self.packages.all():
            package.close()

    def create_package(self, size: int, name: str = "",
                       metadata: dict = None, task: Task = None):
        """
        Creates a new package for this Bounty using a random sample
        of unassigned items (items without a package) of selected size.

        :param size: determines how many items will be put into a new package
        :param metadata: metadata of the package
        :param name: name of the package
        :param task: used to filter items only from a selected task
        :return package: a new package with a random sample of items
        """
        Package = apps.get_model("packages.Package")
        Item = apps.get_model("tasks.Item")

        metadata = metadata or {}  # sets default value to {}

        unassigned_items = Item.objects.filter(task__mission=self.mission)
        if task:
            unassigned_items = unassigned_items.filter(task=task)
        unassigned_items = unassigned_items.filter(package=None).order_by("?")

        if len(unassigned_items) < size:
            raise InsufficientUnassignedItems()

        package = Package.objects.create(
            name=name,
            parent=self,
            order=self.packages.count(),
            metadata=metadata
        )

        for item in unassigned_items.all()[:size]:
            item.package = package
            item.save()

        return package
