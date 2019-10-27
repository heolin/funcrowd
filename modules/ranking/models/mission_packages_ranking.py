from modules.ranking.models.ranking import Ranking
from modules.ranking.query.base import MISSION_PACKAGE_RANKING_BASE_QUERY


class MissionPackagesRanking(Ranking):
    BASE_QUERY = MISSION_PACKAGE_RANKING_BASE_QUERY

    def __init__(self, mission_package):
        self.mission_package = mission_package

    def get_base_query(self):
        return MISSION_PACKAGE_RANKING_BASE_QUERY.format(
            self.mission_package.mission_id
        )

