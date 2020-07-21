FIELDS = {}

from .base import FeedbackField
from .vote_ranking import VoteRanking
from .annotations_count import AnnotationsCount
from .reference_value import ReferenceValue
from .ner_reference_value import NERReferenceValue


for cls in FeedbackField.__subclasses__():
    FIELDS[cls.__name__] = cls
