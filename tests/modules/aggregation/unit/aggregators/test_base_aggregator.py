import pytest
import pandas as pd

from modules.aggregation.aggregators.base import BaseAggregator


@pytest.fixture
@pytest.mark.django_db
def base_aggregator(one_task_multiple_items_with_multiple_annotations_and_reference) -> BaseAggregator:
    task = one_task_multiple_items_with_multiple_annotations_and_reference
    return BaseAggregator(task)


@pytest.fixture
def annotations_table() -> pd.DataFrame:
    return pd.DataFrame([
        [1, [1], 0, 'user0'],
        [1, [1, 2], 1, 'user0'],
        [2, [2], 2, 'user0'],
        [1, [1], 0, 'user1'],
        [2, [2], 1, 'user1'],
        [2, [2], 2, 'user1'],
        [1, [1], 0, 'user2'],
        [2, [1, 2], 1, 'user2'],
        [2, [2], 2, 'user2'],
    ], columns=['input_field', 'list_input_field', 'item', 'user'])


@pytest.mark.django_db
def test_get_annotations_table_whole_task(base_aggregator: BaseAggregator):
    aggregator = base_aggregator

    df_annotations_table = aggregator._get_annotations_table()
    assert len(df_annotations_table) == 32
    assert len(df_annotations_table['user'].unique()) == 6
    assert set(df_annotations_table.columns) == {'input_field', 'item', 'user'}


@pytest.mark.django_db
def test_get_field_result(base_aggregator: BaseAggregator, annotations_table: pd.DataFrame):
    aggregator = base_aggregator

    # item_id = 0
    group = annotations_table[annotations_table['item'] == 0]
    item_result = aggregator._get_field_result(group, 'input_field')
    assert item_result.answer == '1'
    assert item_result.probability == 1.0
    assert item_result.support == 3

    # item_id = 1
    group = annotations_table[annotations_table['item'] == 1]
    item_result = aggregator._get_field_result(group, 'input_field')
    assert item_result.answer == '2'
    assert round(item_result.probability, 2) == 0.67
    assert item_result.support == 2


@pytest.mark.django_db
def test_get_list_field_result(base_aggregator: BaseAggregator, annotations_table: pd.DataFrame):
    aggregator = base_aggregator

    # item_id = 0
    group = annotations_table[annotations_table['item'] == 0]
    item_result = aggregator._get_list_field_result(group, 'list_input_field')
    assert item_result.answer == [1.0]
    assert [round(p, 2) for p in item_result.probability] == [1.0]
    assert item_result.support == [3]

    # item_id = 1
    group = annotations_table[annotations_table['item'] == 1]
    item_result = aggregator._get_list_field_result(group, 'list_input_field')
    assert item_result.answer == [1.0, 2.0]
    assert [round(p, 2) for p in item_result.probability] == [0.67, 1.0]
    assert item_result.support == [2, 3]
