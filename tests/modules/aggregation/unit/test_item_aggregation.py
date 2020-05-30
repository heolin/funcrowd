import pytest

from modules.aggregation.models import ItemAggregation


@pytest.fixture()
def item_aggregation(one_task_items_with_annotations_and_reference):
    task = one_task_items_with_annotations_and_reference
    item = task.items.first()
    return ItemAggregation(
        item=item,
        data={
            "item_id": item.id,
            "annotations_count": 5,
            "answers": {
                "value_input_field": {
                    "answer": "1a",
                    "probability": 0.4,
                    "support": 2
                },
                "list_input_field": {
                    "answer": ["1a", "2a"],
                    "probability": [0.6, 0.5],
                    "support": [3, 2]
                },
            }
        },
        type="BaseAggregator"
    )


@pytest.fixture()
def empty_item_aggregation(one_task_items_with_reference_annotation):
    task = one_task_items_with_reference_annotation
    item = task.items.first()
    return ItemAggregation(
        item=item,
        data={
            "item_id": item.id,
            "annotations_count": 0,
            "answers": {}
        },
        type="BaseAggregator"
    )


@pytest.mark.django_db
def test_item_aggregation(item_aggregation):
    """
    Check getting ItemAggregation statistics
    """
    assert item_aggregation.get_support() == 3
    assert item_aggregation.get_probability() == 0.5
    assert item_aggregation.get_annotations_count() == 5


@pytest.mark.django_db
def test_empty_item_aggregation(empty_item_aggregation):
    """
    Check getting ItemAggregation statistics from an empty object
    """
    assert empty_item_aggregation.get_support() == 0
    assert empty_item_aggregation.get_probability() == 0.
    assert empty_item_aggregation.get_annotations_count() == 0
