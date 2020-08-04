import pytest
from django.test import Client

from modules.achievements.tests.conftest import compare_without_fields
from users.models import EndWorker


@pytest.mark.django_db
def test_ranking_top_view(task_annotations):
    client = Client()

    # test basic top ranking
    response = client.get('/api/v1/ranking/mp/1/top/')

    expected_data = [
        {
            'username': 'user1',
            'annotated_documents': 0,
            'high_agreement_percentage': 0,
            'bonus_exp': 0,
            'value': 0.0,
            'row_number': 1
        },
        {
            'username': 'user2',
            'annotated_documents': 1,
            'high_agreement_percentage': 0,
            'bonus_exp': 0,
            'value': 0.0,
            'row_number': 2
        },
        {
            'username': 'user3',
            'annotated_documents': 1,
            'high_agreement_percentage': 0,
            'bonus_exp': 0,
            'value': 0.0,
            'row_number': 3
        },
        {
            'username': 'user4',
            'annotated_documents': 2,
            'high_agreement_percentage': 0,
            'bonus_exp': 0,
            'value': 0.0,
            'row_number': 4
        },
    ]

    assert len(response.data.keys()) == 2
    assert response.data['mission_id'] == 1
    assert len(response.data['rows']) == 4
    for received, expected in zip(response.data['rows'], expected_data):
        assert compare_without_fields(received, expected, ['user_id'])


@pytest.mark.django_db
def test_ranking_around_view(task_annotations):
    user2 = EndWorker.objects.get(username="user2")

    client = Client()
    client.force_login(user2)

    # test basic around ranking
    response = client.get('/api/v1/ranking/mp/1/around/{0}/'.format(user2.id))
    assert len(response.data.keys()) == 2
    assert response.data['mission_id'] == 1
    assert len(response.data['rows']) == 3


@pytest.mark.django_db
def test_mission_ranking_around_list(two_missions_annotations):
    user2 = EndWorker.objects.get(username="user2")

    client = Client()
    client.force_login(user2)

    # get results for both missions
    response = client.get('/api/v1/ranking/mp/all/around/{0}/'.format(user2.id))
    assert len(response.data) == 2
    assert response.data[0]['mission_id'] == 1
    assert len(response.data[0]['rows']) == 1
    assert response.data[1]['mission_id'] == 2

    # get results for list_size=1
    response = client.get('/api/v1/ranking/mp/all/around/{0}/?list_size=1'.format(user2.id))
    assert len(response.data) == 1
    assert response.data[0]['mission_id'] == 1

    response = client.get('/api/v1/ranking/mp/all/around/{0}/?list_size=1&list_page=1'.format(user2.id))
    assert response.data[0]['mission_id'] == 1

    response = client.get('/api/v1/ranking/mp/all/around/{0}/?list_size=1&list_page=2'.format(user2.id))
    assert response.data[0]['mission_id'] == 2
