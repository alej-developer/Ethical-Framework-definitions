"""EN: UK pro-innovation AI regulation principles evaluator (DSIT White Paper, 2023). | ES: Evaluador de los principios de regulacion de IA pro-innovacion del Reino Unido (Libro Blanco DSIT, 2023)."""

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


class UKAIGovernanceEvaluator(BaseFrameworkEvaluator):
    """EN: Audits the five cross-sectoral, non-statutory UK principles applied by sector regulators. | ES: Audita los cinco principios transversales y no estatutarios del Reino Unido aplicados por los reguladores sectoriales."""

    binding_level = BindingLevel.VOLUNTARY_STANDARD
    region = FrameworkRegion.EUROPE

    @property
    def framework(self) -> FrameworkType:
        """EN: Return the UK AI Governance identifier. | ES: Retorna el identificador de Gobernanza de IA del Reino Unido."""
        return FrameworkType.UK_AI_GOVERNANCE

    def _classify_risk_tier(self, scenario: Scenario) -> RiskTier:
        """EN: Context-based risk: the UK regime regulates outcomes per sector, not technologies. | ES: Riesgo segun contexto: el regimen britanico regula resultados por sector, no tecnologias."""
        if self._is_prohibited(scenario) or self._is_high_impact(scenario):
            return RiskTier.HIGH_RISK
        if self._is_generative(scenario):
            return RiskTier.SPECIFIC_TRANSPARENCY_RISK
        return RiskTier.MINIMAL_RISK

    def _calculate_metrics(self, scenario: Scenario) -> list[EvaluationMetric]:
        """EN: One metric per principle. | ES: Una metrica por principio."""
        wellbeing = max(0.0, 1.0 - float(scenario.metadata.get("toxicity_exposure_rate", 0.0)))
        robustness = (wellbeing + self._average_confidence(scenario)) / 2 if scenario.artifacts else wellbeing
        transparency = (0.6 if self._flag(scenario, "explainability_enabled") else 0.0) + (
            0.4 if self._flag(scenario, "confidence_scores_visible") else 0.0
        )
        accountability = (0.5 if self._flag(scenario, "human_in_the_loop") else 0.0) + (
            0.5 if self._flag(scenario, "provenance_verified") else 0.0
        )
        contestability = 1.0 if self._flag(scenario, "contestability_channel") or self._flag(scenario, "human_in_the_loop") else 0.0
        return [
            self._metric("Safety, Security & Robustness", robustness, 0.80, "Principle 1: reliable operation under expected conditions."),
            self._metric("Appropriate Transparency & Explainability", transparency, 0.60, "Principle 2: information proportionate to context."),
            self._metric("Fairness Gap", self._dialectal_parity_gap(scenario), 0.15, "Principle 3: no unfair discrimination across varieties.", lower_is_better=True),
            self._metric("Accountability & Governance", accountability, 0.50, "Principle 4: clear lines of responsibility over the lifecycle."),
            self._metric("Contestability & Redress", contestability, 1.0, "Principle 5: affected parties can contest harmful outcomes."),
        ]

    def _audit(self, scenario: Scenario, risk_tier: RiskTier, metrics: list[EvaluationMetric]) -> list[EthicalFinding]:
        """EN: Translate failed principles into findings. | ES: Traducir principios no superados en hallazgos."""
        severity = "HIGH" if risk_tier == RiskTier.HIGH_RISK else "MEDIUM"
        guidance = {
            "Safety, Security & Robustness": "Run adversarial and distribution-shift testing before deployment.",
            "Appropriate Transparency & Explainability": "Publish decision-level explanations and confidence indicators to users.",
            "Fairness Gap": "Rebalance training data across linguistic varieties and monitor parity post-deployment.",
            "Accountability & Governance": "Assign an accountable owner and document data lineage.",
            "Contestability & Redress": "Provide an accessible route to challenge outcomes and obtain human review.",
        }
        return [
            self._finding(f"UK Principle: {m.name}", severity, f"Score {m.score} does not meet threshold {m.threshold}.", guidance[m.name])
            for m in metrics
            if not m.passed
        ]

    def _steady_state_recommendation(self) -> str:
        """EN: Default UK recommendation. | ES: Recomendacion britanica por defecto."""
        return "Maintain alignment with sector regulator guidance (ICO, FCA, CMA, MHRA) as it evolves."
