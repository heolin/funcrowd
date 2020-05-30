import pytest

from modules.aggregation.aggregators import ValueFieldResult, ListFieldResult


@pytest.fixture
def value_field_result():
    return ValueFieldResult("1", 0.4, 3)


@pytest.fixture
def list_field_result():
    return ListFieldResult(["1", "2"], [1.0, 0.4], [5, 2])


@pytest.mark.django_db
def test_value_field_result_to_json(value_field_result):
    """
    Test serialization of ValueFieldResult
    """
    data = value_field_result.to_json()

    assert set(data.keys()) == {'answer', 'probability', 'support'}
    assert data['answer'] is not None
    assert type(data['probability']) is float
    assert type(data['support']) is int


@pytest.mark.django_db
def test_list_field_result_to_json(list_field_result):
    """
    Test serialization of ListValueField
    """
    data = list_field_result.to_json()

    assert set(data.keys()) == {'answer', 'probability', 'support'}
    assert data['answer'] is not None
    assert type(data['probability']) is list
    assert type(data['probability'][0]) is float
    assert type(data['support']) is list
    assert type(data['support'][0]) is int
