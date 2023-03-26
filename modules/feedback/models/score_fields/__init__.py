from .base import FeedbackScore
from .reference_score import ReferenceScore
from .voting_score import VotingScore
from .regression_reference_score import RegressionReferenceScore
from .ner_reference_score import NERReferenceScore
from .voting_score_other import VotingScoreOther


SCORE_FIELDS = {cls.__name__: cls for cls in FeedbackScore.__subclasses__()}
