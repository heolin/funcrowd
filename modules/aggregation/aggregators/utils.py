import pandas as pd


def decompose_list_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Decomposes values from a column containing list values to multiple rows.

    :param df: input data frame
    :param column: selected column containing lists
    :return: updated data frame
    """
    column_values = df[column].apply(
        pd.Series).stack().reset_index(level=1, drop=True)
    df = df.drop(column, axis=1)
    df = df.join(column_values.rename(column))
    return df
