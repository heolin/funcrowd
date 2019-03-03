import pandas as pd
from abc import ABC, abstractmethod

from modules.aggregation.models.item_aggregation import ItemAggregation
from tasks.models import Annotation


class AggregationResult(object):
    def __init__(self, item_id, data):
        self.item_id = item_id
        self.data = data


class BaseAggregation(ABC):
    def __init__(self, task):
        self.task = task

    @abstractmethod
    def _logic(self, df) -> [AggregationResult]:
        return []

    def _get_annotations_table(self):
        result = []
        annotations = Annotation.objects.filter(item__task=self.task).exclude(user=None)
        for data, item, user in annotations.values_list("data", "item", "user__username"):
            data['item'] = item
            data['user'] = user
            result.append(data)
        return pd.DataFrame(result)

    def aggregate(self):
        aggregations = []
        for result in self._logic(self._get_annotations_table()):
            aggregation, _ = ItemAggregation.objects.get_or_create(item_id=result.item_id)
            aggregation.data = result.data
            aggregation.type = self.__class__.__name__
            aggregations.append(aggregation)
        return aggregations

