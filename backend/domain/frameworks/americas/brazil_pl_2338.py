"""EN: Brazil Bill PL 2338/2023 (AI regulatory framework) evaluator. | ES: Evaluador del Proyecto de Ley PL 2338/2023 de Brasil (marco regulatorio de IA)."""

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


class BrazilPL2338Evaluator(BaseFrameworkEvaluator):
    """EN: Risk-based bill approved by the Senate (Dec 2024) and pending in the Chamber of Deputies. | ES: Proyecto basado en riesgo aprobado por el Senado (dic. 2024) y pendiente en la Camara de Diputados."""

    binding_level = BindingLevel.PROPOSED_LEGISLATION
    region = FrameworkRegion.AMERICAS

    @property
    def framework(self) -> FrameworkType:
        """EN: Return the Brazil PL 2338 identifier. | ES: Retorna el identificador del PL 2338 de Brasil."""
        return FrameworkType.BRAZIL_PL_2338

    def _classify_risk_tier(self, scenario: Scenario) -> RiskTier:
        """EN: Excessive risk (prohibited) vs. high risk categories. | ES: Riesgo excesivo (prohibido) frente a categorias de alto riesgo."""
        if self._is_prohibited(scenario):
            return RiskTier.UNACCEPTABLE_RISK
        if self._is_high_impact(scenario):
            return RiskTier.HIGH_RISK
        if self._is_generative(scenario):
            return RiskTier.SPECIFIC_TRANSPARENCY_RISK
        return RiskTier.MINIMAL_RISK

    def _calculate_metrics(self, scenario: Scenario) -> list[EvaluationMetric]:
        """EN: Rights of affected persons and governance duties. | ES: Derechos de las personas afectadas y deberes de gobernanza."""
        explanation = 1.0 if self._flag(scenario, "explainability_enabled") else 0.0
        human_review = 1.0 if self._flag(scenario, "human_in_the_loop") else 0.0
        impact_assessment = 1.0 if self._flag(scenario, "impact_assessment_completed") or self._flag(scenario, "provenance_verified") else 0.0
        return [
            self._metric("Right to Explanation", explanation, 1.0, "Affected persons may request an explanation of the decision."),
            self._metric("Right to Human Review", human_review, 1.0, "Affected persons may contest and request human participation."),
            self._metric("Non-Discrimination Gap", self._dialectal_parity_gap(scenario), 0.15, "Prohibition of unlawful or abusive discrimination.", lower_is_better=True),
            self._metric("Algorithmic Impact Assessment", impact_assessment, 1.0, "Documented assessment required for high-risk systems."),
        ]

    def _audit(self, scenario: Scenario, risk_tier: RiskTier, metrics: list[EvaluationMetric]) -> list[EthicalFinding]:
        """EN: Rights-based findings, stricter for high-risk systems. | ES: Hallazgos basados en derechos, mas estrictos para sistemas de alto riesgo."""
        if risk_tier == RiskTier.UNACCEPTABLE_RISK:
            return [
                self._finding(
                    "Excessive Risk",
                    "CRITICAL",
                    f"Domain '{scenario.domain_category}' falls under excessive-risk practices.",
                    "Do not deploy; excessive-risk systems are barred under the bill.",
                )
            ]
        high = risk_tier == RiskTier.HIGH_RISK
        fixes = {
            "Right to Explanation": "Implement per-decision explanations available on request.",
            "Right to Human Review": "Guarantee a human review channel for contested outcomes.",
            "Non-Discrimination Gap": "Correct disparate error rates across linguistic groups.",
            "Algorithmic Impact Assessment": "Complete and publish an algorithmic impact assessment.",
        }
        findings: list[EthicalFinding] = []
        for m in metrics:
            if m.passed:
                continue
            # EN: Impact assessment is only mandatory for high-risk systems | ES: La evaluacion de impacto solo es obligatoria para alto riesgo
            if m.name == "Algorithmic Impact Assessment" and not high:
                continue
            findings.append(self._finding(f"PL 2338: {m.name}", "HIGH" if high else "MEDIUM", f"Score {m.score} vs. {m.threshold}.", fixes[m.name]))
        return findings

    def _steady_state_recommendation(self) -> str:
        """EN: Default Brazil recommendation. | ES: Recomendacion brasilena por defecto."""
        return "Track the bill in the Chamber of Deputies and the LGPD guidance issued by the ANPD."
