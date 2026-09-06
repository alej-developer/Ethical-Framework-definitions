"""EN: Data Transfer Objects (DTOs) for application boundary separation. | ES: Objetos de Transferencia de Datos (DTOs) para la separacion de fronteras de la aplicacion."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class EvaluationMetricDTO(BaseModel):
    """EN: DTO representation of an individual quantified metric. | ES: Representacion DTO de una metrica cuantificada individual."""

    model_config = ConfigDict(from_attributes=True)

    name: str
    score: float
    threshold: float
    passed: bool
    description: str


class EthicalFindingDTO(BaseModel):
    """EN: DTO representing an identified ethical defect or finding. | ES: DTO que representa un defecto etico o hallazgo identificado."""

    model_config = ConfigDict(from_attributes=True)

    framework: str
    category: str
    severity: str
    message: str
    recommendation: str


class FrameworkAssessmentDTO(BaseModel):
    """EN: DTO representing assessment under a specific ethical framework. | ES: DTO que representa la evaluacion bajo un marco etico especifico."""

    model_config = ConfigDict(from_attributes=True)

    framework: str
    risk_tier: str
    compliance_status: str
    metrics: list[EvaluationMetricDTO]
    findings: list[EthicalFindingDTO]
    recommendations: list[str]


class EthicalAssessmentDTO(BaseModel):
    """EN: DTO representing the aggregate multi-framework assessment. | ES: DTO que representa la evaluacion consolidada de multiples marcos."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    scenario_id: str
    created_at: datetime
    framework_assessments: list[FrameworkAssessmentDTO]
    overall_risk_tier: str
    overall_compliance: str
    executive_summary: str


class LinguisticArtifactDTO(BaseModel):
    """EN: DTO representing a linguistic test sample artifact. | ES: DTO que representa un artefacto de muestra de prueba linguistica."""

    model_config = ConfigDict(from_attributes=True)

    text_sample: str
    dialect_or_variety: str
    protected_attribute: str
    expected_output: str
    observed_output: str
    confidence_score: float


class ScenarioDTO(BaseModel):
    """EN: DTO representing a computational linguistics scenario. | ES: DTO que representa un escenario de linguistica computacional."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    description: str
    domain_category: str
    task_type: str
    artifacts: list[LinguisticArtifactDTO]
    metadata: dict[str, Any]


class EvaluateScenarioRequest(BaseModel):
    """EN: DTO request schema for triggering scenario evaluation. | ES: Esquema DTO de solicitud para activar la evaluacion de escenarios."""

    scenario_id: str = Field(..., description="Unique scenario identifier")
    frameworks: list[str] = Field(
        default_factory=lambda: ["EU_AI_ACT", "IEEE_7000_SERIES"],
        description="Target frameworks for evaluation",
    )


class CreateScenarioRequest(BaseModel):
    """EN: DTO request schema for creating a new linguistic scenario. | ES: Esquema DTO de solicitud para crear un nuevo escenario linguistico."""

    title: str
    description: str
    domain_category: str
    task_type: str
    artifacts: list[LinguisticArtifactDTO]
    metadata: dict[str, Any] = Field(default_factory=dict)


# EN: DTOs for Complex NLP Case Studies and Decisions | ES: DTOs para Casos de Estudio Complejos de NLP y Decisiones


class DecisionOptionDTO(BaseModel):
    """EN: DTO representing an ethical intervention choice for a case study. | ES: DTO que representa una opcion de intervencion etica para un caso de estudio."""

    model_config = ConfigDict(from_attributes=True)

    id: str = Field(..., description="Unique identifier for the decision option")
    title: str = Field(..., description="Title of the decision option")
    description: str = Field(..., description="Detailed description of the intervention strategy")
    strategy: str = Field(..., description="High-level engineering or governance strategy")
    dimension_modifiers: dict[str, float] = Field(
        ..., description="Modifiers applied to Transparency, Accountability, and Fairness"
    )
    rationale: str = Field(..., description="Ethical rationale justifying the modifier values")


class CaseStudySummaryDTO(BaseModel):
    """EN: Summary DTO for displaying case study overviews in listings. | ES: DTO de resumen para mostrar vistas generales de casos de estudio en listados."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    nlp_domain: str
    dilemma: str
    domain_category: str
    task_type: str
    available_options_count: int


