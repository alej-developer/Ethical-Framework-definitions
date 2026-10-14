"""EN: Americas regulatory framework evaluators package. | ES: Paquete de evaluadores de marcos regulatorios de las Americas."""

from domain.frameworks.americas.brazil_pl_2338 import BrazilPL2338Evaluator
from domain.frameworks.americas.nist_ai_rmf import NISTAIRMFEvaluator

__all__ = ["NISTAIRMFEvaluator", "BrazilPL2338Evaluator"]
