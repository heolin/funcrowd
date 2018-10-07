from .base import BaseStrategyLogic


class StaticStrategyLogic(BaseStrategyLogic):

    def next(self):
        if self.item:
            return self.task.items.filter(order__gt=self.item.order).first()
        else:
            return self.task.items.first()

    def prev(self):
        return self.task.items.filter(order__lt=self.item.order).last()
