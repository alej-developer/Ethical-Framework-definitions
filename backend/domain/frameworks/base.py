"""EN: Shared building blocks for regional regulatory framework evaluators. | ES: Bloques compartidos para los evaluadores de marcos regulatorios regionales."""

from abc import abstractmethod

from domain.entities import (
    AlignmentStatus,
    BindingLevel,
    ComplianceStatus,
    EthicalFinding,
    EvaluationMetric,
    FrameworkAssessment,
    FrameworkRegion,
    RiskTier,
    Scenario,
    TaskType,
)
from domain.interfaces import IEthicalEvaluator

# EN: Domain categories treated as high-impact by most risk-based regimes | ES: Categorias de dominio tratadas como de alto impacto por la mayoria de regimenes basados en riesgo
HIGH_IMPACT_DOMAINS: frozenset[str] = frozenset(
    {
        "clinical_triage",
        "healthcare",
        "recruitment",
        "employment",
        "law_enforcement",
        "critical_infrastructure",
        "education",
        "credit_scoring",
        "migration",
    }
)

# EN: Domain categories treated as prohibited or excessive risk | ES: Categorias de dominio tratadas como prohibidas o de riesgo excesivo
PROHIBITED_DOMAINS: frozenset[str] = frozenset({"social_scoring", "biometric_categorization_sensitive"})

# EN: Generative or content-producing task types | ES: Tipos de tarea generativos o productores de contenido
GENERATIVE_TASKS: frozenset[TaskType] = frozenset({TaskType.GENERATIVE_QA, TaskType.MACHINE_TRANSLATION})

_SEVERITY_ORDER: dict[str, int] = {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}


