from tasks.consts import FINISHED, VERIFICATION
from .base import BaseStrategyLogic
from modules.order_strategy.exceptions import ActionNotSupported


class DepthFirstStrategyLogic(BaseStrategyLogic):

    def next(self):
        items = self.available().order_by(
            "annotations_done", "order", "id")
        return items.first()

    def prev(self):
        raise ActionNotSupported("Action 'prev' is not supported for this DepthFirstStrategyLogic")
