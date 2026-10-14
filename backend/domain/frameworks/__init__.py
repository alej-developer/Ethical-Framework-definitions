"""EN: Ethical framework package initialization aggregating regional evaluators. | ES: Inicializacion del paquete de marcos eticos que agrega los evaluadores regionales."""

from domain.frameworks.americas import BrazilPL2338Evaluator, NISTAIRMFEvaluator
from domain.frameworks.asia_pacific import (
    ChinaAIRegulationsEvaluator,
    IndiaDPDPAIEvaluator,
    JapanAIActEvaluator,
    KoreaAIBasicActEvaluator,
    SingaporeAIGovernanceEvaluator,
)
from domain.frameworks.base import BaseFrameworkEvaluator
from domain.frameworks.europe import EUAIActEvaluator, UKAIGovernanceEvaluator
from domain.frameworks.international import IEEEStandardsEvaluator
from domain.interfaces import IEthicalEvaluator


def build_default_evaluators() -> list[IEthicalEvaluator]:
    """EN: Instantiate every implemented framework evaluator. | ES: Instanciar todos los evaluadores de marcos implementados."""
    return [
        EUAIActEvaluator(),
        UKAIGovernanceEvaluator(),
        NISTAIRMFEvaluator(),
        BrazilPL2338Evaluator(),
        KoreaAIBasicActEvaluator(),
        ChinaAIRegulationsEvaluator(),
        JapanAIActEvaluator(),
        SingaporeAIGovernanceEvaluator(),
        IndiaDPDPAIEvaluator(),
        IEEEStandardsEvaluator(),
    ]


__all__ = [
    "BaseFrameworkEvaluator",
    "BrazilPL2338Evaluator",
    "ChinaAIRegulationsEvaluator",
    "EUAIActEvaluator",
    "IEEEStandardsEvaluator",
    "IndiaDPDPAIEvaluator",
    "JapanAIActEvaluator",
    "KoreaAIBasicActEvaluator",
    "NISTAIRMFEvaluator",
    "SingaporeAIGovernanceEvaluator",
    "UKAIGovernanceEvaluator",
    "build_default_evaluators",
]
