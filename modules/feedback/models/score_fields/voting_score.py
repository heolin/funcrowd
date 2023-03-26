from .base import FeedbackScore
from modules.feedback.models.utils.voting import get_votings, filter_values
from tasks.field_types import LIST
import numpy as np


class VotingScore(FeedbackScore):
    def __init__(self, field: str, aggregate_others: bool = False):
        super().__init__(field)
        self.aggregate_others = aggregate_others

    def score(self, annotation):
        item = annotation.item
        field = item.template.fields.get(name=self.field)
        if other_annotations := item.annotations.exclude(user=None):
            df_probs = get_votings(other_annotations, field, self.aggregate_others)
            if field.type == LIST:
                scores = [df_probs.get(value, 0.0) for value in annotation.data[self.field]]
                return np.average(scores)
            else:
                value = annotation.data[self.field]
                if field.data_source:
                    values = item.data[field.data_source.name]
                    if self.aggregate_others:
                        value = filter_values(value, values)
                return df_probs.get(value, 0.0)
        return None
