from abc import ABCMeta, abstractmethod


class IStrategyClient:
    __metaclass__ = ABCMeta

    @abstractmethod
    def next_item(self, user, item):
        raise NotImplemented

    @abstractmethod
    def prev_item(self, user, item):
        raise NotImplemented

    @abstractmethod
    def exclude_items_with_user_annotations(self, items, user):
        raise NotImplemented

    @abstractmethod
    def annotate_annotations_done(self, items):
        raise NotImplemented

    @abstractmethod
    def exclude_max_annotations(self, items):
        raise NotImplemented
