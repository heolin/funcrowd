import pytest
from django.test import Client

from modules.achievements.tests.conftest import compare_without_fields
from users.models import EndWorker


@pytest.mark.django_db
def test_ranking_top_view(task_annotations):
    client = Client()

    # test basic top ranking
    response = client.get('/api/v1/ranking/annotations/top/')

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
    response = client.get('/api/v1/ranking/annotations/top/?size=2&page=1')

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
def test_ranking_around_view(task_annotations):
    user2 = EndWorker.objects.get(username="user2")

    client = Client()
    client.force_login(user2)

    # test basic around ranking
    response = client.get('/api/v1/ranking/annotations/around/{0}/'.format(user2.id))
    assert len(response.data) == 4

    # test basic around ranking with get params
    response = client.get('/api/v1/ranking/annotations/around/{0}/?size=1'.format(user2.id))
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
