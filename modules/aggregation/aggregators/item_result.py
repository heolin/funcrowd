from collections import defaultdict
from dataclasses import dataclass, field
from typing import List

from modules.aggregation.aggregators.field_result import FieldResult


@dataclass
class ItemResult:
    """
    Stores information about aggregated answers for all field for one item
    """

    item_id: int
    annotations_count: int
    answers: List[FieldResult] = field(default_factory=lambda: defaultdict(list))

    def add_answer(self, field_name: str, field_result: FieldResult):
        self.answers[field_name].append(field_result)

    def to_json(self):
        """
        Serialize object to json format.
        """
        return {
            "item_id": self.item_id,
            "annotations_count": self.annotations_count,
            "answers": {
                field_name: [
                    answer.to_json()
                    for answer in self.answers[field_name]
                ]
                for field_name in self.answers
            }
        }

    @staticmethod
    def from_json(data):
        """
        Deserialize object from json format.
        """
        item_result = ItemResult(
            item_id=data["item_id"],
            annotations_count=data["annotations_count"]
        )
        for field_name, answers_data in data["answers"].items():
            for answer_data in answers_data:
                item_result.add_answer(field_name, FieldResult.from_json(answer_data))

        return item_result
