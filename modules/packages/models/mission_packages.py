# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from modules.order_strategy.models import Strategy
from modules.order_strategy.models.strategy_client import IStrategyClient
from tasks.models.mission import Mission
from modules.packages.models.utils.query import UNFINISHED_PACKAGES_QUERY


class MissionPackages(models.Model, IStrategyClient):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name="packages")
    max_annotations = models.IntegerField(default=0)
    multiple_annotations = models.BooleanField(default=False)
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)

    def __str__(self):
        return "MissionPackages {}".format(self.mission.id)

    @property
    def items(self):
        return self.packages.all()

    def next_package(self, user, package):
        return self.next_item(user, package)

    def prev_package(self, user, package):
        return self.prev_item(user, package)

    def next_item(self, user, item):
        return self.strategy.next(self, user, item)

    def prev_item(self, user, item):
        return self.strategy.prev(self, user, item)

    def exclude_items_with_user_annotations(self, user):
        items_in_package = self.packages.first().items.count()
        packages = self.packages.filter(items__annotations__user=user)
        packages = packages.annotate(count=models.Count("items__annotations__user") / items_in_package)
        packages = packages.filter(count__gte=1)
        packages = self.packages.exclude(id__in=packages)
        return packages

    def exclude_max_annotations(self, items):
        from modules.packages.models.package import Package
        items_in_package = self.packages.first().items.count()
        unfinished_packages = Package.objects.raw(UNFINISHED_PACKAGES_QUERY,
                                                  [items_in_package, self.id, self.max_annotations])
        packages = Package.objects.filter(id__in=[p.id for p in unfinished_packages])
        packages = self.annotate_annotations_done(packages)
        return packages

    def annotate_annotations_done(self, packages):
        items_in_package = self.packages.first().items.count()
        return packages.annotate(
            annotations_done=models.Count('items__annotations__user') / items_in_package)

