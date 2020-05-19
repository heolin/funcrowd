import pytest

from modules.order_strategy.models import Strategy
from tasks.models import (
    Mission, Task, Item, ItemTemplate, ItemTemplateField
)


@pytest.fixture
@pytest.mark.django_db
def annotations():
    pass
