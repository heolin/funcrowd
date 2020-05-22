from modules.aggregation.aggregators.field_result import FieldResult


class ItemResult:
    """
    Stores information about aggregated answers for all field for one item
    """

    def __init__(self, item_id: int, annotations_count: int):
        self.item_id = item_id
        self.annotations_count = annotations_count
        self.answers = {}

    def add_answer(self, field_name: str, field_result: FieldResult):
        self.answers[field_name] = field_result

    def to_json(self):
        """
        Serialize object to json format.
        """
        return {
            "item_id": self.item_id,
            "annotations_count": self.annotations_count,
            "answers": {
                field_name: self.answers[field_name].to_json()
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
        for field_name, answer_data in data["answers"].items():
            item_result.add_answer(field_name, FieldResult.from_json(answer_data))

        return item_result
