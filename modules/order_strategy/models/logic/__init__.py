STRATEGY_LOGICS = {}

from .base import BaseStrategyLogic
from .static import StaticStrategyLogic
from .breadth_first import BreadthFirstStrategyLogic
from .depth_first import DepthFirstStrategyLogic
from .random import RandomStrategyLogic

for cls in BaseStrategyLogic.__subclasses__():
    STRATEGY_LOGICS[cls.__name__] = cls
