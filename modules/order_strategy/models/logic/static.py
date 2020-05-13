from .base import BaseStrategyLogic


class StaticStrategyLogic(BaseStrategyLogic):

    def next(self):
        items = self.task.items
        if not self.task.multiple_annotations:
            items = self.task.exclude_items_with_user_annotations(items, self.user)

        if self.item:
            return items.filter(order__gt=self.item.order).first()
        else:
            return items.first()

    def prev(self):
        return self.task.items.filter(order__lt=self.item.order).last()
