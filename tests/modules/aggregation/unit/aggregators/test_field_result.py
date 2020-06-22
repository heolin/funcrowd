import pytest

from modules.aggregation.aggregators import FieldResult


@pytest.fixture
def value_field_result():
    return FieldResult("1", 0.4, 3)


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

