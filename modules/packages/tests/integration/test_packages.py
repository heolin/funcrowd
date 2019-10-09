import pytest, json
from rest_framework.test import APIRequestFactory

from tasks.models import Mission
from tasks.api.views.annotation import AnnotationDetail
from modules.packages.api.views.package import NextPackage
from modules.order_strategy.models.strategy import Strategy


@pytest.mark.django_db
def test_setup_tasks(setup_task_with_items, setup_user):
    mission = Mission.objects.first()
    mp = mission.packages
    mp.strategy = Strategy.objects.get(name="DepthFirstStrategyLogic")
    mp.save()

    factory = APIRequestFactory()

    # get annotation
    request = factory.get('/api/v1/missions/{0}/next_package'.format(mission.id))
    request.user = setup_user
    view = NextPackage.as_view()

    response = view(request, mission.id)
    assert response.status_code == 200
    assert len(response.data['items']) == 2
    assert response.data['order'] == 1

    items = response.data['items']
    for item in items:
        payload = {'data': json.dumps({'output': '1'})}
        request = factory.post('/api/v1/items/{0}/annotation'.format(item['id']), payload)
        request.user = setup_user
        view = AnnotationDetail.as_view()
        response = view(request, item['id'])
        assert response.status_code == 200
        assert response.data["is_verified"] is True

    view = NextPackage.as_view()
    request = factory.get('/api/v1/missions/{0}/next_package'.format(mission.id))
    request.user = setup_user
    response = view(request, mission.id)
    assert response.status_code == 200
    assert len(response.data['items']) == 2
    assert response.data['order'] == 2

    view = NextPackage.as_view()
    request = factory.get('/api/v1/missions/{0}/next_package'.format(mission.id))
    request.user = setup_user
    response = view(request, mission.id)
    assert response.status_code == 200
    assert len(response.data['items']) == 2
    assert response.data['order'] == 2
