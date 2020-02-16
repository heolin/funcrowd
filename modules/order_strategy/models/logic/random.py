from tasks.consts import VERIFICATION, FINISHED
from .base import BaseStrategyLogic
from modules.order_strategy.exceptions import ActionNotSupported


class RandomStrategyLogic(BaseStrategyLogic):

    def next(self):
        return self.available().order_by("?").first()

    def prev(self):
        raise ActionNotSupported("Action 'prev' is not supported for this RandomStrategyLogic")

