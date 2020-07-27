import pytest
import json
import time
from django.test import Client

from tasks.models import Item


@pytest.mark.django_db
def test_package_view(packages_with_items, user1):
    mp = packages_with_items
    package = mp.packages.first()

    client = Client()
    client.force_login(user1)

    # package exist
    response = client.get('/api/v1/packages/{0}/'.format(package.id))

    assert response.status_code == 200
    assert response.data['order'] == package.order

    # package does not exist
    response = client.get('/api/v1/packages/{0}/'.format(1000))

    assert response.status_code == 404
    assert str(response.data['detail']) == 'No Package found for given id.'


@pytest.mark.django_db
def test_package_next_item(packages_with_items, user1):
    mp = packages_with_items
    package = mp.packages.first()

    client = Client()
    client.force_login(user1)

    # get first item
    response = client.get('/api/v1/packages/{0}/items/next/'.format(package.id))
    assert response.status_code == 200
    assert response.data is not None

    # wait
    time.sleep(1)

    # annotate_item
    item_id = response.data['id']
    response = client.post(
        '/api/v1/items/{0}/annotation/'.format(item_id),
        {
            'data': json.dumps({'input_field': '1'}),
        }
    )
    assert response.status_code == 200
    assert response.data['is_verified']

    # verify annotation time
    item = Item.objects.get(id=item_id)
    annotation, _ = item.get_or_create_annotation(user1)
    annotation_time = annotation.updated - annotation.created
    assert annotation_time.total_seconds() > 1
    assert annotation.annotated
