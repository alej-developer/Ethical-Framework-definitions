"""EN: Americas regulatory framework evaluators package. | ES: Paquete de evaluadores de marcos regulatorios de las Americas."""

from domain.frameworks.americas.brazil_pl_2338 import BrazilPL2338Evaluator
from domain.frameworks.americas.colorado_ai_act import ColoradoAIActEvaluator
from domain.frameworks.americas.nist_ai_rmf import NISTAIRMFEvaluator
from domain.frameworks.americas.peru_ai_law import PeruAILaw31814Evaluator

__all__ = [
    "BrazilPL2338Evaluator",
    "ColoradoAIActEvaluator",
    "NISTAIRMFEvaluator",
    "PeruAILaw31814Evaluator",
]
