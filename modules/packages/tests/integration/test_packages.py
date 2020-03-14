import pytest, json
from django.test import Client

from tasks.models import Mission
from modules.order_strategy.models.strategy import Strategy


@pytest.mark.django_db
def test_tasks(task_with_items, user1):
    mission = Mission.objects.first()
    mp = mission.packages
    mp.strategy = Strategy.objects.get(name="DepthFirstStrategyLogic")
    mp.save()

    client = Client()
    client.force_login(user1)

    # get annotation
    response = client.get('/api/v1/missions/{0}/next_package/'.format(mission.id))
    assert response.status_code == 200
    assert len(response.data['items']) == 2
    assert response.data['order'] == 1

    items = response.data['items']
    for item in items:
        payload = {'data': json.dumps({'output': '1'})}
        response = client.post('/api/v1/items/{0}/annotation/'.format(item['id']), payload)
        assert response.status_code == 200
        assert response.data["is_verified"] is True

    response = client.get('/api/v1/missions/{0}/next_package/'.format(mission.id))
    assert response.status_code == 200
    assert len(response.data['items']) == 2
    assert response.data['order'] == 2

    response = client.get('/api/v1/missions/{0}/next_package/'.format(mission.id))
    assert response.status_code == 200
    assert len(response.data['items']) == 2
    assert response.data['order'] == 2


@pytest.mark.django_db
def test_tasks(packages_with_metadata, user1):
    mission = Mission.objects.first()
    mp = mission.packages
    mp.max_annotations = 1
    mp.strategy = Strategy.objects.get(name="DepthFirstStrategyLogic")
    mp.save()

    client = Client()
    client.force_login(user1)

    # with one filter
    response = client.get('/api/v1/missions/{0}/next_package/?search=country:Country2'.format(mission.id))
    assert response.data['order'] == 3

    response = client.get('/api/v1/missions/{0}/next_package/?search=country:Country3'.format(mission.id))
    assert response.data['order'] == 5

    # with two filters
    response = client.get('/api/v1/missions/{0}/next_package/?search=country:Country2,city:City4'.format(mission.id))
    assert response.data['order'] == 4
