import pytest
from django.test import Client

from tasks.models import Task


@pytest.mark.django_db
def test_next_item(task_with_items, user1):
    task = Task.objects.first()
    item = task.items.first()

    client = Client()
    client.force_login(user1)

    response = client.get('/api/v1/tasks/{0}/next_item'.format(task.id))
    assert response.status_code == 200

    assert response.data['id'] == item.id
    assert response.data['task'] == task.id
    assert response.data['exp'] == item.exp
    assert response.data['data'] == {'first': 1, 'second': 2}
    assert response.data['template']['id'] == item.template.id

    # task not found
    response = client.get('/api/v1/tasks/{0}/next_item'.format(100))
    assert response.status_code == 404
    assert response.data["detail"].code == "not_found"


@pytest.mark.django_db
def test_next_item_with_previous(task_with_items, user1):
    task = Task.objects.first()
    item = task.items.first()

    client = Client()
    client.force_login(user1)

    # next item with previous given
    next_item = item.task.next_item(user1, item)
    response = client.get('/api/v1/items/{0}/next_item'.format(item.id))
    assert response.status_code == 200

    assert response.data['id'] == next_item.id
    assert response.data['task'] == task.id
    assert response.data['data'] == {'first': 2, 'second': 2}
    assert response.data['template']['id'] == item.template.id

    # no next item
    last_item = task.items.all()[3]
    response = client.get('/api/v1/items/{0}/next_item'.format(last_item.id))
    assert response.status_code == 204
    assert response.data is None

    # item not found
    response = client.get('/api/v1/items/{0}/next_item'.format(100))
    assert response.status_code == 404
    assert response.data["detail"].code == "not_found"
