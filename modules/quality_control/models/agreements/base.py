import pandas as pd
from abc import ABC, abstractmethod
from modules.quality_control.exceptions import MultipleTempaltesFound
from tasks.models import Annotation


class BaseAgreementMetric(ABC):
    def __init__(self, task):
        self.task = task
        self.template = task.items.first().template
        self.annotations = Annotation.objects.filter(item__task=task)
        self.df = pd.DataFrame(list(self.annotations.values_list("item_id", "data", "user_id")),
                               columns=["item_id", "data", "user_id"])

    def _check(self):
        if self.task.items.values_list("template_id", flat=True).distinct().count() > 1:
            raise MultipleTempaltesFound()

    def _get_pivot_table_counts(self, column):
        _df = self.df[["item_id", column]]
        _df = _df.pivot_table(index='item_id', columns=column, aggfunc=len, fill_value=0)
        _df = _df[_df.sum(axis=1) > 1]
        return _df

    def _get_pivot_table_annotations(self, column):
        _df = self.df[["user_id", column]]
        return _df.pivot_table(index='user_id', columns=column, aggfunc=len, fill_value=0)

    @abstractmethod
    def _metric(self, df, dfa):
        pass

    def evaluate(self):
        self._check()
        result = []
        for field in self.template.annotations_fields:
            self.df[field.name] = self.df["data"].apply(lambda x: x[field.name])
            _df = self._get_pivot_table_counts(field.name)
            _dfa = self._get_pivot_table_annotations(field.name)
            _value = self._metric(_df, _dfa)
            result.append(AgreementMetricResult(self.__class__.__name__, field.name, _value))
        return result


class AgreementMetricResult(object):
    def __init__(self, name, column, value):
        self.name = name
        self.column = column
        self.value = value
