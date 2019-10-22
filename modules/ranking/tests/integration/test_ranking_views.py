import pytest
from rest_framework.test import APIRequestFactory, force_authenticate

from modules.achievements.tests.conftest import compare_without_fields
from modules.ranking.api.views.ranking import AnnotationsRankingTop, AnnotationsRankingAround
from users.models import EndWorker


@pytest.mark.django_db
def test_ranking_top_view(setup_task_annotations):
    factory = APIRequestFactory()

    user = EndWorker.objects.get(username="user4")

    # test basic top ranking
    request = factory.get('/api/v1/ranking/annotations/top')
    force_authenticate(request, user)
    view = AnnotationsRankingTop.as_view()
    response = view(request)

    expected_data = [
        {
            'username': 'user4',
            'value': 3.0,
            'row_number': 1
        },
        {
            'username': 'user3',
            'value': 2.0,
            'row_number': 2
        },
        {
            'username': 'user2',
            'value': 1.0,
            'row_number': 3
        },
        {
            'username': 'user1',
            'value': 0.0,
            'row_number': 4
        },
    ]
    assert len(response.data) == 4
    for received, expected in zip(response.data, expected_data):
        assert compare_without_fields(received, expected, ['user_id'])

    # test using get parameters
    request = factory.get('/api/v1/ranking/annotations/top?size=2&page=1')
    force_authenticate(request, user)
    view = AnnotationsRankingTop.as_view()
    response = view(request)

    expected_data = [
        {
            'username': 'user2',
            'value': 1.0,
            'row_number': 3
        },
        {
            'username': 'user1',
            'value': 0.0,
            'row_number': 4
        },
    ]
    assert len(response.data) == 2
    for received, expected in zip(response.data, expected_data):
        assert compare_without_fields(received, expected, ['user_id'])


@pytest.mark.django_db
def test_ranking_around_view(setup_task_annotations):
    factory = APIRequestFactory()

    user = EndWorker.objects.get(username="user2")

    # test basic around ranking
    request = factory.get('/api/v1/ranking/annotations/around/{0}'.format(user.id))
    force_authenticate(request, user)
    view = AnnotationsRankingAround.as_view()
    response = view(request, user.id)
    assert len(response.data) == 4

    # test basic around ranking with get params
    request = factory.get('/api/v1/ranking/annotations/around/{0}?size=1'.format(user.id))
    force_authenticate(request, user)
    view = AnnotationsRankingAround.as_view()
    response = view(request, user.id)

    expected_data = [
        {
            'username': 'user3',
            'value': 2.0,
            'row_number': 2
        },
        {
            'username': 'user2',
            'value': 1.0,
            'row_number': 3
        },
        {
            'username': 'user1',
            'value': 0.0,
            'row_number': 4
        },
    ]
    assert len(response.data) == 3
    for received, expected in zip(response.data, expected_data):
        assert compare_without_fields(received, expected, ['user_id'])
