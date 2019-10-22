from django.urls import path

from modules.ranking.api.views.ranking import (
    AnnotationsRankingTop, AnnotationsRankingAround, ExpRankingTop, ExpRankingAround
)

urlpatterns = [
    path('ranking/annotations/top', AnnotationsRankingTop.as_view(), name='annotations_ranking_top'),
    path('ranking/annotations/around/<int:user_id>', AnnotationsRankingAround.as_view(), name='annotations_ranking_around'),
    path('ranking/exp/top', ExpRankingTop.as_view(), name='exp_ranking_top'),
    path('ranking/exp/around/<int:user_id>', ExpRankingAround.as_view(), name='exp_ranking_around'),
]