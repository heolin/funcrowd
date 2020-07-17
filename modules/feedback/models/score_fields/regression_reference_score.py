from .base import FeedbackScore
import pandas as pd


class RegressionReferenceScore(FeedbackScore):

    def score(self, annotation):
        item = annotation.item
        references = item.annotations.filter(user=None)
        if references:
            ref_values = list(references.values_list("data", flat=True))
            df_references = pd.DataFrame(ref_values)
            value = float(annotation.data[self.field])
            diff = (df_references[self.field] - value).abs()
            scores = (1 - diff / df_references[self.field]).clip(0, 1)
            score = scores.max()
            return score
        return None
