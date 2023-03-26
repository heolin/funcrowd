from .base import FeedbackField
from .vote_ranking import VoteRanking
from .annotations_count import AnnotationsCount
from .reference_value import ReferenceValue
from .ner_reference_value import NERReferenceValue
from .vote_ranking_other import VoteRankingOther


FIELDS = {cls.__name__: cls for cls in FeedbackField.__subclasses__()}
