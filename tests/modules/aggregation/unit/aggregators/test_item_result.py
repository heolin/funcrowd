import pytest

from modules.aggregation.aggregators import ValueFieldResult, ListFieldResult, ItemResult


@pytest.fixture
def item_result():
    return ItemResult(
        item_id=1,
        annotations_count=5,
        answers={
            "value_input_field": ValueFieldResult(1, 0.5, 2),
            "list_input_field": ListFieldResult([1], [0.5], [2]),
        }
    )


@pytest.mark.django_db
def test_item_result_to_json(item_result):
    """
    Test serialization of ItemTemplateField with two fields
    """
    data = item_result.to_json()
    assert type(data['item_id']) is int
    assert type(data['annotations_count']) is int
    assert len(data['answers']) == 2

    assert type(data['answers']['value_input_field']) is dict
    assert type(data['answers']['value_input_field']['probability']) is float

    assert type(data['answers']['list_input_field']) is dict
    assert type(data['answers']['list_input_field']['probability']) is list
