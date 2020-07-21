import pandas as pd
import numpy as np
from ast import literal_eval


def _get_annotation_data(annotation, field_name):
    annotation_data = annotation.data[field_name]
    if type(annotation_data) is str:
        annotation_data = literal_eval(annotation_data)
    return annotation_data


def get_tags_table(annotation, reference, field_name):
    tags = {}

    reference_data = _get_annotation_data(reference, field_name)

    for tag in reference_data:
        key = tuple(tag['tokens'])
        tags[key] = {
            'text': tag['text'],
            'reference': tag['tag']
        }

    annotation_data = _get_annotation_data(annotation, field_name)

    for tag in annotation_data:
        key = tuple(tag['tokens'])
        if key not in tags:
            tags[key] = {
                'text': tag['text'],
                'annotation': tag['tag']
            }
        else:
            tags[key]['annotation'] = tag['tag']

    df = pd.DataFrame(list(tags.values()))
    df = df.replace({np.nan: None})
    df['is_correct'] = df['annotation'] == df['reference']
    return df
