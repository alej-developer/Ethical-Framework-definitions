"""EN: Korea Framework Act on AI Development and Establishment of Trust (AI Basic Act) evaluator. | ES: Evaluador de la Ley Marco de Corea sobre Desarrollo de IA y Establecimiento de Confianza (Ley Basica de IA)."""

from domain.entities import (
    BindingLevel,
    EthicalFinding,
    EvaluationMetric,
    FrameworkRegion,
    FrameworkType,
    RiskTier,
    Scenario,
)
from domain.frameworks.base import BaseFrameworkEvaluator


class KoreaAIBasicActEvaluator(BaseFrameworkEvaluator):
    """EN: Promulgated January 2025, in force from January 2026; regulates high-impact and generative AI. | ES: Promulgada en enero de 2025, vigente desde enero de 2026; regula la IA de alto impacto y la generativa."""

    binding_level = BindingLevel.LEGALLY_BINDING
    region = FrameworkRegion.ASIA_PACIFIC

    @property
    def framework(self) -> FrameworkType:
        """EN: Return the Korea AI Basic Act identifier. | ES: Retorna el identificador de la Ley Basica de IA de Corea."""
        return FrameworkType.KOREA_AI_BASIC_ACT

    def _classify_risk_tier(self, scenario: Scenario) -> RiskTier:
        """EN: High-impact AI vs. generative AI notice duties. | ES: IA de alto impacto frente a deberes de aviso de IA generativa."""
        if self._is_prohibited(scenario) or self._is_high_impact(scenario):
            return RiskTier.HIGH_RISK
        if self._is_generative(scenario):
            return RiskTier.SPECIFIC_TRANSPARENCY_RISK
        return RiskTier.MINIMAL_RISK

    def _calculate_metrics(self, scenario: Scenario) -> list[EvaluationMetric]:
        """EN: Transparency, risk management and user protection duties. | ES: Deberes de transparencia, gestion de riesgos y proteccion del usuario."""
        notice = 1.0 if self._flag(scenario, "content_labeling_enabled") or self._flag(scenario, "confidence_scores_visible") else 0.0
        explanation = 1.0 if self._flag(scenario, "explainability_enabled") else 0.0
        oversight = 1.0 if self._flag(scenario, "human_in_the_loop") else 0.0
        return [
            self._metric("AI Use Notice & Labeling", notice, 1.0, "Users are notified that AI or generative AI is involved."),
            self._metric("Explanation of Outcomes", explanation, 1.0, "High-impact operators explain criteria and key data where feasible."),
            self._metric("Human Oversight", oversight, 1.0, "Human management and supervision of high-impact AI."),
            self._metric("Fairness Gap", self._dialectal_parity_gap(scenario), 0.15, "Trustworthiness duty: avoid discriminatory outcomes.", lower_is_better=True),
        ]

    def _audit(self, scenario: Scenario, risk_tier: RiskTier, metrics: list[EvaluationMetric]) -> list[EthicalFinding]:
        """EN: Apply duties according to tier. | ES: Aplicar deberes segun el nivel."""
        high = risk_tier == RiskTier.HIGH_RISK
        generative = self._is_generative(scenario)
        applicable = {
            "AI Use Notice & Labeling": high or generative,
            "Explanation of Outcomes": high,
            "Human Oversight": high,
            "Fairness Gap": True,
        }
        fixes = {
            "AI Use Notice & Labeling": "Display advance notice of AI use and label generated outputs.",
            "Explanation of Outcomes": "Document and disclose decision criteria for high-impact use.",
            "Human Oversight": "Establish human supervision and a risk management plan.",
            "Fairness Gap": "Reduce error disparity between linguistic groups.",
        }
        return [
            self._finding(f"AI Basic Act: {m.name}", "HIGH" if high else "MEDIUM", f"Score {m.score} vs. {m.threshold}.", fixes[m.name])
            for m in metrics
            if not m.passed and applicable[m.name]
        ]

    def _steady_state_recommendation(self) -> str:
        """EN: Default Korea recommendation. | ES: Recomendacion coreana por defecto."""
        return "Monitor Enforcement Decrees issued by the Ministry of Science and ICT."
