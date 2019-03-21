import pandas as pd
from tasks.field_types import LIST


def filter_values(value, values):
    if value in values:
        return value
    else:
        return "<OTHER>"


def _filter_other_values(row, field_name, data_source_field_name):
    return filter_values(row[field_name], row[data_source_field_name])


def get_votings(annotations, field):
    other_values = list(annotations.values_list("data", flat=True))
    if field.type == LIST:
        results = []
        for row in other_values:
            for key, values in row.items():
                for value in values:
                    results.append({key: value})
        other_values = results
    df_other = pd.DataFrame(other_values)

    if field.data_source:
        items_values = list(annotations.values_list("item__data", flat=True))
        df_other[field.data_source.name] = [row[field.data_source.name] for row in items_values]
        df_other[field.name] = df_other.apply(_filter_other_values,
                                              field_name=field.name,
                                              data_source_field_name=field.data_source.name,
                                              axis=1)
        df_other = df_other.drop(field.data_source.name, axis=1)

    df_probs = df_other[field.name].value_counts() / len(df_other)
    return df_probs
