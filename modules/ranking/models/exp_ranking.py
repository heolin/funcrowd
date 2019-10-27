from modules.ranking.models.ranking import Ranking
from modules.ranking.query.base import EXP_RANKING_BASE_QUERY


class ExpRanking(Ranking):
    BASE_QUERY = EXP_RANKING_BASE_QUERY
