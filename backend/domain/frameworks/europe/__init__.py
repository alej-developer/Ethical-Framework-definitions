"""EN: European regulatory framework evaluators package. | ES: Paquete de evaluadores de marcos regulatorios europeos."""

from domain.frameworks.europe.coe_ai_convention import CoEAIConventionEvaluator
from domain.frameworks.europe.eu_ai_act import EUAIActEvaluator
from domain.frameworks.europe.uk_ai_governance import UKAIGovernanceEvaluator

__all__ = ["CoEAIConventionEvaluator", "EUAIActEvaluator", "UKAIGovernanceEvaluator"]
