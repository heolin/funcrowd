from .base import BaseStrategyLogic


class StaticStrategyLogic(BaseStrategyLogic):

    def next(self):
            return self.items.filter(order__gt=self.item.order).first()

    def prev(self):
        return self.items.filter(order__lt=self.item.order).last()
