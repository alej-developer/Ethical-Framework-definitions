"""EN: India Digital Personal Data Protection Act 2023 evaluator applied to AI processing. | ES: Evaluador de la Ley de Proteccion de Datos Personales Digitales de India 2023 aplicada al tratamiento por IA."""

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


class IndiaDPDPAIEvaluator(BaseFrameworkEvaluator):
    """EN: Binding data-protection duties (consent, purpose limitation, accuracy, data principal rights) for AI pipelines. | ES: Deberes vinculantes de proteccion de datos (consentimiento, limitacion de finalidad, exactitud, derechos del titular) para tuberias de IA."""

    binding_level = BindingLevel.LEGALLY_BINDING
    region = FrameworkRegion.ASIA_PACIFIC

    @property
    def framework(self) -> FrameworkType:
        """EN: Return the India DPDP identifier. | ES: Retorna el identificador DPDP de India."""
        return FrameworkType.INDIA_DPDP_AI

    def _classify_risk_tier(self, scenario: Scenario) -> RiskTier:
        """EN: DPDP is not risk-tiered; personal-data-heavy decisions are treated as high risk. | ES: La DPDP no clasifica por riesgo; las decisiones con muchos datos personales se tratan como alto riesgo."""
        if self._is_prohibited(scenario) or self._is_high_impact(scenario):
            return RiskTier.HIGH_RISK
        if self._is_generative(scenario):
            return RiskTier.SPECIFIC_TRANSPARENCY_RISK
        return RiskTier.MINIMAL_RISK

    def _calculate_metrics(self, scenario: Scenario) -> list[EvaluationMetric]:
        """EN: Data fiduciary obligations. | ES: Obligaciones del fiduciario de datos."""
        consent = 1.0 if self._flag(scenario, "consent_verified") or self._flag(scenario, "provenance_verified") else 0.0
        rights = 1.0 if self._flag(scenario, "contestability_channel") or self._flag(scenario, "human_in_the_loop") else 0.0
        return [
            self._metric("Lawful Consent & Notice", consent, 1.0, "Section 6: free, specific, informed consent with notice."),
            self._metric("Data Accuracy", self._average_confidence(scenario), 0.75, "Section 8(3): completeness and accuracy when data drives decisions."),
            self._metric("Grievance & Correction Rights", rights, 1.0, "Sections 12-13: correction, erasure and grievance redressal."),
        ]

    def _audit(self, scenario: Scenario, risk_tier: RiskTier, metrics: list[EvaluationMetric]) -> list[EthicalFinding]:
        """EN: Consent failures are critical; others scale with risk. | ES: Los fallos de consentimiento son criticos; el resto escala con el riesgo."""
        high = risk_tier == RiskTier.HIGH_RISK
        fixes = {
            "Lawful Consent & Notice": "Collect verifiable consent and issue itemised notices before processing.",
            "Data Accuracy": "Validate data quality where outputs affect data principals.",
            "Grievance & Correction Rights": "Set up grievance redressal and correction workflows.",
        }
        findings: list[EthicalFinding] = []
        for m in metrics:
            if m.passed:
                continue
            severity = "CRITICAL" if m.name == "Lawful Consent & Notice" else ("HIGH" if high else "MEDIUM")
            findings.append(self._finding(f"DPDP Act: {m.name}", severity, f"Score {m.score} vs. {m.threshold}.", fixes[m.name]))
        return findings

    def _steady_state_recommendation(self) -> str:
        """EN: Default India recommendation. | ES: Recomendacion india por defecto."""
        return "Align with the DPDP Rules and the national AI governance guidelines as they are phased in."
