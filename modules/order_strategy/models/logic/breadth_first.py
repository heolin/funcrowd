from .base import BaseStrategyLogic
from django.db.models import Count


class BreadthFirstStrategyLogic(BaseStrategyLogic):

    def next(self):
        items = self.items
        if not self.task.multiple_annotations:
            items = self.items.exclude(annotations__user=self.user)
        items = items.annotate(annotations_done=Count("annotations"))

        if self.max_annotations:
            items = items.filter(annotations_done__lte=self.task.max_annotations)
        items = items.order_by("annotations_done")
        return items.first()

    def prev(self):
        # not supported, add exception
        pass
