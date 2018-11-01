# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from sortedm2m.fields import SortedManyToManyField
from tasks.models.item import Item
from modules.packages.models.mission_packages import MissionPackages


class Package(models.Model):
    parent = models.ForeignKey(MissionPackages, on_delete=models.CASCADE, related_name="packages")
    items = SortedManyToManyField(Item)
    order = models.IntegerField(default=0)

    def __str__(self):
        return "Package {} {}".format(self.parent.mission.id, self.order)

    class Meta:
        ordering = ['order']


# Trying to achieve results as following query
"""
select 
	A.id,
	SUM(full_annotations) as annotations_done
from
	(select
		"packages_package"."id",
		"tasks_annotation"."user_id",
		(COUNT("tasks_annotation"."id") / 2) AS "full_annotations"
	from
		"packages_missionpackages"
		LEFT OUTER JOIN "packages_package" ON ("packages_missionpackages"."id" = "packages_package"."parent_id")
		LEFT OUTER JOIN "packages_package_items" ON ("packages_package"."id" = "packages_package_items"."package_id")
		LEFT OUTER JOIN "tasks_item" ON ("packages_package_items"."item_id" = "tasks_item"."id")
		LEFT OUTER JOIN "tasks_annotation" ON ("tasks_item"."id" = "tasks_annotation"."item_id")
	where
		"packages_missionpackages"."mission_id" = 1
	group by
		"packages_package"."id", "tasks_annotation"."user_id") as A
group by
	A.id
    """

"""
items_in_package = 2
mission.packages.values(
    "packages", "packages__items__annotations__user"
).annotate(
    full_annotations=Sum('packages__items__annotations__user')/items_in_package
).values(
    "packages", "full_annotations"
).annotate(
    total_annotations=Sum("full_annotations")
) """
