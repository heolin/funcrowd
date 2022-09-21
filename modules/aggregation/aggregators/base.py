from dataclasses import dataclass, field
from django.apps import apps
from django.db import transaction
from typing import Text, List, Dict

from .field_result import FieldResult
from .item_result import ItemResult
from .utils import normalize_answer_value, clean_answer_value


@dataclass
class FieldAnswers:
    field: Text
    answers: Dict[Text, int] = field(default_factory=dict)


@dataclass
class Answer:
    value: Text
    count: int


@dataclass
class ItemAnswers:
    item_id: int
    annotation_counts: int = field(default=0)
    field_answers: Dict[Text, FieldAnswers] = field(default_factory=dict)


class BaseAggregator:
    """
    Aggregates annotations and selects final answer for each
    annotation field in the item.

    Aggregation can be performed for all items in the task at once,
    or, if item object is passed in the constructor, just a single item.
    """

    def __init__(self, task, item=None, exclude_skipped=False):
        self.task = task
        self.item = item

        if self.item:
            self.template = self.item.template
        else:
            # if aggregation is done for the whole task, it will assume
            # that all items share the same template
            self.template = self.task.items.first().template

        self.exclude_skipped = exclude_skipped

    def _aggregate_annotations(self) -> List[ItemAnswers]:
        """
        Generates a data frame with all values for annotations
        from all fields from all users.

        :return: pd.DataFrame,
        """
        Annotation = apps.get_model("tasks.Annotation")
        annotations = Annotation.objects.filter(item__task=self.task).exclude(user=None)
        if self.item:
            annotations = annotations.filter(item_id=self.item)
        if self.exclude_skipped:
            annotations = annotations.exclude(skipped=True)

        fields_types = self._get_fields_types()

        # aggregate item answers
        item_answers = {}
        for data, item, _ in annotations.values_list("data", "item", "user__username").distinct():
            item_answer = item_answers.get(item, ItemAnswers(item))
            item_answer.annotation_counts += 1

            for field, value in data.items():
                field_answer = item_answer.field_answers.get(field, FieldAnswers(field))
                if fields_types[field] == 'list':
                    for val in value:
                        key = normalize_answer_value(val)
                        _answer = field_answer.answers.get(key, Answer(val, 0))
                        _answer.count += 1
                        field_answer.answers[key] = _answer
                else:
                    key = normalize_answer_value(value)
                    _answer = field_answer.answers.get(key, Answer(value, 0))
                    _answer.count += 1
                    field_answer.answers[key] = _answer

                item_answer.field_answers[field] = field_answer

            item_answers[item] = item_answer
        return list(item_answers.values())

    def _get_fields_types(self):
        Item = apps.get_model("tasks.Item")
        fields_types = {}
        if self.task:
            _items = Item.objects.filter(task=self.task)
        else:
            _items = Item.objects.filter(task=self.item.task)
        for value in _items.values(
                'template__fields__name', 'template__fields__type').distinct():
            fields_types[value['template__fields__name']] = value['template__fields__type']
        return fields_types

    def _logic(self, items_answers: List[ItemAnswers]) -> List[ItemResult]:
        """
        Aggregates annotations done for items and selects, one final answer

        :param items_answers: a list of ItemAnswers generated from `_aggregate_annotations`
        :return: a list of ItemResult, one for each item
        """

        item_results = []
        for item_answers in items_answers:
            item_result = ItemResult(item_answers.item_id, item_answers.annotation_counts)
            for field, field_answers in item_answers.field_answers.items():
                for _answer in field_answers.answers.values():
                    _probability = _answer.count / item_answers.annotation_counts
                    result = FieldResult(
                        clean_answer_value(_answer.value),
                        _probability,
                        _answer.count
                    )
                    item_result.add_answer(field, result)
            item_results.append(item_result)
        return item_results

    @transaction.atomic
    def aggregate(self):
        """
        Performs aggregation of answers for selected item/items,
        and updates ItemAggregation objects with the new values.

        :return: List[ItemAggregation]
        """
        ItemAggregation = apps.get_model("aggregation.ItemAggregation")
        aggregations = []
        for result in self._logic(self._aggregate_annotations()):
            aggregation, _ = ItemAggregation.objects.get_or_create(item_id=result.item_id)
            aggregation.data = result.to_json()
            aggregation.type = self.__class__.__name__
            aggregation.save()
            aggregations.append(aggregation)
        return aggregations
