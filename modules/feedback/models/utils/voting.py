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
    df_values = pd.DataFrame(list(annotations.values("item_id", "data"))).set_index("item_id")
    s_values = df_values['data'].apply(lambda x: x.get(field.name))
    s_values = s_values[s_values.notnull()]

    if field.type == LIST:
        s_values = s_values.apply(pd.Series).stack().reset_index(level=-1, drop=True)
    df_values = s_values.to_frame(field.name)

    if field.data_source:
        df_source_values = pd.DataFrame(list(annotations.values("item_id", "item__data").distinct()))\
            .set_index("item_id")
        df_source_values = df_source_values['item__data']\
            .apply(lambda x: x[field.data_source.name])\
            .to_frame(name=field.data_source.name)
        df_values = df_values.join(df_source_values)

        df_values[field.name] = df_values.apply(_filter_other_values,
                                                field_name=field.name,
                                                data_source_field_name=field.data_source.name,
                                                axis=1)
        df_values.drop(field.data_source.name, axis=1, inplace=True)

    df_probs = df_values[field.name].value_counts() / len(annotations)
    return df_probs
