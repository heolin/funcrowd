
class FieldResult:
    """
    Stores information about aggregated answer for field with a single value.
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
