import pytest
import pandas as pd

from modules.aggregation.aggregators import (
    BaseAggregator, ValueFieldResult, ListFieldResult
)
from modules.aggregation.models import ItemAggregation


# fixtures
@pytest.fixture
@pytest.mark.django_db
def empty_task_aggregator(one_task_items_with_reference_annotation) -> BaseAggregator:
    task = one_task_items_with_reference_annotation
    return BaseAggregator(task)


@pytest.fixture
@pytest.mark.django_db
def task_aggregator(one_task_items_with_annotations_and_reference) -> BaseAggregator:
    task = one_task_items_with_annotations_and_reference
    return BaseAggregator(task)


@pytest.fixture
@pytest.mark.django_db
def list_task_aggregator(one_task_items_with_list_annotations_and_reference) -> BaseAggregator:
    task = one_task_items_with_list_annotations_and_reference
    return BaseAggregator(task)


@pytest.fixture
def empty_annotations_table():
    return pd.DataFrame()


# tests
@pytest.mark.django_db
def test_get_annotations_table_single_item(one_task_items_with_annotations_and_reference):
    """
    Test computing `annotations_table` only for a selected item,
    when item restriction is set on the aggregator.
    """

    task = one_task_items_with_annotations_and_reference
    aggregator = BaseAggregator(task, item=task.items.first())
    annotations_table = aggregator._get_annotations_table()

    assert len(annotations_table) == 5
    assert len(annotations_table['user'].unique()) == 5
    assert set(annotations_table.columns) == {'input_field', 'item', 'user'}


@pytest.mark.django_db
def test_get_annotations_table_whole_task(task_aggregator: BaseAggregator):
    """
    Test computing `annotations_table` for the whole task
    """
    aggregator = task_aggregator
    annotations_table = aggregator._get_annotations_table()

    assert len(annotations_table) == 30
    assert len(annotations_table['user'].unique()) == 5
    assert set(annotations_table.columns) == {'input_field', 'item', 'user'}


@pytest.mark.django_db
def test_get_annotations_table_empty_task(empty_task_aggregator: BaseAggregator):
    """
    Test computing `annotations_table` for an empty task
    """
    aggregator = empty_task_aggregator
    annotations_table = aggregator._get_annotations_table()

    assert len(annotations_table) == 0


@pytest.mark.django_db
def test_get_field_result(task_aggregator: BaseAggregator):
    """
    Test getting aggregated answer for standard value field.
    """
    aggregator = task_aggregator
    annotations_table = aggregator._get_annotations_table()
    items = aggregator.task.items.all()

    # first_item
    item = items[0]
    group = annotations_table[annotations_table['item'] == item.id]
    field_result = aggregator._get_field_result(group, 'input_field')
    assert type(field_result) is ValueFieldResult
    assert field_result.answer == '0'
    assert field_result.probability == 0.4
    assert field_result.support == 2

    # second_item
    item = items[1]
    group = annotations_table[annotations_table['item'] == item.id]
    field_result = aggregator._get_field_result(group, 'input_field')
    assert field_result.answer == '1'
    assert round(field_result.probability, 2) == 0.8
    assert field_result.support == 4


@pytest.mark.django_db
def test_get_list_field_result(list_task_aggregator: BaseAggregator):
    """
    Test getting aggregated answer for a list field
    """
    aggregator = list_task_aggregator
    annotations_table = aggregator._get_annotations_table()
    items = aggregator.task.items.all()

    # item_id = 0
    item = items[0]
    group = annotations_table[annotations_table['item'] == item.id]
    field_result = aggregator._get_list_field_result(group, 'list_input_field')
    assert type(field_result) is ListFieldResult
    assert field_result.answer == ['1', '2']
    assert [round(p, 2) for p in field_result.probability] == [0.8, 0.6]
    assert field_result.support == [4, 3]

    # item_id = 1
    item = items[1]
    group = annotations_table[annotations_table['item'] == item.id]
    field_result = aggregator._get_list_field_result(group, 'list_input_field')
    assert field_result.answer == ['2']
    assert [round(p, 2) for p in field_result.probability] == [1.0]
    assert field_result.support == [5]


@pytest.mark.django_db
def test_logic(task_aggregator: BaseAggregator):
    """
    Test full aggregation logic
    """
    aggregator = task_aggregator
    annotations_table = aggregator._get_annotations_table()
    item = aggregator.task.items.all()[0]

    item_results = aggregator._logic(annotations_table)

    assert len(item_results) == 6

    item_result = item_results[0]
    assert item_result.item_id == item.id
    assert item_result.annotations_count == 5
    assert len(item_result.answers) == 1

    field_result = item_result.answers['input_field']
    assert field_result.answer == '0'
    assert field_result.probability == 0.4
    assert field_result.support == 2


@pytest.mark.django_db
def test_logic_empty_table(task_aggregator: BaseAggregator, empty_annotations_table: pd.DataFrame):
    """
    Test full aggregation logic for an empty table
    """
    aggregator = task_aggregator

    item_results = aggregator._logic(empty_annotations_table)

    assert len(item_results) == 0


@pytest.mark.django_db
def test_logic_list_task(list_task_aggregator: BaseAggregator):
    """
    Test full aggregation logic for list field
    """
    aggregator = list_task_aggregator
    df_annotations_table = aggregator._get_annotations_table()
    item = aggregator.task.items.all()[0]

    item_results = aggregator._logic(df_annotations_table)

    assert len(item_results) == 3

    item_result = item_results[0]
    assert item_result.item_id == item.id
    assert item_result.annotations_count == 5
    assert len(item_result.answers) == 1

    field_result = item_result.answers['list_input_field']
    assert field_result.answer == ['1', '2']
    assert [round(p, 2) for p in field_result.probability] == [0.8, 0.6]
    assert field_result.support == [4, 3]


@pytest.mark.django_db
def test_aggregate(task_aggregator: BaseAggregator):
    """
    Test performing aggregation and saving/updating ItemAggregation
    objects in the database.
    """
    aggregator = task_aggregator

    item_aggregations = aggregator.aggregate()

    assert len(item_aggregations) == ItemAggregation.objects.count()

    item_aggregation = item_aggregations[0]
    assert item_aggregation.type == "BaseAggregator"
    assert set(item_aggregation.data.keys()) == \
           {'answers', 'item_id', 'annotations_count'}


@pytest.mark.django_db
def empty_test_aggregate(empty_task_aggregator: BaseAggregator):
    """
    Test performing aggregation on an empty task with no annotations
    """
    aggregator = empty_task_aggregator

    item_aggregations = aggregator.aggregate()

    assert len(item_aggregations) == 0
    assert ItemAggregation.objects.count() == 0
