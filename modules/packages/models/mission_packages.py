# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging

from django.apps import apps
from django.db import models

from modules.order_strategy.models import Strategy
from tasks.models.mission import Mission

# -*- coding: utf-8 -*-

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

    def create_package(self, size: int):
        """
        Creates a new package for this Bounty using a random sample
        of unassigned items (items without a package) of selected size.

        :param size: determines how many items will be put into a new package
        :return package: a new package with a random sample of items
        """
        Package = apps.get_model("packages.Package")
        Item = apps.get_model("tasks.Item")

        unassigned_items = Item.objects.filter(
            task__mission=self.mission
        ).filter(
            item__package=None
        ).order_by("?")

        if unassigned_items:
            if len(unassigned_items) < size:
                size = len(unassigned_items)
                log.warning("Insufficient number of unassigned items."
                            f"Creating a package with {size} items.")
            package = Package.objects.create(
                parent=self,
                order=self.packages.count()
            )

            for item in unassigned_items.all()[:size]:
                item.package = package
                item.save()

            return package
