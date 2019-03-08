import pandas as pd
from abc import ABC, abstractmethod

from modules.aggregation.models.item_aggregation import ItemAggregation
from tasks.models import Annotation


class AggregationResult(object):
    def __init__(self, item_id, data):
        self.item_id = item_id
        self.data = data


class BaseAggregation(ABC):
    def __init__(self, task, item=None, exclude_skipped=False):
        self.task = task
        self.item = item
        self.exclude_skipped = exclude_skipped

    @abstractmethod
    def _logic(self, df) -> [AggregationResult]:
        return []

    def _get_annotations_table(self):
        result = []

        annotations = Annotation.objects.filter(item__task=self.task).exclude(user=None)
        if self.item:
            annotations = annotations.filter(item_id=self.item)
        if self.exclude_skipped:
            annotations = annotations.exclude(skipped=True)

        for data, item, user in annotations.values_list("data", "item", "user__username"):
            data['item'] = item
            data['user'] = user
            for field in self.item.template.annotations_fields:
                if field.name not in data:
                    data[field.name] = None
            result.append(data)
        return pd.DataFrame(result).fillna("<EMPTY>")

    def aggregate(self):
        aggregations = []
        for result in self._logic(self._get_annotations_table()):
            aggregation, _ = ItemAggregation.objects.get_or_create(item_id=result.item_id)
            aggregation.data = result.data
            aggregation.type = self.__class__.__name__
            aggregation.save()
            aggregations.append(aggregation)
        return aggregations