class BaseFrameworkEvaluator(IEthicalEvaluator):
    """EN: Template-method base providing metrics helpers and verdict derivation. | ES: Base de metodo plantilla que aporta utilidades de metricas y derivacion de veredictos."""

    #: EN: Legal binding level of the framework | ES: Nivel de vinculacion legal del marco
    binding_level: BindingLevel = BindingLevel.LEGALLY_BINDING
    #: EN: Geographic region of the framework | ES: Region geografica del marco
    region: FrameworkRegion = FrameworkRegion.INTERNATIONAL

    def evaluate(self, scenario: Scenario) -> FrameworkAssessment:
        """EN: Run the template pipeline: metrics, findings, verdicts and recommendations. | ES: Ejecutar la tuberia plantilla: metricas, hallazgos, veredictos y recomendaciones."""
        risk_tier = self._classify_risk_tier(scenario)
        metrics = self._calculate_metrics(scenario)
        findings = self._audit(scenario, risk_tier, metrics)
        compliance = self._derive_compliance(risk_tier, findings)
        alignment = self._derive_alignment(metrics, findings) if self.binding_level != BindingLevel.LEGALLY_BINDING else None
        recommendations = [f.recommendation for f in findings] or [self._steady_state_recommendation()]

        return FrameworkAssessment(
            framework=self.framework,
            risk_tier=risk_tier,
            compliance_status=compliance,
            metrics=metrics,
            findings=findings,
            recommendations=list(dict.fromkeys(recommendations)),
            binding_level=self.binding_level,
            alignment_status=alignment,
            region=self.region,
        )

    # EN: Hooks implemented by concrete evaluators | ES: Ganchos implementados por los evaluadores concretos

    @abstractmethod
    def _classify_risk_tier(self, scenario: Scenario) -> RiskTier:
        """EN: Map scenario to the framework's risk taxonomy. | ES: Mapear el escenario a la taxonomia de riesgo del marco."""

    @abstractmethod
    def _calculate_metrics(self, scenario: Scenario) -> list[EvaluationMetric]:
        """EN: Compute framework-specific quantitative metrics. | ES: Calcular metricas cuantitativas especificas del marco."""

    @abstractmethod
    def _audit(self, scenario: Scenario, risk_tier: RiskTier, metrics: list[EvaluationMetric]) -> list[EthicalFinding]:
        """EN: Produce findings from metrics and scenario context. | ES: Producir hallazgos a partir de metricas y contexto del escenario."""

    @abstractmethod
    def _steady_state_recommendation(self) -> str:
        """EN: Recommendation returned when no findings are detected. | ES: Recomendacion devuelta cuando no se detectan hallazgos."""

    # EN: Shared metric helpers | ES: Utilidades compartidas de metricas

    @staticmethod
    def _flag(scenario: Scenario, key: str) -> bool:
        """EN: Read a boolean flag from scenario metadata (defaults to False). | ES: Leer un indicador booleano de los metadatos del escenario (por defecto False)."""
        return bool(scenario.metadata.get(key, False))

    @staticmethod
    def _domain(scenario: Scenario) -> str:
        """EN: Normalised domain category. | ES: Categoria de dominio normalizada."""
        return scenario.domain_category.lower()

    @classmethod
    def _is_high_impact(cls, scenario: Scenario) -> bool:
        """EN: Whether the scenario falls into a high-impact domain. | ES: Si el escenario pertenece a un dominio de alto impacto."""
        return scenario.task_type == TaskType.CLINICAL_TRIAGE or cls._domain(scenario) in HIGH_IMPACT_DOMAINS

    @classmethod
    def _is_prohibited(cls, scenario: Scenario) -> bool:
        """EN: Whether the scenario falls into a prohibited domain. | ES: Si el escenario pertenece a un dominio prohibido."""
        return cls._domain(scenario) in PROHIBITED_DOMAINS

    @staticmethod
    def _is_generative(scenario: Scenario) -> bool:
        """EN: Whether the scenario produces synthetic content. | ES: Si el escenario produce contenido sintetico."""
        return scenario.task_type in GENERATIVE_TASKS

    @staticmethod
    def _dialectal_parity_gap(scenario: Scenario) -> float:
        """EN: Max accuracy gap across linguistic varieties. | ES: Brecha maxima de exactitud entre variedades linguisticas."""
        varieties = {a.dialect_or_variety for a in scenario.artifacts}
        accuracies: list[float] = []
        for variety in varieties:
            group = [a for a in scenario.artifacts if a.dialect_or_variety == variety]
            accuracies.append(sum(1 for a in group if a.observed_output == a.expected_output) / len(group))
        return round(max(accuracies) - min(accuracies), 3) if accuracies else 0.0

    @staticmethod
    def _average_confidence(scenario: Scenario) -> float:
        """EN: Mean model confidence over artifacts. | ES: Confianza media del modelo sobre los artefactos."""
        if not scenario.artifacts:
            return 0.0
        return round(sum(a.confidence_score for a in scenario.artifacts) / len(scenario.artifacts), 3)

    @staticmethod
    def _metric(name: str, score: float, threshold: float, description: str, lower_is_better: bool = False) -> EvaluationMetric:
        """EN: Build a metric deciding pass/fail against its threshold. | ES: Construir una metrica decidiendo aprobado/suspenso frente a su umbral."""
        passed = score <= threshold if lower_is_better else score >= threshold
        return EvaluationMetric(name=name, score=round(score, 3), threshold=threshold, passed=passed, description=description)

    def _finding(self, category: str, severity: str, message: str, recommendation: str) -> EthicalFinding:
        """EN: Build a finding bound to this evaluator's framework. | ES: Construir un hallazgo vinculado al marco de este evaluador."""
        return EthicalFinding(
            framework=self.framework,
            category=category,
            severity=severity,
            message=message,
            recommendation=recommendation,
        )

    # EN: Shared verdict derivation | ES: Derivacion compartida de veredictos

    def _derive_compliance(self, risk_tier: RiskTier, findings: list[EthicalFinding]) -> ComplianceStatus:
        """EN: Map risk tier and finding severities to a compliance verdict. | ES: Mapear nivel de riesgo y severidades a un veredicto de cumplimiento."""
        if risk_tier == RiskTier.UNACCEPTABLE_RISK:
            return ComplianceStatus.PROHIBITED
        severities = [f.severity for f in findings]
        if "CRITICAL" in severities or severities.count("HIGH") >= 2:
            return ComplianceStatus.NON_COMPLIANT
        if severities:
            return ComplianceStatus.PARTIALLY_COMPLIANT
        return ComplianceStatus.COMPLIANT

    @staticmethod
    def _derive_alignment(metrics: list[EvaluationMetric], findings: list[EthicalFinding]) -> AlignmentStatus:
        """EN: Alignment verdict for soft-law frameworks based on metric pass ratio. | ES: Veredicto de alineacion para marcos de soft-law segun la proporcion de metricas aprobadas."""
        if any(_SEVERITY_ORDER.get(f.severity, 0) >= 4 for f in findings):
            return AlignmentStatus.NOT_ALIGNED
        ratio = sum(1 for m in metrics if m.passed) / len(metrics) if metrics else 0.0
        if ratio >= 1.0:
            return AlignmentStatus.FULLY_ALIGNED
        if ratio >= 0.75:
            return AlignmentStatus.SUBSTANTIALLY_ALIGNED
        if ratio >= 0.4:
            return AlignmentStatus.PARTIALLY_ALIGNED
        return AlignmentStatus.NOT_ALIGNED
