from typing import List
from abc import ABC


class FieldResult(ABC):
    """
    Abstract class providing shared interfaces for all field results.
    """
    def __init__(self, answer: object, probability: object, support: object):
        self.answer = answer
        self.probability = probability
        self.support = support

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


class ValueFieldResult(FieldResult):
    """
    Stores information about aggregated answer for field with a single value.
    """
    def __init__(self, answer: object, probability: float, support: int):
        super().__init__(answer, probability, support)


class ListFieldResult(FieldResult):
    """
    Stores information about aggregated answer for list field.
    It contains a list of final answers, their probabilities and supports.
    """

    def __init__(self, answers: List[object], probabilities: List[float], supports: List[int]):
        super().__init__(answers, probabilities, supports)
