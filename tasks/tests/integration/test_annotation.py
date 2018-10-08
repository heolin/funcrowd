import pytest
from rest_framework.test import APIRequestFactory

from tasks.api.serializers.dto.annotation_response import AnnotationResponseSerializer
from tasks.models.dto.annotation_response import AnnotationResponse
from tasks.models import (
    Task, Item, Annotation
)



@pytest.mark.django_db
def test_annotation(setup_task_with_items, setup_user, setup_other_user):
    factory = APIRequestFactory()


