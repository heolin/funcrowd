from modules.feedback.models.utils.ner import get_tags_table
from .base import FeedbackScore


class NERReferenceScore(FeedbackScore):

    def score(self, annotation):
        item = annotation.item
        reference = item.annotations.filter(user=None).first()

        if reference:
            df = get_tags_table(annotation, reference, self.field)
            reference_max = df['reference'].notnull().sum()
            score = 0
            if reference_max:
                score = df['is_correct'].sum() / reference_max
            return score
        return None
