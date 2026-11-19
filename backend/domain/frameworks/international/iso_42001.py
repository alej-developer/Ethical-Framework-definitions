"""EN: ISO/IEC 42001:2023 Artificial Intelligence Management System (AIMS) evaluator. | ES: Evaluador del Sistema de Gestion de Inteligencia Artificial ISO/IEC 42001:2023 (AIMS)."""

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


class ISO42001Evaluator(BaseFrameworkEvaluator):
    """EN: Certifiable international management-system standard covering AI risk assessment, impact assessment and lifecycle controls (Annex A). | ES: Estandar internacional certificable de sistema de gestion que cubre evaluacion de riesgos, impacto y controles de ciclo de vida de IA (Anexo A)."""

    binding_level = BindingLevel.VOLUNTARY_STANDARD
    region = FrameworkRegion.INTERNATIONAL

    @property
    def framework(self) -> FrameworkType:
        """EN: Return the ISO/IEC 42001 identifier. | ES: Retorna el identificador de ISO/IEC 42001."""
        return FrameworkType.ISO_IEC_42001

    def _classify_risk_tier(self, scenario: Scenario) -> RiskTier:
        """EN: Map scenario impact to risk tiers for Clause 6.1.2 / 6.1.4 scoping. | ES: Mapear el impacto del escenario a niveles de riesgo para el alcance de Clausulas 6.1.2 / 6.1.4."""
        if self._is_prohibited(scenario) or self._is_high_impact(scenario):
            return RiskTier.HIGH_RISK
        if self._is_generative(scenario):
            return RiskTier.SPECIFIC_TRANSPARENCY_RISK
        return RiskTier.MINIMAL_RISK

    def _calculate_metrics(self, scenario: Scenario) -> list[EvaluationMetric]:
        """EN: AIMS controls from Clauses 6 & 8 and Annex A (data, impact assessment, human oversight, transparency). | ES: Controles AIMS de Clausulas 6 y 8 y Anexo A (datos, evaluacion de impacto, supervision humana, transparencia)."""
        data_lifecycle = 1.0 if self._flag(scenario, "provenance_verified") else 0.0
        oversight = 1.0 if self._flag(scenario, "human_in_the_loop") else 0.0
        documentation = (0.6 if self._flag(scenario, "explainability_enabled") else 0.0) + (
            0.4 if self._flag(scenario, "confidence_scores_visible") else 0.0
        )
        return [
            self._metric(
                "AIMS Data Quality & Provenance (Annex A.7)",
                data_lifecycle,
                1.0,
                "Documented data acquisition, provenance, and quality controls across the AI lifecycle.",
            ),
            self._metric(
                "AI System Impact & Fairness Gap (Clause 6.1.4)",
                self._dialectal_parity_gap(scenario),
                0.15,
                "Assessment of consequences for individuals and groups, including linguistic fairness.",
                lower_is_better=True,
            ),
            self._metric(
                "Human Oversight & Accountability (Annex A.3 / A.9)",
                oversight,
                1.0,
                "Defined roles, responsibilities, and human-in-the-loop checkpoints for high-impact use.",
            ),
            self._metric(
                "Information for Interested Parties (Annex A.8)",
                documentation,
                0.60,
                "Clear system documentation, intended use boundaries, and uncertainty disclosure.",
            ),
        ]

    def _audit(self, scenario: Scenario, risk_tier: RiskTier, metrics: list[EvaluationMetric]) -> list[EthicalFinding]:
        """EN: Convert unmet AIMS controls into corrective actions (Clause 10.2). | ES: Convertir controles AIMS no cumplidos en acciones correctivas (Clausula 10.2)."""
        severity = "HIGH" if risk_tier == RiskTier.HIGH_RISK else "MEDIUM"
        fixes = {
            "AIMS Data Quality & Provenance (Annex A.7)": "Implement Annex A.7 data lineage records, consent verification, and dataset quality gates.",
            "AI System Impact & Fairness Gap (Clause 6.1.4)": "Run a formal AI System Impact Assessment (AIIA) and remediate dialectal performance gaps.",
            "Human Oversight & Accountability (Annex A.3 / A.9)": "Assign accountable AIMS owners and enforce human-in-the-loop verification for consequential outputs.",
            "Information for Interested Parties (Annex A.8)": "Publish Annex A.8 system documentation, explainability artefacts, and confidence indicators.",
        }
        return [
            self._finding(
                f"ISO/IEC 42001: {m.name}",
                severity,
                f"Score {m.score} vs. target {m.threshold}.",
                fixes[m.name],
            )
            for m in metrics
            if not m.passed
        ]

    def _steady_state_recommendation(self) -> str:
        """EN: Default ISO/IEC 42001 recommendation. | ES: Recomendacion por defecto de ISO/IEC 42001."""
        return "Schedule periodic internal AIMS audits (Clause 9.2) and management reviews to sustain ISO/IEC 42001 readiness."
