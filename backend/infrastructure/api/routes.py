"""EN: FastAPI route definitions for case studies, decisions, evaluations, and health endpoints. | ES: Definiciones de rutas FastAPI para casos de estudio, decisiones, evaluaciones y puntos finales de salud."""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status

from application.dtos import (
    CaseStudyDTO,
    CaseStudySummaryDTO,
    DecisionImpactResponseDTO,
    EthicalAssessmentDTO,
    EvaluateScenarioRequest,
    ScenarioDTO,
    SubmitDecisionRequest,
)
from application.evaluators.composite_evaluator import CompositeEvaluator
from application.evaluators.matrix_evaluator import MatrixEvaluator
from application.use_cases import (
    EvaluateScenarioUseCase,
    GetCaseStudyUseCase,
    GetDecisionImpactUseCase,
    GetScenarioUseCase,
    ListCaseStudiesUseCase,
    ListScenariosUseCase,
    SubmitDecisionUseCase,
)
from domain.frameworks.eu_ai_act import EUAIActEvaluator
from domain.frameworks.ieee_standards import IEEEStandardsEvaluator
from infrastructure.repositories.in_memory_repository import (
    InMemoryAssessmentRepository,
    InMemoryCaseStudyRepository,
    InMemoryDecisionImpactRepository,
    InMemoryScenarioRepository,
)

router = APIRouter(prefix="/api/v1", tags=["AI Ethics Simulator"])

# EN: Singleton persistence and evaluator services for dependency injection | ES: Servicios de evaluacion y persistencia unicos para inyeccion de dependencias
_case_study_repo = InMemoryCaseStudyRepository()
_scenario_repo = InMemoryScenarioRepository(_case_study_repo)
_assessment_repo = InMemoryAssessmentRepository()
_decision_impact_repo = InMemoryDecisionImpactRepository()
_matrix_evaluator = MatrixEvaluator()
_composite_evaluator = CompositeEvaluator(evaluators=[EUAIActEvaluator(), IEEEStandardsEvaluator()])


# EN: Dependency provider functions | ES: Funciones proveedoras de dependencias


def get_list_case_studies_use_case() -> ListCaseStudiesUseCase:
    """EN: Dependency provider for ListCaseStudiesUseCase. | ES: Proveedor de dependencia para ListCaseStudiesUseCase."""
    return ListCaseStudiesUseCase(_case_study_repo)


def get_case_study_use_case() -> GetCaseStudyUseCase:
    """EN: Dependency provider for GetCaseStudyUseCase. | ES: Proveedor de dependencia para GetCaseStudyUseCase."""
    return GetCaseStudyUseCase(_case_study_repo)


def get_submit_decision_use_case() -> SubmitDecisionUseCase:
    """EN: Dependency provider for SubmitDecisionUseCase. | ES: Proveedor de dependencia para SubmitDecisionUseCase."""
    return SubmitDecisionUseCase(
        case_study_repository=_case_study_repo,
        decision_impact_repository=_decision_impact_repo,
        matrix_evaluator=_matrix_evaluator,
        composite_evaluator=_composite_evaluator,
    )


def get_decision_impact_use_case() -> GetDecisionImpactUseCase:
    """EN: Dependency provider for GetDecisionImpactUseCase. | ES: Proveedor de dependencia para GetDecisionImpactUseCase."""
    return GetDecisionImpactUseCase(_decision_impact_repo)


def get_list_scenarios_use_case() -> ListScenariosUseCase:
    """EN: Dependency provider for ListScenariosUseCase. | ES: Proveedor de dependencia para ListScenariosUseCase."""
    return ListScenariosUseCase(_scenario_repo)


def get_scenario_use_case() -> GetScenarioUseCase:
    """EN: Dependency provider for GetScenarioUseCase. | ES: Proveedor de dependencia para GetScenarioUseCase."""
    return GetScenarioUseCase(_scenario_repo)


def get_evaluate_scenario_use_case() -> EvaluateScenarioUseCase:
    """EN: Dependency provider for EvaluateScenarioUseCase. | ES: Proveedor de dependencia para EvaluateScenarioUseCase."""
    return EvaluateScenarioUseCase(
        scenario_repository=_scenario_repo,
        assessment_repository=_assessment_repo,
        composite_evaluator=_composite_evaluator,
    )


# EN: Health and Metadata Endpoints | ES: Puntos Finales de Salud y Metadatos


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="EN: Health Check Probe | ES: Sondeo de Verificacion de Salud",
    description="EN: Returns service operational readiness and architectural compliance. | ES: Retorna la preparacion operativa del servicio y cumplimiento arquitectonico.",
)
def health_check() -> dict[str, str]:
    """EN: Health check probe verifying service responsiveness. | ES: Sondeo de verificacion de salud que valida la capacidad de respuesta del servicio."""
    return {
        "status": "healthy",
        "service": "ai-ethics-simulator-backend",
        "architecture": "Clean Architecture / SOLID",
    }


@router.get(
    "/frameworks",
    status_code=status.HTTP_200_OK,
    summary="EN: List Supported Ethical Frameworks | ES: Listar Marcos Eticos Soportados",
    description="EN: Returns metadata regarding supported statutory and technical AI ethics frameworks. | ES: Retorna metadatos sobre los marcos estatutarios y tecnicos de etica en IA soportados.",
)
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


