from tasks.consts import FINISHED, VERIFICATION


class BaseStrategyLogic(object):
    def __init__(self, task, user, item):
        self.task = task
        self.user = user
        self.item = item

    def available(self):
        items = self.task.items
        if not self.task.multiple_annotations:
            items = self.task.exclude_items_with_user_annotations(self.user)

        items = self.task.annotate_annotations_done(items)

        if self.task.max_annotations:
            items = self.task.exclude_max_annotations(items)

        items = items.exclude(status__in=[FINISHED, VERIFICATION])
        return items

    def next(self):
        return self.available().first()

    def prev(self):
        pass


