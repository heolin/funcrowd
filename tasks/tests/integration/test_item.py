import pytest
from rest_framework.test import APIRequestFactory, force_authenticate
from tasks.api.views.item import (
    TaskNextItem, TaskNextItemWithPrevious
)
from tasks.models import Task


@pytest.mark.django_db
def test_next_item(setup_task_with_items, setup_user):
    factory = APIRequestFactory()

    task = Task.objects.first()
    item = task.items.first()

    request = factory.get('/api/v1/tasks/{0}/next_item'.format(task.id))
    force_authenticate(request, setup_user)
    view = TaskNextItem.as_view()
    response = view(request, task.id)
    assert response.status_code == 200

    assert response.data['id'] == item.id
    assert response.data['task'] == task.id
    assert response.data['exp'] == item.exp
    assert response.data['data'] == {'first': 1, 'second': 2}
    assert response.data['template']['id'] == item.template.id

    # task not found
    request = factory.get('/api/v1/tasks/{0}/next_item'.format(100))
    force_authenticate(request, setup_user)
    view = TaskNextItem.as_view()
    response = view(request, 100)
    assert response.status_code == 404
    assert response.data["detail"].code == "not_found"


@pytest.mark.django_db
def test_next_item_with_previous(setup_task_with_items, setup_user):
    factory = APIRequestFactory()

    task = Task.objects.first()
    item = task.items.first()

    # next item with previous given
    request = factory.get('/api/v1/items/{0}/next_item'.format(item.id))
    request.user = setup_user
    force_authenticate(request, setup_user)
    next_item = item.task.next_item(request.user, item)

    view = TaskNextItemWithPrevious.as_view()
    response = view(request, item.id)
    assert response.status_code == 200

    assert response.data['id'] == next_item.id
    assert response.data['task'] == task.id
    assert response.data['data'] == {'first': 2, 'second': 2}
    assert response.data['template']['id'] == item.template.id

    # no next item
    request = factory.get('/api/v1/items/{0}/next_item'.format(next_item.id))
    force_authenticate(request, setup_user)

    view = TaskNextItemWithPrevious.as_view()
    response = view(request, next_item.id)
    assert response.status_code == 204
    assert response.data is None

    # item not found
    request = factory.get('/api/v1/items/{0}/next_item'.format(100))
    force_authenticate(request, setup_user)
    view = TaskNextItemWithPrevious.as_view()
    response = view(request, 100)
    assert response.status_code == 404
    assert response.data["detail"].code == "not_found"
