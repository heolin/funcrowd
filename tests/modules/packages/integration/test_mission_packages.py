import json
import pytest
from django.test import Client

from modules.order_strategy.models.strategy import Strategy


@pytest.mark.django_db
def test_next_package(packages_with_items, user1):
    mp = packages_with_items
    mp.strategy = Strategy.objects.get(name="DepthFirstStrategyLogic")
    mp.save()

    client = Client()
    client.force_login(user1)

    # get annotation
    response = client.get('/api/v1/missions/{0}/next_package/'.format(mp.mission_id))
    assert response.status_code == 200
    assert len(response.data['items']) == 2
    assert response.data['order'] == 1

    items = response.data['items']
    for item in items:
        payload = {'data': json.dumps({'input_field': '0'})}
        response = client.post('/api/v1/items/{0}/annotation/'.format(item['id']), payload)
        assert response.status_code == 200
        assert response.data["is_verified"] is True

    response = client.get('/api/v1/missions/{0}/next_package/'.format(mp.mission_id))
    assert response.status_code == 200
    assert len(response.data['items']) == 2
    assert response.data['order'] == 2

    response = client.get('/api/v1/missions/{0}/next_package/'.format(mp.mission_id))
    assert response.status_code == 200
    assert len(response.data['items']) == 2
    assert response.data['order'] == 2


@pytest.mark.django_db
def test_next_package_with_search(packages_with_metadata, user1):
    mp = packages_with_metadata
    mp.max_annotations = 1
    mp.strategy = Strategy.objects.get(name="DepthFirstStrategyLogic")
    mp.save()

    client = Client()
    client.force_login(user1)

    # with one filter
    response = client.get(
        '/api/v1/missions/{0}/next_package/?search=country:Country2'.format(mp.mission_id))
    assert response.data['order'] == 3

    response = client.get(
        '/api/v1/missions/{0}/next_package/?search=country:Country3'.format(mp.mission_id))
    assert response.data['order'] == 5

    # with two filters
    response = client.get(
        '/api/v1/missions/{0}/next_package/?search=country:Country2,city:City4'.format(mp.mission_id))
    assert response.data['order'] == 4


@pytest.mark.django_db
def test_create_package(packages_with_unassigned_items, user1):
    mp = packages_with_unassigned_items

    client = Client()
    client.force_login(user1)

    # no size params passed
    response = client.post(
        '/api/v1/missions/{0}/create_package/'.format(mp.mission_id),
        {}
    )
    assert response.status_code == 400
    assert str(response.data[0]) == "Field 'size' not provided"

    # size params too large
    response = client.post(
        '/api/v1/missions/{0}/create_package/'.format(mp.mission_id),
        {"size": 100}
    )
    assert response.status_code == 400
    assert response.data['detail'].code == 'insufficient_unassigned_items'

    # size param passed
    response = client.post(
        '/api/v1/missions/{0}/create_package/'.format(mp.mission_id),
        {"size": 1}
    )
    assert response.status_code == 200
    assert response.data['order'] == 0

    # size and metadata params passed
    response = client.post(
        '/api/v1/missions/{0}/create_package/'.format(mp.mission_id),
        {"size": 1, "metadata": {"number": 1}}
    )
    assert response.status_code == 200
    assert response.data['order'] == 1
