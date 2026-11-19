"""EN: Ethical framework package initialization aggregating regional evaluators. | ES: Inicializacion del paquete de marcos eticos que agrega los evaluadores regionales."""

from domain.frameworks.africa import AUContinentalAIEvaluator
from domain.frameworks.americas import (
    BrazilPL2338Evaluator,
    ColoradoAIActEvaluator,
    NISTAIRMFEvaluator,
    PeruAILaw31814Evaluator,
)
from domain.frameworks.asia_pacific import (
    ChinaAIRegulationsEvaluator,
    IndiaDPDPAIEvaluator,
    JapanAIActEvaluator,
    KoreaAIBasicActEvaluator,
    SingaporeAIGovernanceEvaluator,
)
from domain.frameworks.base import BaseFrameworkEvaluator
from domain.frameworks.europe import CoEAIConventionEvaluator, EUAIActEvaluator, UKAIGovernanceEvaluator
from domain.frameworks.international import IEEEStandardsEvaluator, ISO42001Evaluator
from domain.interfaces import IEthicalEvaluator


def build_default_evaluators() -> list[IEthicalEvaluator]:
    """EN: Instantiate every implemented framework evaluator. | ES: Instanciar todos los evaluadores de marcos implementados."""
    return [
        EUAIActEvaluator(),
        UKAIGovernanceEvaluator(),
        CoEAIConventionEvaluator(),
        NISTAIRMFEvaluator(),
        ColoradoAIActEvaluator(),
        BrazilPL2338Evaluator(),
        PeruAILaw31814Evaluator(),
        KoreaAIBasicActEvaluator(),
        ChinaAIRegulationsEvaluator(),
        JapanAIActEvaluator(),
        SingaporeAIGovernanceEvaluator(),
        IndiaDPDPAIEvaluator(),
        AUContinentalAIEvaluator(),
        IEEEStandardsEvaluator(),
        ISO42001Evaluator(),
    ]


__all__ = [
    "AUContinentalAIEvaluator",
    "BaseFrameworkEvaluator",
    "BrazilPL2338Evaluator",
    "ChinaAIRegulationsEvaluator",
    "CoEAIConventionEvaluator",
    "ColoradoAIActEvaluator",
    "EUAIActEvaluator",
    "IEEEStandardsEvaluator",
    "ISO42001Evaluator",
    "IndiaDPDPAIEvaluator",
    "JapanAIActEvaluator",
    "KoreaAIBasicActEvaluator",
    "NISTAIRMFEvaluator",
    "PeruAILaw31814Evaluator",
    "SingaporeAIGovernanceEvaluator",
    "UKAIGovernanceEvaluator",
    "build_default_evaluators",
]
