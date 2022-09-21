from dataclasses import dataclass
from typing import Text


@dataclass
class FieldResult:
    """
    Stores information about aggregated answer for field with a single value.
    """

    answer: Text
    probability: float
    support: int

    def to_json(self):
        """
        Serialize object to json format.
        """
        return {
            "answer": self.answer,
            "probability": self.probability,
            "support": self.support
        }

    @staticmethod
    def from_json(data):
        """
        Deserialize object from json format.
        """
        return FieldResult(
            data['answer'],
            data['probability'],
            data['support']
        )
