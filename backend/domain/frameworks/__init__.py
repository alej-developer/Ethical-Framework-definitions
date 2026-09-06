"""EN: Ethical framework package initialization. | ES: Inicializacion del paquete de marcos eticos."""

from domain.frameworks.eu_ai_act import EUAIActEvaluator
from domain.frameworks.ieee_standards import IEEEStandardsEvaluator

__all__ = ["EUAIActEvaluator", "IEEEStandardsEvaluator"]
