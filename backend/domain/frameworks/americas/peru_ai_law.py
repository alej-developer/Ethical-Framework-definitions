"""EN: Peru Law No. 31814 promoting the use of Artificial Intelligence (2023) evaluator. | ES: Evaluador de la Ley N. 31814 de Peru que promueve el uso de la Inteligencia Artificial (2023)."""

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


class PeruAILaw31814Evaluator(BaseFrameworkEvaluator):
    """EN: Legally binding national AI framework in Latin America grounded in risk-based governance, human supervision and fundamental rights. | ES: Marco legal nacional vinculante de IA en Latinoamerica basado en gestion de riesgos, supervision humana y derechos fundamentales."""

    binding_level = BindingLevel.LEGALLY_BINDING
    region = FrameworkRegion.AMERICAS

    @property
    def framework(self) -> FrameworkType:
        """EN: Return the Peru Law 31814 identifier. | ES: Retorna el identificador de la Ley 31814 de Peru."""
        return FrameworkType.PERU_AI_LAW_31814

    def _classify_risk_tier(self, scenario: Scenario) -> RiskTier:
        """EN: Risk-based classification aligned with Law 31814 and its implementing regulation. | ES: Clasificacion basada en riesgo alineada con la Ley 31814 y su reglamento."""
        if self._is_prohibited(scenario):
            return RiskTier.UNACCEPTABLE_RISK
        if self._is_high_impact(scenario):
            return RiskTier.HIGH_RISK
        if self._is_generative(scenario):
            return RiskTier.SPECIFIC_TRANSPARENCY_RISK
        return RiskTier.MINIMAL_RISK

    def _calculate_metrics(self, scenario: Scenario) -> list[EvaluationMetric]:
        """EN: Core principles of Law 31814: risk-based security, transparency, human supervision and non-discrimination. | ES: Principios rectores de la Ley 31814: seguridad basada en riesgos, transparencia, supervision humana y no discriminacion."""
        transparency = 1.0 if self._flag(scenario, "explainability_enabled") else 0.0
        human_supervision = 1.0 if self._flag(scenario, "human_in_the_loop") else 0.0
        provenance = 1.0 if self._flag(scenario, "provenance_verified") else 0.0
        return [
            self._metric(
                "Fundamental Rights & Non-Discrimination Gap",
                self._dialectal_parity_gap(scenario),
                0.15,
                "AI systems must safeguard human dignity and prevent arbitrary discrimination.",
                lower_is_better=True,
            ),
            self._metric(
                "Human Supervision & Accountability",
                human_supervision,
                1.0,
                "Mandatory human oversight for systems impacting legal, employment, or clinical rights.",
            ),
            self._metric(
                "Transparency & Citizen Notice",
                transparency,
                1.0,
                "Clear information to affected citizens on AI criteria and outcomes.",
            ),
            self._metric(
                "Data Quality & Privacy Governance",
                provenance,
                1.0,
                "Lawful data sourcing aligned with national personal data protection standards.",
            ),
        ]

    def _audit(self, scenario: Scenario, risk_tier: RiskTier, metrics: list[EvaluationMetric]) -> list[EthicalFinding]:
        """EN: Audit against Peru Law 31814 principles and risk tiers. | ES: Auditar frente a los principios y niveles de riesgo de la Ley 31814 de Peru."""
        if risk_tier == RiskTier.UNACCEPTABLE_RISK:
            return [
                self._finding(
                    "Ley 31814: Prohibited Risk",
                    "CRITICAL",
                    f"Domain '{scenario.domain_category}' contravenes fundamental rights protections under Law 31814.",
                    "Halt deployment; systems causing unacceptable harm to fundamental rights are barred.",
                )
            ]
        severity = "HIGH" if risk_tier == RiskTier.HIGH_RISK else "MEDIUM"
        fixes = {
            "Fundamental Rights & Non-Discrimination Gap": "Remediate linguistic and demographic accuracy disparities prior to deployment.",
            "Human Supervision & Accountability": "Assign designated human oversight and accountability roles for high-risk decisions.",
            "Transparency & Citizen Notice": "Inform citizens when interacting with AI and provide accessible decision explanations.",
            "Data Quality & Privacy Governance": "Verify dataset provenance and personal data protection compliance.",
        }
        return [
            self._finding(
                f"Peru Law 31814: {m.name}",
                severity,
                f"Score {m.score} vs. threshold {m.threshold}.",
                fixes[m.name],
            )
            for m in metrics
            if not m.passed
        ]

    def _steady_state_recommendation(self) -> str:
        """EN: Default Peru Law 31814 recommendation. | ES: Recomendacion por defecto de la Ley 31814 de Peru."""
        return "Maintain risk-based governance records aligned with the Secretariat of Government and Digital Transformation (SGTD) guidance."
