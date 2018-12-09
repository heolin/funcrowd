import pandas as pd
from .base import FeedbackField


class ReferenceValue(FeedbackField):

    def evaluate(self, annotation):
        item = annotation.item
        references = item.annotations.filter(user=None)
        if references:
            ref_values = list(references.values_list("data", flat=True))
            df_references = pd.DataFrame(ref_values)
            return list(df_references[self.field])
        return None
