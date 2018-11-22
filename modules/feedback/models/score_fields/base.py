
class FeedbackScore(object):
    def __init__(self, field):
        self.field = field

    def score(self, annotation):
        raise NotImplemented
