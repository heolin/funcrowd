from modules.feedback.models.utils.ner import get_tags_table
from .base import FeedbackScore


class NERReferenceScore(FeedbackScore):

    def score(self, annotation):
        item = annotation.item
        reference = item.annotations.filter(user=None).first()

        if reference:
            df = get_tags_table(annotation, reference, self.field)
            score = df['is_correct'].sum() / df['reference'].notnull().sum()
            return score
        return None
