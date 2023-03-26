import pytest
import pandas as pd

"""
from modules.aggregation.aggregators.utils import decompose_list_column


@pytest.fixture
def list_field_data_frame():
    return pd.DataFrame([
        {"input_field": ["1", "2"], "other_field": "a"},
        {"input_field": ["1", "1"], "other_field": "b"},
        {"input_field": ["2"], "other_field": "c"},
    ])


def test_decompose_list_column(list_field_data_frame: pd.DataFrame):
    df = decompose_list_column(list_field_data_frame, 'input_field')

    assert len(df) == 5

    input_field_counts = df['input_field'].value_counts()
    assert input_field_counts.loc["1"] == 3
    assert input_field_counts.loc["2"] == 2

    other_field_counts = df['other_field'].value_counts()
    assert other_field_counts.loc["a"] == 2
    assert other_field_counts.loc["b"] == 2
    assert other_field_counts.loc["c"] == 1
"""

