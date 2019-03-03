import numpy as np

from .base import BaseAgreementMetric
from .utils import identity_kernel, get_weights


def observed_agreement(df, dfa, weights_kernel=identity_kernel):
    N, q = df.shape
    n = df.sum(axis=1)

    w = get_weights(q, weights_kernel)

    r_star = df.dot(w)

    po = ((df * (r_star-1)).sum(axis=1) / (n * (n-1))).sum()/N
    return po


class ObservedAgreementMetric(BaseAgreementMetric):

    def _metric(self, df, dfa):
        return observed_agreement(df, dfa)
