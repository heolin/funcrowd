
class BaseStrategyLogic(object):
    def __init__(self, task, user, item):
        self.task = task
        self.user = user
        self.item = item

    def next(self):
        pass

    def prev(self):
        pass


