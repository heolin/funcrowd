from .base import FeedbackField
import pandas as pd


class AnnotationsCount(FeedbackField):

    def evaluate(self, annotation):
        item = annotation.item
        other_annotations = item.annotations.exclude(user=None).exclude(user=annotation.user)
        if other_annotations:
            return other_annotations.count()
        return None
