"""EN: Singapore Model AI Governance Framework (2nd ed. 2020; Generative AI edition 2024) evaluator. | ES: Evaluador del Marco Modelo de Gobernanza de IA de Singapur (2a ed. 2020; edicion IA Generativa 2024)."""

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


class SingaporeAIGovernanceEvaluator(BaseFrameworkEvaluator):
    """EN: Voluntary IMDA/PDPC framework, testable through the AI Verify toolkit. | ES: Marco voluntario de IMDA/PDPC, verificable mediante el kit AI Verify."""

    binding_level = BindingLevel.VOLUNTARY_STANDARD
    region = FrameworkRegion.ASIA_PACIFIC

    @property
    def framework(self) -> FrameworkType:
        """EN: Return the Singapore AI governance identifier. | ES: Retorna el identificador de gobernanza de IA de Singapur."""
        return FrameworkType.SINGAPORE_AI_GOVERNANCE

    def _classify_risk_tier(self, scenario: Scenario) -> RiskTier:
        """EN: Probability/severity matrix for human involvement. | ES: Matriz probabilidad/severidad para la intervencion humana."""
        if self._is_prohibited(scenario) or self._is_high_impact(scenario):
            return RiskTier.HIGH_RISK
        if self._is_generative(scenario):
            return RiskTier.SPECIFIC_TRANSPARENCY_RISK
        return RiskTier.MINIMAL_RISK

    def _calculate_metrics(self, scenario: Scenario) -> list[EvaluationMetric]:
        """EN: Four framework areas. | ES: Cuatro areas del marco."""
        governance = 1.0 if self._flag(scenario, "provenance_verified") else 0.0
        human_involvement = 1.0 if self._flag(scenario, "human_in_the_loop") else 0.0
        communication = (0.5 if self._flag(scenario, "explainability_enabled") else 0.0) + (
            0.5 if self._flag(scenario, "confidence_scores_visible") else 0.0
        )
        return [
            self._metric("Internal Governance", governance, 1.0, "Clear roles, data accountability and risk controls."),
            self._metric("Human Involvement", human_involvement, 1.0, "Level of human oversight proportionate to risk."),
            self._metric("Operations Management Bias Gap", self._dialectal_parity_gap(scenario), 0.15, "Data quality and bias minimisation.", lower_is_better=True),
            self._metric("Stakeholder Communication", communication, 0.50, "Disclosure, explanation and feedback channels."),
        ]

    def _audit(self, scenario: Scenario, risk_tier: RiskTier, metrics: list[EvaluationMetric]) -> list[EthicalFinding]:
        """EN: Human involvement only required for higher-risk contexts. | ES: La intervencion humana solo se exige en contextos de mayor riesgo."""
        high = risk_tier == RiskTier.HIGH_RISK
        fixes = {
            "Internal Governance": "Assign AI governance roles and document data lineage.",
            "Human Involvement": "Move to human-in-the-loop for high-severity decisions.",
            "Operations Management Bias Gap": "Run AI Verify fairness tests per linguistic variety.",
            "Stakeholder Communication": "Publish disclosures and offer feedback and review channels.",
        }
        return [
            self._finding(f"Model AI Governance: {m.name}", "HIGH" if high else "MEDIUM", f"Score {m.score} vs. {m.threshold}.", fixes[m.name])
            for m in metrics
            if not m.passed and (m.name != "Human Involvement" or high)
        ]

    def _steady_state_recommendation(self) -> str:
        """EN: Default Singapore recommendation. | ES: Recomendacion de Singapur por defecto."""
        return "Publish an AI Verify report to evidence alignment with the framework."
