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


class FrameworkRegion(str, Enum):
    """EN: Geographic region classification for regulatory frameworks. | ES: Clasificacion de region geografica para marcos regulatorios."""

    EUROPE = "EUROPE"
    AMERICAS = "AMERICAS"
    ASIA_PACIFIC = "ASIA_PACIFIC"
    AFRICA = "AFRICA"
    INTERNATIONAL = "INTERNATIONAL"


class BindingLevel(str, Enum):
    """EN: Legal binding level of a regulatory framework. | ES: Nivel de vinculacion legal de un marco regulatorio."""

    LEGALLY_BINDING = "LEGALLY_BINDING"
    VOLUNTARY_STANDARD = "VOLUNTARY_STANDARD"
    PROPOSED_LEGISLATION = "PROPOSED_LEGISLATION"


class AlignmentStatus(str, Enum):
    """EN: Alignment verdict for voluntary or soft-law frameworks. | ES: Veredicto de alineacion para marcos voluntarios o de soft-law."""

    FULLY_ALIGNED = "FULLY_ALIGNED"
    SUBSTANTIALLY_ALIGNED = "SUBSTANTIALLY_ALIGNED"
    PARTIALLY_ALIGNED = "PARTIALLY_ALIGNED"
    NOT_ALIGNED = "NOT_ALIGNED"


class FrameworkType(str, Enum):
    """EN: Supported ethical frameworks for algorithmic evaluation. | ES: Marcos eticos soportados para evaluacion algoritmica."""

    # EN: Europe | ES: Europa
    EU_AI_ACT = "EU_AI_ACT"
    UK_AI_GOVERNANCE = "UK_AI_GOVERNANCE"
    # EN: Americas | ES: Americas
    NIST_AI_RMF = "NIST_AI_RMF"
    BRAZIL_PL_2338 = "BRAZIL_PL_2338"
    # EN: Asia-Pacific | ES: Asia-Pacifico
    KOREA_AI_BASIC_ACT = "KOREA_AI_BASIC_ACT"
    CHINA_AI_REGULATIONS = "CHINA_AI_REGULATIONS"
    JAPAN_AI_ACT = "JAPAN_AI_ACT"
    SINGAPORE_AI_GOVERNANCE = "SINGAPORE_AI_GOVERNANCE"
    INDIA_DPDP_AI = "INDIA_DPDP_AI"
    # EN: International Standards | ES: Estandares Internacionales
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
    geographic_region: str | None = None
    geographic_source: str | None = None


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
    binding_level: BindingLevel = BindingLevel.LEGALLY_BINDING
    alignment_status: AlignmentStatus | None = None
    region: FrameworkRegion | None = None


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


class EthicalDimension(str, Enum):
    """EN: Multidimensional ethical pillars for quantitative assessment. | ES: Pilares eticos multidimensionales para evaluacion cuantitativa."""

    TRANSPARENCY = "TRANSPARENCY"
    ACCOUNTABILITY = "ACCOUNTABILITY"
    FAIRNESS = "FAIRNESS"


@dataclass(frozen=True)
class DimensionScore:
    """EN: Quantified evaluation score and impact delta for a specific ethical dimension. | ES: Puntuacion de evaluacion cuantificada y delta de impacto para una dimension etica especifica."""

    dimension: EthicalDimension
    baseline_score: float
    decision_score: float
    delta: float
    rationale: str


@dataclass(frozen=True)
class MultidimensionalMatrix:
    """EN: Unified multidimensional matrix evaluating Transparency, Accountability, and Fairness. | ES: Matriz multidimensional unificada que evalua Transparencia, Rendicion de Cuentas y Equidad."""

    transparency: DimensionScore
    accountability: DimensionScore
    fairness: DimensionScore
    overall_alignment: float


@dataclass(frozen=True)
class DecisionOption:
    """EN: Predefined decision alternative for an ethical dilemma in computational linguistics. | ES: Alternativa de decision predefinida para un dilema etico en linguistica computacional."""

    id: str
    title: str
    description: str
    strategy: str
    dimension_modifiers: dict[EthicalDimension, float]
    rationale: str


@dataclass
class CaseStudy:
    """EN: Complex computational linguistics case study presenting an ethical dilemma. | ES: Caso de estudio complejo de linguistica computacional que presenta un dilema etico."""

    id: str
    title: str
    nlp_domain: str
    dilemma: str
    context_description: str
    task_type: TaskType
    domain_category: str
    linguistic_artifacts: list[LinguisticArtifact]
    baseline_matrix: dict[EthicalDimension, float]
    decision_options: list[DecisionOption]
    regulatory_implications: dict[str, str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_scenario(self) -> Scenario:
        """EN: Convert case study to base Scenario entity for framework evaluation. | ES: Convertir caso de estudio a entidad base Scenario para evaluacion de marcos."""
        meta = dict(self.metadata)
        meta["nlp_domain"] = self.nlp_domain
        meta["dilemma"] = self.dilemma
        return Scenario(
            id=self.id,
            title=self.title,
            description=self.context_description,
            domain_category=self.domain_category,
            task_type=self.task_type,
            artifacts=self.linguistic_artifacts,
            metadata=meta,
        )


@dataclass(frozen=True)
class UserDecision:
    """EN: User decision submission addressing a case study dilemma. | ES: Envio de decision del usuario que aborda el dilema de un caso de estudio."""

    case_id: str
    selected_option_id: str
    user_rationale: str
    custom_weights: dict[str, float] | None = None


@dataclass
class DecisionImpactResult:
    """EN: Complete impact calculation of a submitted decision against the multidimensional matrix. | ES: Calculo de impacto completo de una decision enviada frente a la matriz multidimensional."""

    decision_id: str
    case_id: str
    selected_option: DecisionOption
    matrix: MultidimensionalMatrix
    framework_assessments: list[FrameworkAssessment]
    overall_risk_tier: RiskTier
    overall_compliance: ComplianceStatus
    trade_off_analysis: str
    recommendations: list[str]
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
