"""EN: China generative AI, deep synthesis and AI content labeling rules evaluator. | ES: Evaluador de las normas chinas de IA generativa, sintesis profunda y etiquetado de contenido de IA."""

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


class ChinaAIRegulationsEvaluator(BaseFrameworkEvaluator):
    """EN: Interim Measures for Generative AI Services (2023), Deep Synthesis Provisions (2023) and AI Content Labeling Measures (2025). | ES: Medidas Provisionales para Servicios de IA Generativa (2023), Disposiciones de Sintesis Profunda (2023) y Medidas de Etiquetado (2025)."""

    binding_level = BindingLevel.LEGALLY_BINDING
    region = FrameworkRegion.ASIA_PACIFIC

    @property
    def framework(self) -> FrameworkType:
        """EN: Return the China AI regulations identifier. | ES: Retorna el identificador de las regulaciones chinas de IA."""
        return FrameworkType.CHINA_AI_REGULATIONS

    def _classify_risk_tier(self, scenario: Scenario) -> RiskTier:
        """EN: Generative services carry the core obligations. | ES: Los servicios generativos concentran las obligaciones principales."""
        if self._is_prohibited(scenario):
            return RiskTier.UNACCEPTABLE_RISK
        if self._is_high_impact(scenario):
            return RiskTier.HIGH_RISK
        if self._is_generative(scenario):
            return RiskTier.SPECIFIC_TRANSPARENCY_RISK
        return RiskTier.MINIMAL_RISK

    def _calculate_metrics(self, scenario: Scenario) -> list[EvaluationMetric]:
        """EN: Labeling, lawful training data, content safety and non-discrimination. | ES: Etiquetado, datos de entrenamiento licitos, seguridad del contenido y no discriminacion."""
        harm = float(scenario.metadata.get("toxicity_exposure_rate", 0.0))
        return [
            self._metric("Synthetic Content Labeling", 1.0 if self._flag(scenario, "content_labeling_enabled") else 0.0, 1.0, "Explicit and implicit labels on AI-generated content."),
            self._metric("Lawful Training Data", 1.0 if self._flag(scenario, "provenance_verified") else 0.0, 1.0, "Training data from lawful sources respecting IP and personal information."),
            self._metric("Content Safety", max(0.0, 1.0 - harm), 0.95, "Generated content must not contain illegal or harmful information."),
            self._metric("Non-Discrimination Gap", self._dialectal_parity_gap(scenario), 0.15, "Measures to prevent discrimination by ethnicity, region, etc.", lower_is_better=True),
        ]

    def _audit(self, scenario: Scenario, risk_tier: RiskTier, metrics: list[EvaluationMetric]) -> list[EthicalFinding]:
        """EN: Labeling applies only to generative output. | ES: El etiquetado solo aplica a salidas generativas."""
        if risk_tier == RiskTier.UNACCEPTABLE_RISK:
            return [self._finding("Prohibited Use", "CRITICAL", f"Domain '{scenario.domain_category}' is not permissible.", "Cease provision of the service.")]
        generative = self._is_generative(scenario)
        fixes = {
            "Synthetic Content Labeling": "Add visible labels and metadata watermarks to generated content.",
            "Lawful Training Data": "Audit training data sources and obtain consent or licences.",
            "Content Safety": "Strengthen content filtering and complaint handling mechanisms.",
            "Non-Discrimination Gap": "Adjust data and models to remove regional or ethnic disparities.",
        }
        findings: list[EthicalFinding] = []
        for m in metrics:
            if m.passed or (m.name == "Synthetic Content Labeling" and not generative):
                continue
            severity = "HIGH" if m.name in ("Content Safety", "Lawful Training Data") else "MEDIUM"
            findings.append(self._finding(f"CAC Rules: {m.name}", severity, f"Score {m.score} vs. {m.threshold}.", fixes[m.name]))
        return findings

    def _steady_state_recommendation(self) -> str:
        """EN: Default China recommendation. | ES: Recomendacion china por defecto."""
        return "Complete algorithm filing with the CAC and keep security assessments up to date."
