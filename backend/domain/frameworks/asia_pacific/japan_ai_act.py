"""EN: Japan AI Promotion Act (2025) and AI Guidelines for Business evaluator. | ES: Evaluador de la Ley de Promocion de IA de Japon (2025) y las Directrices de IA para Empresas."""

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


class JapanAIActEvaluator(BaseFrameworkEvaluator):
    """EN: Statute without sanctions; operational duties come from the METI/MIC AI Guidelines for Business. | ES: Ley sin sanciones; los deberes operativos proceden de las Directrices de IA para Empresas de METI/MIC."""

    binding_level = BindingLevel.VOLUNTARY_STANDARD
    region = FrameworkRegion.ASIA_PACIFIC

    @property
    def framework(self) -> FrameworkType:
        """EN: Return the Japan AI Act identifier. | ES: Retorna el identificador de la Ley de IA de Japon."""
        return FrameworkType.JAPAN_AI_ACT

    def _classify_risk_tier(self, scenario: Scenario) -> RiskTier:
        """EN: Risk-based approach of the Guidelines. | ES: Enfoque basado en riesgo de las Directrices."""
        if self._is_prohibited(scenario) or self._is_high_impact(scenario):
            return RiskTier.HIGH_RISK
        if self._is_generative(scenario):
            return RiskTier.SPECIFIC_TRANSPARENCY_RISK
        return RiskTier.MINIMAL_RISK

    def _calculate_metrics(self, scenario: Scenario) -> list[EvaluationMetric]:
        """EN: Human-centric, safety, fairness, transparency and accountability principles. | ES: Principios de centralidad humana, seguridad, equidad, transparencia y rendicion de cuentas."""
        harm = float(scenario.metadata.get("toxicity_exposure_rate", 0.0))
        transparency = (0.5 if self._flag(scenario, "explainability_enabled") else 0.0) + (
            0.5 if self._flag(scenario, "confidence_scores_visible") else 0.0
        )
        return [
            self._metric("Human-Centric & Safety", max(0.0, 1.0 - harm), 0.90, "Avoid harm to life, body, property and dignity."),
            self._metric("Fairness Gap", self._dialectal_parity_gap(scenario), 0.15, "Avoid unjust bias and discrimination.", lower_is_better=True),
            self._metric("Transparency", transparency, 0.50, "Provide reasonable information to stakeholders."),
            self._metric("Accountability", 1.0 if self._flag(scenario, "provenance_verified") else 0.0, 1.0, "Traceability and documentation across the value chain."),
        ]

    def _audit(self, scenario: Scenario, risk_tier: RiskTier, metrics: list[EvaluationMetric]) -> list[EthicalFinding]:
        """EN: Soft-law findings capped at HIGH. | ES: Hallazgos de soft-law limitados a HIGH."""
        severity = "HIGH" if risk_tier == RiskTier.HIGH_RISK else "MEDIUM"
        fixes = {
            "Human-Centric & Safety": "Introduce safety evaluation and red-teaming before release.",
            "Fairness Gap": "Evaluate performance per linguistic group and rebalance data.",
            "Transparency": "Publish usage policies, limitations and explanation mechanisms.",
            "Accountability": "Maintain logs and documentation enabling traceability.",
        }
        return [
            self._finding(f"AI Guidelines for Business: {m.name}", severity, f"Score {m.score} vs. {m.threshold}.", fixes[m.name])
            for m in metrics
            if not m.passed
        ]

    def _steady_state_recommendation(self) -> str:
        """EN: Default Japan recommendation. | ES: Recomendacion japonesa por defecto."""
        return "Follow updates from the AI Strategy Headquarters and the AI Basic Plan."