# EN: Case Studies Endpoints | ES: Puntos Finales de Casos de Estudio


@router.get(
    "/cases",
    response_model=list[CaseStudySummaryDTO],
    status_code=status.HTTP_200_OK,
    summary="EN: Fetch All Complex NLP Case Studies | ES: Obtener Todos los Casos de Estudio Complejos de NLP",
    description="EN: Retrieves summaries of complex computational linguistics ethical dilemmas. | ES: Recupera resumenes de dilemas eticos complejos en linguistica computacional.",
)
def get_case_studies(
    use_case: Annotated[ListCaseStudiesUseCase, Depends(get_list_case_studies_use_case)],
) -> list[CaseStudySummaryDTO]:
    """EN: Retrieve all registered computational linguistics case studies. | ES: Recuperar todos los casos de estudio de linguistica computacional registrados."""
    return use_case.execute()


@router.get(
    "/cases/{case_id}",
    response_model=CaseStudyDTO,
    status_code=status.HTTP_200_OK,
    summary="EN: Fetch Specific Case Study Details | ES: Obtener Detalles de Caso de Estudio Especifico",
    description="EN: Retrieves full specification, artifacts, baseline matrix, and decision options for a case study. | ES: Recupera la especificacion completa, artefactos, matriz base y opciones de decision para un caso de estudio.",
)
def get_case_study(
    case_id: str,
    use_case: Annotated[GetCaseStudyUseCase, Depends(get_case_study_use_case)],
) -> CaseStudyDTO:
    """EN: Retrieve specific case study specification by identifier. | ES: Recuperar la especificacion de un caso de estudio por identificador."""
    return use_case.execute(case_id)


# EN: Decision Submission and Evaluation Endpoints | ES: Puntos Finales de Envio y Evaluacion de Decisiones


@router.post(
    "/decisions",
    response_model=DecisionImpactResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="EN: Submit Ethical Decision and Calculate Impact | ES: Enviar Decision Etica y Calcular Impacto",
    description="EN: Evaluates chosen decision against multidimensional matrix (Transparency, Accountability, Fairness) and international frameworks. | ES: Evalua la decision elegida frente a la matriz multidimensional (Transparencia, Rendicion de Cuentas, Equidad) y marcos internacionales.",
)
def submit_decision(
    request: SubmitDecisionRequest,
    use_case: Annotated[SubmitDecisionUseCase, Depends(get_submit_decision_use_case)],
) -> DecisionImpactResponseDTO:
    """EN: Submit decision option, compute multidimensional impact and regulatory audit. | ES: Enviar opcion de decision, calcular impacto multidimensional y auditoria regulatoria."""
    return use_case.execute(request)


@router.get(
    "/evaluations/{evaluation_id}",
    response_model=DecisionImpactResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="EN: Fetch Decision Impact Calculation Result | ES: Obtener Resultado de Calculo de Impacto de Decision",
    description="EN: Retrieves a previously computed decision impact evaluation by identifier. | ES: Recupera una evaluacion de impacto de decision previamente calculada por identificador.",
)
def get_decision_impact(
    evaluation_id: str,
    use_case: Annotated[GetDecisionImpactUseCase, Depends(get_decision_impact_use_case)],
) -> DecisionImpactResponseDTO:
    """EN: Retrieve stored decision impact evaluation. | ES: Recuperar evaluacion de impacto de decision almacenada."""
    result = use_case.execute(evaluation_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Evaluation with id '{evaluation_id}' was not found.",
        )
    return result


# EN: Scenarios Compatibility Endpoints | ES: Puntos Finales de Compatibilidad de Escenarios


@router.get(
    "/scenarios",
    response_model=list[ScenarioDTO],
    status_code=status.HTTP_200_OK,
    summary="EN: List Scenarios | ES: Listar Escenarios",
)
def get_scenarios(
    use_case: Annotated[ListScenariosUseCase, Depends(get_list_scenarios_use_case)],
) -> list[ScenarioDTO]:
    """EN: Retrieve all registered computational linguistics scenarios. | ES: Recuperar todos los escenarios de linguistica computacional registrados."""
    return use_case.execute()


@router.get(
    "/scenarios/{scenario_id}",
    response_model=ScenarioDTO,
    status_code=status.HTTP_200_OK,
    summary="EN: Get Scenario by ID | ES: Obtener Escenario por ID",
)
def get_scenario(
    scenario_id: str,
    use_case: Annotated[GetScenarioUseCase, Depends(get_scenario_use_case)],
) -> ScenarioDTO:
    """EN: Retrieve a specific scenario by its unique identifier. | ES: Recuperar un escenario especifico por su identificador unico."""
    return use_case.execute(scenario_id)


@router.post(
    "/evaluations",
    response_model=EthicalAssessmentDTO,
    status_code=status.HTTP_201_CREATED,
    summary="EN: Evaluate Scenario | ES: Evaluar Escenario",
)
def evaluate_scenario(
    request: EvaluateScenarioRequest,
    use_case: Annotated[EvaluateScenarioUseCase, Depends(get_evaluate_scenario_use_case)],
) -> EthicalAssessmentDTO:
    """EN: Execute ethical evaluation on a specified scenario across chosen frameworks. | ES: Ejecutar evaluacion etica sobre un escenario especificado a traves de los marcos elegidos."""
    return use_case.execute(request)
