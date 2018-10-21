import numpy as np

from .base import BaseAgreementMetric
from .utils import identity_kernel, get_weights


def krippendorffs_alpha(df, dfa, weights_kernel=identity_kernel):
    N, q = df.shape
    n = df.sum(axis=1)

    w = get_weights(q, weights_kernel)

    r_star = df.dot(w)

    po2 = ((df * (r_star-1)).sum(axis=1) / (n * (n-1))).sum()/N

    rdash = df.sum(axis=1).sum() / N

    epsilon = 1 / (N*rdash)
    po = po2 * (1-epsilon) + epsilon

    pi = df.div(df.sum(axis=1), axis=0).sum() / N

    pc = (w * np.array(pi).reshape(1, q).T * np.array(pi).reshape(1, q)).sum()

    alpha = (po - pc) / (1 - pc)
    return alpha


class KrippendorffsAlphaMetric(BaseAgreementMetric):

    def _metric(self, df, dfa):
        return krippendorffs_alpha(df, dfa)
