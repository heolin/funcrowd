AGREEMENT_METRICS = {}

from .base import BaseAgreementMetric
from .cohens_kappa import CohensKappaMetric
from .gwets_gamma import GwetsGammaMetric
from .krippendorff_alpha import KrippendorffsAlphaMetric
from .observed_agreement import ObservedAgreementMetric
from .s_score import SScoreMetric
from .scotts_pi import ScottsPiMetric


for cls in BaseAgreementMetric.__subclasses__():
    AGREEMENT_METRICS[cls.__name__] = cls
