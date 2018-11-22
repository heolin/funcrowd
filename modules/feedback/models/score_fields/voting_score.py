from .base import FeedbackScore
import pandas as pd


class VotingScore(FeedbackScore):

    def score(self, annotation):
        item = annotation.item
        other_annotations = item.annotations.exclude(user=None).exclude(user=annotation.user)
        if other_annotations:
            other_values = other_annotations.values_list("data", flat=True)
            df_other = pd.DataFrame(list(other_values))
            df_probs = df_other[self.field].value_counts() / len(df_other)
            score = df_probs.get(annotation.data[self.field], 0.0)
            return score
        return None
