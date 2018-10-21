import numpy as np

from .base import BaseAgreementMetric
from .utils import identity_kernel, get_weights


def gwets_gamma(df, dfa, weights_kernel=identity_kernel):
    N, q = df.shape
    n = df.sum(axis=1)

    w = get_weights(q, weights_kernel)

    r_star = df.dot(w)

    po = ((df * (r_star-1)).sum(axis=1) / (n * (n-1))).sum() / N

    Tw = w.sum()

    pi = df.div(df.sum(axis=1), axis=0).sum() / N

    pc = (pi*(1 - pi)).values.sum() * Tw / (q*(q-1))

    gamma = (po - pc) / (1 - pc)
    return gamma


class GwetsGammaMetric(BaseAgreementMetric):

    def _metric(self, df, dfa):
        return gwets_gamma(df, dfa)
