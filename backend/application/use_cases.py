"""EN: Application use cases orchestrating domain entities and persistence ports. | ES: Casos de uso de la aplicacion que orquestan entidades de dominio y puertos de persistencia."""

from application.dtos import (
    EthicalAssessmentDTO,
    EthicalFindingDTO,
    EvaluateScenarioRequest,
    EvaluationMetricDTO,
    FrameworkAssessmentDTO,
    LinguisticArtifactDTO,
    ScenarioDTO,
)
from application.evaluators.composite_evaluator import CompositeEvaluator
from domain.entities import EthicalAssessment, Scenario
from domain.exceptions import ScenarioNotFoundError
from domain.interfaces import IAssessmentRepository, IScenarioRepository


class EvaluateScenarioUseCase:
    """EN: Use case for executing ethical audits on a scenario across selected frameworks. | ES: Caso de uso para ejecutar auditorias eticas sobre un escenario a traves de los marcos seleccionados."""

    def __init__(
        self,
        scenario_repository: IScenarioRepository,
        assessment_repository: IAssessmentRepository,
        composite_evaluator: CompositeEvaluator,
    ) -> None:
        # EN: Inject repository and evaluation dependencies (DIP) | ES: Inyectar dependencias de repositorio y evaluacion (DIP)
        self._scenario_repository = scenario_repository
        self._assessment_repository = assessment_repository
        self._composite_evaluator = composite_evaluator

    def execute(self, request: EvaluateScenarioRequest) -> EthicalAssessmentDTO:
        """EN: Orchestrate the evaluation workflow and persist the generated assessment. | ES: Orquestar el flujo de evaluacion y persistir la evaluacion generada."""
        scenario = self._scenario_repository.get_by_id(request.scenario_id)
        if scenario is None:
            raise ScenarioNotFoundError(request.scenario_id)

        assessment = self._composite_evaluator.evaluate_scenario(
            scenario=scenario,
            framework_names=request.frameworks,
        )

        self._assessment_repository.save(assessment)
        return self._map_to_dto(assessment)

    def _map_to_dto(self, assessment: EthicalAssessment) -> EthicalAssessmentDTO:
        """EN: Map domain EthicalAssessment aggregate to application DTO. | ES: Mapear el agregado de dominio EthicalAssessment al DTO de la aplicacion."""
        framework_dtos: list[FrameworkAssessmentDTO] = []

        for fa in assessment.framework_assessments:
            metric_dtos = [
                EvaluationMetricDTO(
                    name=m.name,
                    score=m.score,
                    threshold=m.threshold,
                    passed=m.passed,
                    description=m.description,
                )
                for m in fa.metrics
            ]

            finding_dtos = [
                EthicalFindingDTO(
                    framework=fa.framework.value,
                    category=f.category,
                    severity=f.severity,
                    message=f.message,
                    recommendation=f.recommendation,
                )
                for f in fa.findings
            ]

            framework_dtos.append(
                FrameworkAssessmentDTO(
                    framework=fa.framework.value,
                    risk_tier=fa.risk_tier.value,
                    compliance_status=fa.compliance_status.value,
                    metrics=metric_dtos,
                    findings=finding_dtos,
                    recommendations=fa.recommendations,
                )
            )

        return EthicalAssessmentDTO(
            id=assessment.id,
            scenario_id=assessment.scenario_id,
            created_at=assessment.created_at,
            framework_assessments=framework_dtos,
            overall_risk_tier=assessment.overall_risk_tier.value,
            overall_compliance=assessment.overall_compliance.value,
            executive_summary=assessment.executive_summary,
        )


class ListScenariosUseCase:
    """EN: Use case for querying all available computational linguistics scenarios. | ES: Caso de uso para consultar todos los escenarios de linguistica computacional disponibles."""

    def __init__(self, scenario_repository: IScenarioRepository) -> None:
        # EN: Inject scenario persistence dependency | ES: Inyectar dependencia de persistencia de escenarios
        self._scenario_repository = scenario_repository

    def execute(self) -> list[ScenarioDTO]:
        """EN: Retrieve all scenarios and map them to DTO representations. | ES: Recuperar todos los escenarios y mapearlos a representaciones DTO."""
        scenarios = self._scenario_repository.list_all()
        return [self._map_scenario(s) for s in scenarios]

    def _map_scenario(self, scenario: Scenario) -> ScenarioDTO:
        """EN: Map domain Scenario entity to ScenarioDTO. | ES: Mapear entidad Scenario de dominio a ScenarioDTO."""
        artifacts = [
            LinguisticArtifactDTO(
                text_sample=a.text_sample,
                dialect_or_variety=a.dialect_or_variety,
                protected_attribute=a.protected_attribute,
                expected_output=a.expected_output,
                observed_output=a.observed_output,
                confidence_score=a.confidence_score,
            )
            for a in scenario.artifacts
        ]

        return ScenarioDTO(
            id=scenario.id,
            title=scenario.title,
            description=scenario.description,
            domain_category=scenario.domain_category,
            task_type=scenario.task_type.value,
            artifacts=artifacts,
            metadata=scenario.metadata,
        )


class GetScenarioUseCase:
    """EN: Use case for fetching a specific scenario by identifier. | ES: Caso de uso para obtener un escenario especifico por identificador."""

    def __init__(self, scenario_repository: IScenarioRepository) -> None:
        # EN: Inject repository dependency | ES: Inyectar dependencia de repositorio
        self._scenario_repository = scenario_repository

    def execute(self, scenario_id: str) -> ScenarioDTO:
        """EN: Retrieve scenario and convert to DTO, raising error if not found. | ES: Recuperar escenario y convertir a DTO, lanzando error si no se encuentra."""
        scenario = self._scenario_repository.get_by_id(scenario_id)
        if scenario is None:
            raise ScenarioNotFoundError(scenario_id)

        artifacts = [
            LinguisticArtifactDTO(
                text_sample=a.text_sample,
                dialect_or_variety=a.dialect_or_variety,
                protected_attribute=a.protected_attribute,
                expected_output=a.expected_output,
                observed_output=a.observed_output,
                confidence_score=a.confidence_score,
            )
            for a in scenario.artifacts
        ]

        return ScenarioDTO(
            id=scenario.id,
            title=scenario.title,
            description=scenario.description,
            domain_category=scenario.domain_category,
            task_type=scenario.task_type.value,
            artifacts=artifacts,
            metadata=scenario.metadata,
        )
