from abc import ABC
from django.db import connection

from modules.ranking.models.utils import dictfetchall
from modules.ranking.query import (
    RANKING_PAGINATION_QUERY, RANKING_NEIGHBOURHOOD_QUERY
)


class Ranking(ABC):
    BASE_QUERY = None

    def top(self, size=10, page=0):
        query = RANKING_PAGINATION_QUERY.format(
            self.BASE_QUERY, size, page * size)

        cursor = connection.cursor()
        cursor.execute(query)
        return dictfetchall(cursor)

    def around(self, user_id, size=2):
        query = RANKING_NEIGHBOURHOOD_QUERY.format(
            self.BASE_QUERY, user_id, size
        )

        cursor = connection.cursor()
        cursor.execute(query)
        return dictfetchall(cursor)
