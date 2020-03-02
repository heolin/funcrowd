from .base import FeedbackScore
import pandas as pd


class ReferenceScore(FeedbackScore):

    def score(self, annotation):
        item = annotation.item
        references = item.annotations.filter(user=None)
        if references:
            ref_values = list(references.values_list("data", flat=True))
            df_references = pd.DataFrame(ref_values)
            score = int(
                (df_references[self.field].astype(str).str.lower() ==
                 str(annotation.data[self.field]).lower()).any()
            )
            return score
        return None
