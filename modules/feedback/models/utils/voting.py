import pandas as pd
from tasks.field_types import LIST


def get_votings(annotations, field):
    other_values = annotations.values_list("data", flat=True)
    other_values = list(other_values)
    if field.type == LIST:
        results = []
        for row in other_values:
            for key, values in row.items():
                for value in values:
                    results.append({key: value})
        other_values = results
    df_other = pd.DataFrame(other_values)
    print(df_other[field.name].value_counts())
    df_probs = df_other[field.name].value_counts() / len(df_other)
    return df_probs
