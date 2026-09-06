"""EN: FastAPI route definitions for scenarios, ethical evaluations, and health endpoints. | ES: Definiciones de rutas FastAPI para escenarios, evaluaciones eticas y puntos finales de salud."""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status

from application.dtos import (
    EthicalAssessmentDTO,
    EvaluateScenarioRequest,
    ScenarioDTO,
)
from application.evaluators.composite_evaluator import CompositeEvaluator
from application.use_cases import (
    EvaluateScenarioUseCase,
    GetScenarioUseCase,
    ListScenariosUseCase,
)
from domain.exceptions import ScenarioNotFoundError, UnsupportedFrameworkError
from domain.frameworks.eu_ai_act import EUAIActEvaluator
from domain.frameworks.ieee_standards import IEEEStandardsEvaluator
from infrastructure.repositories.in_memory_repository import (
    InMemoryAssessmentRepository,
    InMemoryScenarioRepository,
)

router = APIRouter(prefix="/api/v1", tags=["AI Ethics Simulator"])

# EN: Singleton repository instances for state preservation during lifecycle | ES: Instancias unicas de repositorio para preservacion de estado durante el ciclo de vida
_scenario_repo = InMemoryScenarioRepository()
_assessment_repo = InMemoryAssessmentRepository()
_composite_evaluator = CompositeEvaluator(evaluators=[EUAIActEvaluator(), IEEEStandardsEvaluator()])


def get_list_scenarios_use_case() -> ListScenariosUseCase:
    """EN: Factory for list scenarios use case. | ES: Fabrica para el caso de uso de listar escenarios."""
    return ListScenariosUseCase(_scenario_repo)


def get_scenario_use_case() -> GetScenarioUseCase:
    """EN: Factory for get scenario use case. | ES: Fabrica para el caso de uso de obtener escenario."""
    return GetScenarioUseCase(_scenario_repo)


def get_evaluate_scenario_use_case() -> EvaluateScenarioUseCase:
    """EN: Factory for evaluate scenario use case. | ES: Fabrica para el caso de uso de evaluar escenario."""
    return EvaluateScenarioUseCase(
        scenario_repository=_scenario_repo,
        assessment_repository=_assessment_repo,
        composite_evaluator=_composite_evaluator,
    )


@router.get("/health", status_code=status.HTTP_200_OK)
def health_check() -> dict[str, str]:
    """EN: Health check probe verifying service responsiveness. | ES: Sondeo de verificacion de salud que valida la capacidad de respuesta del servicio."""
    return {
        "status": "healthy",
        "service": "ai-ethics-simulator-backend",
        "architecture": "Clean Architecture / SOLID",
    }


@router.get("/frameworks", status_code=status.HTTP_200_OK)
def list_frameworks() -> list[dict[str, Any]]:
    """EN: Return metadata and descriptions for supported ethical evaluation frameworks. | ES: Retornar metadatos y descripciones para los marcos de evaluacion etica soportados."""
    return [
        {
            "id": "EU_AI_ACT",
            "name": "EU Artificial Intelligence Act (Regulation EU 2024/1689)",
            "jurisdiction": "European Union",
            "focus_areas": [
                "Prohibited AI practices",
                "High-risk computational linguistics (Annex III)",
                "Data governance & dialectal non-discrimination (Article 10)",
                "Linguistic transparency & watermarking (Article 50)",
            ],
        },
        {
            "id": "IEEE_7000_SERIES",
            "name": "IEEE 7000-2021 and IEEE 7001-2021 Standards",
            "jurisdiction": "International",
            "focus_areas": [
                "Ethical value-driven system design",
                "Stakeholder well-being and harm avoidance",
                "Multi-tiered algorithmic transparency",
                "Procedural fairness across demographic dialects",
            ],
        },
    ]


@router.get("/scenarios", response_model=list[ScenarioDTO], status_code=status.HTTP_200_OK)
def get_scenarios(
    use_case: Annotated[ListScenariosUseCase, Depends(get_list_scenarios_use_case)],
) -> list[ScenarioDTO]:
    """EN: Retrieve all registered computational linguistics scenarios. | ES: Recuperar todos los escenarios de linguistica computacional registrados."""
    return use_case.execute()


@router.get("/scenarios/{scenario_id}", response_model=ScenarioDTO, status_code=status.HTTP_200_OK)
def get_scenario(
    scenario_id: str,
    use_case: Annotated[GetScenarioUseCase, Depends(get_scenario_use_case)],
) -> ScenarioDTO:
    """EN: Retrieve a specific scenario by its unique identifier. | ES: Recuperar un escenario especifico por su identificador unico."""
    try:
        return use_case.execute(scenario_id)
    except ScenarioNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.post("/evaluations", response_model=EthicalAssessmentDTO, status_code=status.HTTP_201_CREATED)
def evaluate_scenario(
    request: EvaluateScenarioRequest,
    use_case: Annotated[EvaluateScenarioUseCase, Depends(get_evaluate_scenario_use_case)],
) -> EthicalAssessmentDTO:
    """EN: Execute ethical evaluation on a specified scenario across chosen frameworks. | ES: Ejecutar evaluacion etica sobre un escenario especificado a traves de los marcos elegidos."""
    try:
        return use_case.execute(request)
    except ScenarioNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except UnsupportedFrameworkError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
