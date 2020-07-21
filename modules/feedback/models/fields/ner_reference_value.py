from modules.feedback.models.utils.ner import get_tags_table
from .base import FeedbackField


class NERReferenceValue(FeedbackField):

    def evaluate(self, annotation):
        item = annotation.item
        reference = item.annotations.filter(user=None).first()

        if reference:
            df = get_tags_table(annotation, reference, self.field)
            return df.to_dict(orient='rows')

        return None
