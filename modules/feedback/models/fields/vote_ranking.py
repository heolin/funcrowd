from .base import FeedbackField
from modules.feedback.models.utils.voting import get_votings


class VoteRanking(FeedbackField):

    def evaluate(self, annotation):
        item = annotation.item
        field = item.template.fields.get(name=self.field)
        other_annotations = item.annotations.exclude(user=None)  # .exclude(user=annotation.user)
        if other_annotations:
            df_probs = get_votings(other_annotations, field)
            scores = df_probs.to_dict()
            return scores
        return None
