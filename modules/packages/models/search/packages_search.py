from django.db import models
from django.db.models import Count, Q, Sum

from modules.packages.consts import UserPackageStatus
from modules.packages.models.utils.query import UNFINISHED_PACKAGES_QUERY
from modules.packages.models.package import Package
from modules.order_strategy.models.strategy_client import IStrategyClient
from tasks.consts import VERIFICATION, FINISHED


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

    def exclude_items_with_user_annotations(self, packages, user):
        # excluded packages already finished by the user
        user_packages = self.mission_packages.packages.filter(
            progress__user=user, progress__status=UserPackageStatus.FINISHED)
        packages = packages.exclude(id__in=user_packages)
        return packages

    def exclude_max_annotations(self, packages):
        # collects all unfinished packages
        packages = self.annotate_annotations_done(packages)  # adding items done by user, used for sorting
        return packages

    def annotate_annotations_done(self, packages):
        packages = packages.annotate(
            annotations_done=Sum(
                models.Case(
                    models.When(progress__status=UserPackageStatus.FINISHED, then=1),
                    default=0,
                    output_field=models.IntegerField()
                )
            )
        )
        return packages
