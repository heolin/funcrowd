from . import VotingScore
from .base import FeedbackScore
from modules.feedback.models.utils.voting import get_votings, filter_values
from tasks.field_types import LIST
import numpy as np


class VotingScoreOther(VotingScore):

    def __init__(self, field: str):
        super().__init__(field, True)
