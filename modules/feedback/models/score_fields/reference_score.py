from .base import FeedbackScore
import pandas as pd


class ReferenceScore(FeedbackScore):

    def score(self, annotation):
        item = annotation.item
        references = item.annotations.filter(user=None)
        if references:
            ref_values = list(references.values_list("data", flat=True))
            df_references = pd.DataFrame(ref_values)
            score = int((df_references[self.field] == annotation.data[self.field]).any())
            return score
        return None
