"""EN: Core domain entities and value objects for AI ethics evaluation. | ES: Entidades centrales de dominio y objetos de valor para la evaluacion etica de IA."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any


class RiskTier(str, Enum):
    """EN: Risk tier categorization based on regulatory taxonomies. | ES: Categorizacion de nivel de riesgo basada en taxonomias regulatorias."""

    UNACCEPTABLE_RISK = "UNACCEPTABLE_RISK"
    HIGH_RISK = "HIGH_RISK"
    SPECIFIC_TRANSPARENCY_RISK = "SPECIFIC_TRANSPARENCY_RISK"
    MINIMAL_RISK = "MINIMAL_RISK"


class ComplianceStatus(str, Enum):
    """EN: Evaluation compliance verdict. | ES: Veredicto de cumplimiento de la evaluacion."""

    COMPLIANT = "COMPLIANT"
    PARTIALLY_COMPLIANT = "PARTIALLY_COMPLIANT"
    NON_COMPLIANT = "NON_COMPLIANT"
    PROHIBITED = "PROHIBITED"


class TaskType(str, Enum):
    """EN: Computational linguistics task taxonomy. | ES: Taxonomia de tareas de linguistica computacional."""

    TEXT_CLASSIFICATION = "TEXT_CLASSIFICATION"
    MACHINE_TRANSLATION = "MACHINE_TRANSLATION"
    GENERATIVE_QA = "GENERATIVE_QA"
    CLINICAL_TRIAGE = "CLINICAL_TRIAGE"
    CONTENT_MODERATION = "CONTENT_MODERATION"


class FrameworkType(str, Enum):
    """EN: Supported ethical frameworks for algorithmic evaluation. | ES: Marcos eticos soportados para evaluacion algoritmica."""

    EU_AI_ACT = "EU_AI_ACT"
    IEEE_7000_SERIES = "IEEE_7000_SERIES"


@dataclass(frozen=True)
class EvaluationMetric:
    """EN: Quantified evaluation metric for algorithmic behaviour. | ES: Metrica cuantificada de evaluacion para el comportamiento algoritmico."""

    name: str
    score: float
    threshold: float
    passed: bool
    description: str


@dataclass(frozen=True)
class EthicalFinding:
    """EN: Specific finding or violation detected during evaluation. | ES: Hallazgo o infraccion especifica detectada durante la evaluacion."""

    framework: FrameworkType
    category: str
    severity: str
    message: str
    recommendation: str


@dataclass(frozen=True)
class LinguisticArtifact:
    """EN: Computational linguistics sample evaluated within a scenario. | ES: Muestra de linguistica computacional evaluada dentro de un escenario."""

    text_sample: str
    dialect_or_variety: str
    protected_attribute: str
    expected_output: str
    observed_output: str
    confidence_score: float


@dataclass
class Scenario:
    """EN: Computational linguistics scenario subjected to ethical audit. | ES: Escenario de linguistica computacional sometido a auditoria etica."""

    id: str
    title: str
    description: str
    domain_category: str
    task_type: TaskType
    artifacts: list[LinguisticArtifact]
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class FrameworkAssessment:
    """EN: Evaluation outcome under a single ethical framework. | ES: Resultado de evaluacion bajo un unico marco etico."""

    framework: FrameworkType
    risk_tier: RiskTier
    compliance_status: ComplianceStatus
    metrics: list[EvaluationMetric]
    findings: list[EthicalFinding]
    recommendations: list[str]


@dataclass
class EthicalAssessment:
    """EN: Consolidated ethical assessment across multiple frameworks. | ES: Evaluacion etica consolidada a traves de multiples marcos."""

    id: str
    scenario_id: str
    created_at: datetime
    framework_assessments: list[FrameworkAssessment]
    overall_risk_tier: RiskTier
    overall_compliance: ComplianceStatus
    executive_summary: str

    @classmethod
    def create(
        cls,
        assessment_id: str,
        scenario_id: str,
        framework_assessments: list[FrameworkAssessment],
        executive_summary: str,
    ) -> "EthicalAssessment":
        """EN: Factory method computing consolidated risk and compliance. | ES: Metodo de fabrica que calcula el riesgo y cumplimiento consolidados."""
        # EN: Determine highest risk tier among all frameworks | ES: Determinar el nivel de riesgo mas alto entre todos los marcos
        risk_priority = {
            RiskTier.UNACCEPTABLE_RISK: 4,
            RiskTier.HIGH_RISK: 3,
            RiskTier.SPECIFIC_TRANSPARENCY_RISK: 2,
            RiskTier.MINIMAL_RISK: 1,
        }

        overall_risk = RiskTier.MINIMAL_RISK
        current_max_prio = 0
        for fa in framework_assessments:
            prio = risk_priority.get(fa.risk_tier, 0)
            if prio > current_max_prio:
                current_max_prio = prio
                overall_risk = fa.risk_tier

        # EN: Determine overall compliance status | ES: Determinar el estado general de cumplimiento
        compliance_priority = {
            ComplianceStatus.PROHIBITED: 4,
            ComplianceStatus.NON_COMPLIANT: 3,
            ComplianceStatus.PARTIALLY_COMPLIANT: 2,
            ComplianceStatus.COMPLIANT: 1,
        }

        overall_compliance = ComplianceStatus.COMPLIANT
        current_comp_prio = 0
        for fa in framework_assessments:
            comp_prio = compliance_priority.get(fa.compliance_status, 0)
            if comp_prio > current_comp_prio:
                current_comp_prio = comp_prio
                overall_compliance = fa.compliance_status

        return cls(
            id=assessment_id,
            scenario_id=scenario_id,
            created_at=datetime.now(UTC),
            framework_assessments=framework_assessments,
            overall_risk_tier=overall_risk,
            overall_compliance=overall_compliance,
            executive_summary=executive_summary,
        )
