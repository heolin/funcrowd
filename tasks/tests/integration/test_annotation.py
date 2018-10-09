import pytest
from rest_framework.test import APIRequestFactory

from tasks.api.serializers.dto.annotation_response import AnnotationResponseSerializer
from tasks.models.dto.annotation_response import AnnotationResponse
from tasks.models import (
    Task, Item, Annotation
)

from tasks.api.views.annotation import AnnotationDetail


@pytest.mark.django_db
def test_annotation(setup_task_with_items, setup_user, setup_other_user):
    factory = APIRequestFactory()

    task = Task.objects.first()
    item = task.items.first()

    request = factory.get('/api/v1/items/{0}/annotation'.format(item.id))
    request.user = setup_user
    view = AnnotationDetail.as_view()
    response = view(request, task.id)
    assert response.status_code == 200
    assert response.data == {
        'item_id': item.id,
        'data': {'output': '', 'optional': ''},
        'is_done': False,
        'is_skipped': False
     }
