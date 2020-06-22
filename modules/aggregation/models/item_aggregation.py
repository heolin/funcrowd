# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import numpy as np
from django.contrib.postgres.fields import JSONField
from django.db import models

from modules.aggregation.aggregators import ItemResult


class ItemAggregation(models.Model):
    """
    ItemAggregation stores aggregated information about EndWorkers answers.
    The `data` field contains an output from the `Aggregator` in a form of
    sterialized `ItemResult`.
    """

    data = JSONField(blank=True, null=True)
    item = models.ForeignKey("tasks.Item", on_delete=models.CASCADE, related_name="aggregations")
    created = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=20, choices=None)

    def __init__(self, *args, **kwargs):
        super(ItemAggregation, self).__init__(*args, **kwargs)
        self._item_result = None  # cache field used to store deserialized ItemResult stored in `data`

    class Meta:
        verbose_name_plural = "ItemAggregations"

    @property
    def item_result(self):
        if not self._item_result:
            self._item_result = ItemResult.from_json(self.data)
        return self._item_result

    def __str__(self):
        return f"{self.__class__.__name__}(#{self.id} - {self.item.id}"

    def get_probability(self) -> float:
        """
        Aggregated value of probabilities for this items.
        Computed as a average from all its field results' probabilities.
        For ListFieldResults, all values are counted separately.
        """
        if not self.item_result:
            return 0.0

        values = []
        for field_name, field_results in self.item_result.answers.items():
            for field_result in field_results:
                values.append(field_result.probability)
        if values:
            return np.average(values)
        return 0.0

    def get_support(self) -> int:
        """
        Aggregated value of support for this items.
        Computed as a max from all its field results' support.
        For ListFieldResults, all values are counted separately.
        """
        if not self.item_result:
            return 0

        values = []
        for field_name, field_results in self.item_result.answers.items():
            for field_result in field_results:
                values.append(field_result.support)
        if values:
            return np.max(values)
        return 0

    def get_annotations_count(self) -> int:
        """
        Total annotations made
        """
        if not self.item_result:
            return 0

        return self.item_result.annotations_count

