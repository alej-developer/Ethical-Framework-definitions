"""EN: International standards evaluators package. | ES: Paquete de evaluadores de estandares internacionales."""

from domain.frameworks.international.ieee_standards import IEEEStandardsEvaluator
from domain.frameworks.international.iso_42001 import ISO42001Evaluator

__all__ = ["IEEEStandardsEvaluator", "ISO42001Evaluator"]
