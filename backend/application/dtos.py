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
