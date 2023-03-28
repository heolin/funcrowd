from .base import FeedbackField
from .vote_ranking import VoteRanking
from .annotations_count import AnnotationsCount
from .reference_value import ReferenceValue
from .ner_reference_value import NERReferenceValue
from .vote_ranking_other import VoteRankingOther
from ..utils.helpers import all_subclasses

FIELDS = {cls.__name__: cls for cls in all_subclasses(FeedbackField)}
