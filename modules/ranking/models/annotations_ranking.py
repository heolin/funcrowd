from modules.ranking.models.ranking import Ranking
from modules.ranking.query import ANNOTATIONS_COUNT_RANKING_BASE_QUERY


class AnnotationsRanking(Ranking):
    BASE_QUERY = ANNOTATIONS_COUNT_RANKING_BASE_QUERY
