from .base import BaseStrategyLogic
from modules.order_strategy.exceptions import ActionNotSupported


class RandomStrategyLogic(BaseStrategyLogic):

    def next(self):
        items = self.task.items
        if not self.task.multiple_annotations:
            items = self.task.exclude_items_with_user_annotations(self.user)
        items = self.task.annotate_annotations_done(items)

        if self.task.max_annotations:
            items = self.task.exclude_max_annotations(items)
        items = items.order_by("?")
        return items.first()

    def prev(self):
        raise ActionNotSupported("Action 'prev' is not supported for this RandomStrategyLogic")

