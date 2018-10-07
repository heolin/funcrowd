from .base import BaseStrategyLogic
from django.db.models import Count
from modules.order_strategy.exceptions import ActionNotSupported


class RandomStrategyLogic(BaseStrategyLogic):

    def next(self):
        items = self.task.items
        if not self.task.multiple_annotations:
            items = self.task.items.exclude(annotations__user=self.user)
        items = items.annotate(annotations_done=Count("annotations"))
        if self.task.max_annotations:
            items = items.filter(annotations_done__lt=self.task.max_annotations)
        items = items.order_by("?")
        return items.first()

    def prev(self):
        raise ActionNotSupported("Action 'prev' is not supported for this RandomStrategyLogic")

