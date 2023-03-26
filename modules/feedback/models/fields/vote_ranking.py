from .base import FeedbackField
from modules.feedback.models.utils.voting import get_votings


class VoteRanking(FeedbackField):
    def __init__(self, field: str, aggregate_others: bool = False):
        super().__init__(field)
        self.aggregate_others = aggregate_others

    def evaluate(self, annotation):
        item = annotation.item
        field = item.template.fields.get(name=self.field)
        if other_annotations := item.annotations.exclude(user=None):
            df_probs = get_votings(other_annotations, field, self.aggregate_others)
            return df_probs.to_dict()
        return None
