import pytest

from modules.ranking.models import ExpRanking, AnnotationsRanking
from users.models import EndWorker


@pytest.mark.django_db
def test_exp_ranking_top(users):
    ranking = ExpRanking()

    results = ranking.top()
    assert len(results) == 4
    assert results[0]['value'] > results[1]['value']
    assert results[1]['value'] > results[2]['value']
    assert results[2]['value'] > results[3]['value']
    assert results[0]['row_number'] == 1
    assert results[0]['username'] == 'user4'

    results = ranking.top(2)
    assert len(results) == 2

    results = ranking.top(2)
    assert results[0]['username'] == 'user4'

    results = ranking.top(2, 1)
    assert results[0]['username'] == 'user2'


@pytest.mark.django_db
def test_exp_ranking_around(users):
    ranking = ExpRanking()

    user = EndWorker.objects.get(username='user2')
    results = ranking.around(user.id, 1)
    assert len(results) == 3
    assert results[0]['username'] == 'user3'
    assert results[1]['username'] == 'user2'
    assert results[2]['username'] == 'user1'

    user = EndWorker.objects.get(username='user4')
    results = ranking.around(user.id, 1)
    assert len(results) == 2


@pytest.mark.django_db
def test_annotations_count_ranking_top(task_annotations):
    ranking = AnnotationsRanking()

    results = ranking.top()
    assert len(results) == 4
    assert results[0]['value'] == 3
    assert results[1]['value'] == 2
    assert results[2]['value'] == 1
    assert results[3]['value'] == 0
    assert results[0]['username'] == 'user4'
    assert results[0]['row_number'] == 1

    results = ranking.top(2)
    assert len(results) == 2

    results = ranking.top(2)
    assert results[0]['username'] == 'user4'

    results = ranking.top(2, 1)
    assert results[0]['username'] == 'user2'


@pytest.mark.django_db
def test_annotations_count_ranking_around(task_annotations):
    ranking = AnnotationsRanking()

    user2 = EndWorker.objects.get(username='user2')
    results = ranking.around(user2.id, 1)
    assert len(results) == 3
    assert results[0]['username'] == 'user3'
    assert results[1]['username'] == 'user2'
    assert results[2]['username'] == 'user1'

    user4 = EndWorker.objects.get(username='user4')
    results = ranking.around(user4.id, 1)
    assert len(results) == 2
