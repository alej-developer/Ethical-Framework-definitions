"""EN: Asia-Pacific regulatory framework evaluators package. | ES: Paquete de evaluadores de marcos regulatorios de Asia-Pacifico."""

from domain.frameworks.asia_pacific.china_ai_regulations import ChinaAIRegulationsEvaluator
from domain.frameworks.asia_pacific.india_dpdp_ai import IndiaDPDPAIEvaluator
from domain.frameworks.asia_pacific.japan_ai_act import JapanAIActEvaluator
from domain.frameworks.asia_pacific.korea_ai_basic_act import KoreaAIBasicActEvaluator
from domain.frameworks.asia_pacific.singapore_ai_governance import SingaporeAIGovernanceEvaluator

__all__ = [
    "KoreaAIBasicActEvaluator",
    "ChinaAIRegulationsEvaluator",
    "JapanAIActEvaluator",
    "SingaporeAIGovernanceEvaluator",
    "IndiaDPDPAIEvaluator",
]
