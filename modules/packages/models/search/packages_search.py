from django.db import models
from django.db.models import Count, Q

from modules.packages.consts import UserPackageStatus
from modules.packages.models.utils.query import UNFINISHED_PACKAGES_QUERY
from modules.packages.models.package import Package
from modules.order_strategy.models.strategy_client import IStrategyClient


class PackagesSearch(IStrategyClient):
    def __init__(self, mission_packages, search):
        self.mission_packages = mission_packages
        self.search = {
            f"metadata__{key}": value
            for (key, value) in search.items()
        }

    @property
    def multiple_annotations(self):
        return False

    @property
    def max_annotations(self):
        return self.mission_packages.max_annotations

    @property
    def items(self):
        return self.mission_packages.packages.filter(**self.search)

    @property
    def items_in_package(self):
        return self.mission_packages.packages.first().items.count()

    def next_package(self, user, package):
        return self.next_item(user, package)

    def prev_package(self, user, package):
        return self.prev_item(user, package)

    def next_item(self, user, item):
        return self.mission_packages.strategy.next(self, user, item)

    def prev_item(self, user, item):
        return self.mission_packages.strategy.prev(self, user, item)

    def exclude_items_with_user_annotations(self, user):
        # excluded packages already finished by the user
        packages = self.mission_packages.packages.filter(
            progress__user=user, progress__status=UserPackageStatus.FINISHED)
        packages = self.items.exclude(id__in=packages)
        return packages

    def exclude_max_annotations(self, packages):
        # collects all unfinished packages
        packages = packages.filter(**self.search)
        packages = packages.annotate(
            packages_done=Count("progress", only=Q(progress__status=UserPackageStatus.FINISHED)))
        if self.mission_packages.max_annotations > 0:
            packages = packages.filter(packages_done__lt=self.mission_packages.max_annotations)
        packages = self.annotate_annotations_done(packages)  # adding items done by user, used for sorting
        return packages

    def annotate_annotations_done(self, packages):
        return packages.annotate(
            annotations_done=models.Count('items__annotations__user') / self.items_in_package)