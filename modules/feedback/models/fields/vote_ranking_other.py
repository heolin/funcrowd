from . import VoteRanking
from .base import FeedbackField
from modules.feedback.models.utils.voting import get_votings


class VoteRankingOther(VoteRanking):

    def __init__(self, field: str):
        super().__init__(field, True)
