from abc import ABC, abstractmethod


class BaseAchievementLogic(ABC):
    def __init__(self, user):
        self.user

    @abstractmethod
    def _logic(self, df):
        return []


# EVENT MANAGER
# register i te tematy
