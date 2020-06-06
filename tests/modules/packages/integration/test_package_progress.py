import pytest
from django.test import Client


@pytest.mark.django_db
def test_package_status(packages_with_annotated_items, user1, user2):
    mp = packages_with_annotated_items

    client = Client()
    client.force_login(user1)

    # first package first user
    reference_data = {
        "items_done": 2,
        "items_count": 2,
        "progress": 1.0,
        "status": "FINISHED"
    }

    package = mp.packages.all()[0]
    response = client.get('/api/v1/packages/{0}/status/'.format(package.id))
    assert response.status_code == 200
    for field, value in reference_data.items():
        assert response.data[field] == value
    assert response.data['reward'] is not None

    # third package first user
    reference_data = {
        "items_done": 1,
        "items_count": 2,
        "progress": 0.5,
        "status": "IN_PROGRESS"
    }

    package = mp.packages.all()[2]
    response = client.get('/api/v1/packages/{0}/status/'.format(package.id))
    for field, value in reference_data.items():
        assert response.data[field] == value
    assert response.data['reward'] is None

    # third package second user
    client.force_login(user2)

    reference_data = {
        "items_done": 0,
        "items_count": 2,
        "progress": 0.0,
        "status": "NONE"
    }

    package = mp.packages.all()[2]
    response = client.get('/api/v1/packages/{0}/status/'.format(package.id))
    for field, value in reference_data.items():
        assert response.data[field] == value
    assert response.data['reward'] is None


@pytest.mark.django_db
def test_packages_status(packages_with_annotated_items, user1, user2):
    mp = packages_with_annotated_items

    client = Client()

    # first user
    client.force_login(user1)
    response = client.get('/api/v1/packages/status/')
    assert len(response.data) == 3
    assert response.status_code == 200

    # second user
    client.force_login(user2)
    response = client.get('/api/v1/packages/status/')
    assert len(response.data) == 1
    assert response.status_code == 200
