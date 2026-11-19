"""EN: African Union Continental Artificial Intelligence Strategy (2024) evaluator. | ES: Evaluador de la Estrategia Continental de Inteligencia Artificial de la Union Africana (2024)."""

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


class AUContinentalAIEvaluator(BaseFrameworkEvaluator):
    """EN: Evaluates alignment with the AU Continental AI Strategy emphasizing linguistic inclusion, data sovereignty and human rights. | ES: Evalua la alineacion con la Estrategia Continental de IA de la Union Africana con foco en inclusion linguistica, soberania de datos y derechos humanos."""

    binding_level = BindingLevel.VOLUNTARY_STANDARD
    region = FrameworkRegion.AFRICA

    @property
    def framework(self) -> FrameworkType:
        """EN: Return the AU Continental AI Strategy identifier. | ES: Retorna el identificador de la Estrategia Continental de IA de la UA."""
        return FrameworkType.AU_CONTINENTAL_AI

    def _classify_risk_tier(self, scenario: Scenario) -> RiskTier:
        """EN: Map scenario impact to risk tiers under AU human-rights-based governance guidance. | ES: Mapear el impacto del escenario a niveles de riesgo bajo la guia de gobernanza basada en derechos humanos de la UA."""
        if self._is_prohibited(scenario) or self._is_high_impact(scenario):
            return RiskTier.HIGH_RISK
        if self._is_generative(scenario):
            return RiskTier.SPECIFIC_TRANSPARENCY_RISK
        return RiskTier.MINIMAL_RISK

    def _calculate_metrics(self, scenario: Scenario) -> list[EvaluationMetric]:
        """EN: Linguistic equity, data sovereignty/provenance, and human-rights accountability metrics. | ES: Metricas de equidad linguistica, soberania/procedencia de datos y rendicion de cuentas en derechos humanos."""
        data_sovereignty = 1.0 if self._flag(scenario, "provenance_verified") else 0.0
        human_oversight = 1.0 if self._flag(scenario, "human_in_the_loop") else 0.0
        transparency = 1.0 if self._flag(scenario, "explainability_enabled") else 0.0
        return [
            self._metric(
                "Linguistic Inclusion Parity Gap",
                self._dialectal_parity_gap(scenario),
                0.15,
                "Equal algorithmic performance across African, vernacular, and underrepresented linguistic varieties.",
                lower_is_better=True,
            ),
            self._metric(
                "Data Sovereignty & Provenance",
                data_sovereignty,
                1.0,
                "Verifiable, lawful, and consent-respecting provenance for training and evaluation corpora.",
            ),
            self._metric(
                "Human-Centric Oversight",
                human_oversight,
                1.0,
                "Human oversight mechanisms safeguarding fundamental rights in high-impact deployments.",
            ),
            self._metric(
                "Stakeholder Transparency",
                transparency,
                1.0,
                "Clear disclosure of AI use and decision rationale to affected communities.",
            ),
        ]

    def _audit(self, scenario: Scenario, risk_tier: RiskTier, metrics: list[EvaluationMetric]) -> list[EthicalFinding]:
        """EN: Surface actionable recommendations aligned with AU Continental AI Strategy pillars. | ES: Generar recomendaciones accionables alineadas con los pilares de la Estrategia Continental de IA de la UA."""
        severity = "HIGH" if risk_tier == RiskTier.HIGH_RISK else "MEDIUM"
        fixes = {
            "Linguistic Inclusion Parity Gap": "Expand representation and disaggregated benchmarking for underrepresented dialects and African linguistic varieties.",
            "Data Sovereignty & Provenance": "Document corpus lineage and enforce regional data governance and consent controls (Malabo Convention alignment).",
            "Human-Centric Oversight": "Establish independent human review for high-impact automated decisions.",
            "Stakeholder Transparency": "Publish accessible explanations and linguistic error disclosures for affected users.",
        }
        return [
            self._finding(
                f"AU AI Strategy: {m.name}",
                severity,
                f"Score {m.score} vs. target {m.threshold}.",
                fixes[m.name],
            )
            for m in metrics
            if not m.passed
        ]

    def _steady_state_recommendation(self) -> str:
        """EN: Default AU Continental AI Strategy recommendation. | ES: Recomendacion por defecto de la Estrategia Continental de IA de la UA."""
        return "Maintain continuous linguistic-diversity monitoring and align data governance with AU Digital Transformation and Malabo Convention principles."
