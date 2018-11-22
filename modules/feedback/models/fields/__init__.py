FIELDS = {}

from .base import FeedbackField
from .vote_ranking import VoteRanking
from .annotations_count import AnnotationsCount


for cls in FeedbackField.__subclasses__():
    FIELDS[cls.__name__] = cls
