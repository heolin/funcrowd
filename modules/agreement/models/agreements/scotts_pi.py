import numpy as np

from .base import BaseAgreementMetric
from .utils import identity_kernel, get_weights


def scotts_pi(df, dfa, weights_kernel=identity_kernel):
    N, q = df.shape
    n = df.sum(axis=1)

    w = get_weights(q, weights_kernel)

    r_star = df.dot(w)

    po = ((df * (r_star-1)).sum(axis=1) / (n * (n-1))).sum() / N

    pik = df.div(df.sum(axis=1), axis=0).sum() / N

    pc = (w * np.array(pik).reshape(1, q).T * np.array(pik).reshape(1, q)).sum()

    pi = (po - pc) / (1 - pc)
    return pi


class ScottsPiMetric(BaseAgreementMetric):

    def _metric(self, df, dfa):
        return scotts_pi(df, dfa)
