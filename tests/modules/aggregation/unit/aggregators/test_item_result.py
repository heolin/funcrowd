import pytest

from modules.aggregation.aggregators import ItemResult, FieldResult


@pytest.fixture
def item_result():
    item_result = ItemResult(
        item_id=1,
        annotations_count=5
    )
    item_result.answers = {
        "single_input_field": [
            FieldResult(1, 0.5, 2),
        ],
        "list_input_field": [
            FieldResult(1, 0.5, 2),
            FieldResult(2, 0.5, 1),
        ]
    }
    return item_result


@pytest.mark.django_db
def test_item_result_to_json(item_result):
    """
    Test serialization of ItemTemplateField with two fields
    """
    data = item_result.to_json()
    assert type(data['item_id']) is int
    assert type(data['annotations_count']) is int
    assert len(data['answers']) == 2

    assert type(data['answers']['single_input_field']) is list
    assert type(data['answers']['single_input_field'][0]['probability']) is float
    assert len(data['answers']['single_input_field']) == 1

    assert type(data['answers']['list_input_field']) is list
    assert type(data['answers']['list_input_field'][0]['probability']) is float
    assert len(data['answers']['list_input_field']) == 2
