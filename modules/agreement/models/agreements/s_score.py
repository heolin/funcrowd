import numpy as np

from .base import BaseAgreementMetric
from .utils import identity_kernel, get_weights


def s_score(df, dfa, weights_kernel=identity_kernel):
    N, q = df.shape
    n = df.sum(axis=1)

    w = get_weights(q, weights_kernel)

    r_star = df.dot(w)

    po = ((df * (r_star-1)).sum(axis=1) / (n * (n-1))).sum()/N

    pc = w.sum() / q**2

    S = (po - pc) / (1 - pc)
    return S


class SScoreMetric(BaseAgreementMetric):

    def _metric(self, df, dfa):
        return s_score(df, dfa)
