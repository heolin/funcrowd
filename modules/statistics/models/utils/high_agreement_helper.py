import numpy as np

import tasks as t

HIGH_AGREEMENT_THRESHOLD = 0.5


def get_high_agreement_count(user, mission=None):
    high_agreement_count = 0
    annotations = t.models.Annotation.objects.filter(user=user)
    if mission:
        annotations = annotations.filter(item__task__mission=mission)
    for annotation in annotations:
        feedback = annotation.get_feedback()
        if not feedback:
            continue
        avg_field_scores = {}
        for field, values in feedback.scores.items():
            avg_field_scores[field] = np.average(list(values.values()))
        avg_scores = np.average(list(avg_field_scores.values()))
        if avg_scores >= HIGH_AGREEMENT_THRESHOLD:
            high_agreement_count += 1
    return high_agreement_count
