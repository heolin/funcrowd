SCORE_FIELDS = {}

from .base import FeedbackScore
from .reference_score import ReferenceScore
from .voting_score import VotingScore


for cls in FeedbackScore.__subclasses__():
    SCORE_FIELDS[cls.__name__] = cls
