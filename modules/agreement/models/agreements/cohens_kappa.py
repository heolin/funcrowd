import numpy as np

from .base import BaseAgreementMetric
from .utils import identity_kernel, get_weights


def cohens_kappa(df, dfa, weights_kernel=identity_kernel):
    N, q = df.shape
    n = df.sum(axis=1)

    w = get_weights(q, weights_kernel)

    r_star = df.dot(w)

    po = ((df * (r_star-1)).sum(axis=1) / (n * (n-1))).sum() / N

    p = dfa.div(dfa.sum(axis=1), axis=0)
    r, q = p.shape

    pbar = p.sum(axis=0) / r

    rpbar = r * np.array(pbar).reshape(1, q).T * np.array(pbar).reshape(1, q)
    pg = np.array(p).T.dot(np.array(p))
    s2 = (pg - rpbar) / (r - 1)

    pbarplus = np.array(pbar).reshape(1, q).T * np.array(pbar).reshape(1, q)
    pc = (w * (pbarplus - s2/r)).sum()

    k = (po - pc) / (1 - pc)
    return k


class CohensKappaMetric(BaseAgreementMetric):

    def _metric(self, df, dfa):
        return cohens_kappa(df, dfa)