class CaseStudyDTO(BaseModel):
    """EN: Comprehensive DTO detailing an NLP ethical case study and its decision space. | ES: DTO integral que detalla un caso de estudio etico de NLP y su espacio de decision."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    nlp_domain: str
    dilemma: str
    context_description: str
    task_type: str
    domain_category: str
    linguistic_artifacts: list[LinguisticArtifactDTO]
    baseline_matrix: dict[str, float]
    decision_options: list[DecisionOptionDTO]
    regulatory_implications: dict[str, str]
    metadata: dict[str, Any]


class SubmitDecisionRequest(BaseModel):
    """EN: Request payload for submitting an ethical decision for a case study. | ES: Carga de solicitud para enviar una decision etica para un caso de estudio."""

    case_id: str = Field(..., min_length=1, description="Identifier of the target case study")
    selected_option_id: str = Field(..., min_length=1, description="Identifier of the chosen decision alternative")
    user_rationale: str = Field(..., min_length=10, description="User justification for the selected intervention")
    custom_weights: dict[str, float] | None = Field(
        default=None, description="Optional custom dimension weights for matrix evaluation"
    )
    frameworks: list[str] = Field(
        default_factory=lambda: ["EU_AI_ACT", "IEEE_7000_SERIES"],
        description="International frameworks to cross-evaluate against",
    )


class DimensionScoreDTO(BaseModel):
    """EN: DTO reflecting evaluated score and impact delta for a single dimension. | ES: DTO que refleja la puntuacion evaluada y el delta de impacto para una sola dimension."""

    model_config = ConfigDict(from_attributes=True)

    dimension: str
    baseline_score: float
    decision_score: float
    delta: float
    rationale: str


class MultidimensionalMatrixDTO(BaseModel):
    """EN: DTO packaging the three core ethical dimensions and overall alignment score. | ES: DTO que empaqueta las tres dimensiones eticas centrales y la puntuacion de alineacion general."""

    model_config = ConfigDict(from_attributes=True)

    transparency: DimensionScoreDTO
    accountability: DimensionScoreDTO
    fairness: DimensionScoreDTO
    overall_alignment: float


class DecisionImpactResponseDTO(BaseModel):
    """EN: Complete evaluation response reporting multidimensional impact and regulatory audit. | ES: Respuesta de evaluacion completa que informa el impacto multidimensional y la auditoria regulatoria."""

    model_config = ConfigDict(from_attributes=True)

    decision_id: str
    case_id: str
    selected_option: DecisionOptionDTO
    matrix: MultidimensionalMatrixDTO
    framework_assessments: list[FrameworkAssessmentDTO]
    overall_risk_tier: str
    overall_compliance: str
    trade_off_analysis: str
    recommendations: list[str]
    created_at: datetime


# EN: Standardized Error Envelope DTOs | ES: DTOs de Envoltorio de Error Estandarizado


class StandardErrorDetailDTO(BaseModel):
    """EN: Standardized error detail structure returned across all failed HTTP requests. | ES: Estructura de detalle de error estandarizada retornada en todas las solicitudes HTTP fallidas."""

    code: str = Field(..., description="Machine-readable error classification code")
    message: str = Field(..., description="Human-readable description of the error")
    status_code: int = Field(..., description="HTTP status code")
    details: dict[str, Any] | list[Any] | None = Field(
        default=None, description="Structured contextual diagnostics or validation failure items"
    )
    timestamp: str = Field(..., description="ISO 8601 UTC timestamp of error occurrence")


class StandardErrorResponseDTO(BaseModel):
    """EN: Standardized envelope containing error diagnostics. | ES: Envoltorio estandarizado que contiene diagnosticos de error."""

    error: StandardErrorDetailDTO
