"""EN: Application layer tests validating use cases and orchestration logic. | ES: Pruebas de la capa de aplicacion que validan casos de uso y logica de orquestacion."""

import pytest

from application.dtos import EvaluateScenarioRequest
from application.evaluators.composite_evaluator import CompositeEvaluator
from application.use_cases import (
    EvaluateScenarioUseCase,
    GetScenarioUseCase,
    ListScenariosUseCase,
)
from domain.entities import (
    EthicalAssessment,
    LinguisticArtifact,
    Scenario,
    TaskType,
)
from domain.exceptions import ScenarioNotFoundError, UnsupportedFrameworkError
from domain.frameworks.eu_ai_act import EUAIActEvaluator
from domain.frameworks.ieee_standards import IEEEStandardsEvaluator
from domain.interfaces import IAssessmentRepository, IScenarioRepository


class MockScenarioRepository(IScenarioRepository):
    """EN: Mock scenario repository for isolated unit testing. | ES: Repositorio simulado de escenarios para pruebas unitarias aisladas."""

    def __init__(self, initial_scenarios: list[Scenario] | None = None) -> None:
        self._data: dict[str, Scenario] = {s.id: s for s in (initial_scenarios or [])}

    def get_by_id(self, scenario_id: str) -> Scenario | None:
        return self._data.get(scenario_id)

    def list_all(self) -> list[Scenario]:
        return list(self._data.values())

    def save(self, scenario: Scenario) -> None:
        self._data[scenario.id] = scenario


class MockAssessmentRepository(IAssessmentRepository):
    """EN: Mock assessment repository for tracking persisted evaluations. | ES: Repositorio simulado de evaluaciones para rastrear evaluaciones persistidas."""

    def __init__(self) -> None:
        self.saved_assessments: list[EthicalAssessment] = []

    def save(self, assessment: EthicalAssessment) -> None:
        self.saved_assessments.append(assessment)

    def get_by_id(self, assessment_id: str) -> EthicalAssessment | None:
        return next((a for a in self.saved_assessments if a.id == assessment_id), None)

    def list_by_scenario(self, scenario_id: str) -> list[EthicalAssessment]:
        return [a for a in self.saved_assessments if a.scenario_id == scenario_id]


@pytest.fixture
def sample_scenario() -> Scenario:
    """EN: Fixture providing a standard test scenario entity. | ES: Accesorio que proporciona una entidad de escenario de prueba estandar."""
    return Scenario(
        id="fixture-scenario-1",
        title="Dialect Fairness Test",
        description="Scenario testing fairness across dialects.",
        domain_category="content_moderation",
        task_type=TaskType.CONTENT_MODERATION,
        artifacts=[
            LinguisticArtifact(
                text_sample="Hello there",
                dialect_or_variety="SAE",
                protected_attribute="norm",
                expected_output="OK",
                observed_output="OK",
                confidence_score=0.9,
            )
        ],
        metadata={"provenance_verified": True, "explainability_enabled": True},
    )


def test_list_scenarios_use_case(sample_scenario: Scenario) -> None:
    """EN: Verify ListScenariosUseCase returns DTO representations. | ES: Verificar que ListScenariosUseCase retorne representaciones DTO."""
    repo = MockScenarioRepository([sample_scenario])
    use_case = ListScenariosUseCase(repo)

    result = use_case.execute()

    assert len(result) == 1
    assert result[0].id == "fixture-scenario-1"
    assert result[0].title == "Dialect Fairness Test"


def test_get_scenario_not_found() -> None:
    """EN: Ensure GetScenarioUseCase raises ScenarioNotFoundError on unknown ID. | ES: Asegurar que GetScenarioUseCase lance ScenarioNotFoundError en un ID desconocido."""
    repo = MockScenarioRepository([])
    use_case = GetScenarioUseCase(repo)

    with pytest.raises(ScenarioNotFoundError):
        use_case.execute("non-existent-id")


def test_evaluate_scenario_use_case_success(sample_scenario: Scenario) -> None:
    """EN: Test end-to-end orchestration of scenario evaluation. | ES: Probar la orquestacion de extremo a extremo de la evaluacion de escenarios."""
    scenario_repo = MockScenarioRepository([sample_scenario])
    assessment_repo = MockAssessmentRepository()
    composite_evaluator = CompositeEvaluator([EUAIActEvaluator(), IEEEStandardsEvaluator()])

    use_case = EvaluateScenarioUseCase(
        scenario_repository=scenario_repo,
        assessment_repository=assessment_repo,
        composite_evaluator=composite_evaluator,
    )

    request = EvaluateScenarioRequest(
        scenario_id="fixture-scenario-1",
        frameworks=["EU_AI_ACT", "IEEE_7000_SERIES"],
    )

    result = use_case.execute(request)

    assert result.scenario_id == "fixture-scenario-1"
    assert len(result.framework_assessments) == 2
    assert len(assessment_repo.saved_assessments) == 1
    assert "Evaluation conducted" in result.executive_summary


def test_evaluate_scenario_unsupported_framework(sample_scenario: Scenario) -> None:
    """EN: Ensure evaluating with an invalid framework raises UnsupportedFrameworkError. | ES: Asegurar que evaluar con un marco invalido lance UnsupportedFrameworkError."""
    scenario_repo = MockScenarioRepository([sample_scenario])
    assessment_repo = MockAssessmentRepository()
    composite_evaluator = CompositeEvaluator([EUAIActEvaluator()])

    use_case = EvaluateScenarioUseCase(
        scenario_repository=scenario_repo,
        assessment_repository=assessment_repo,
        composite_evaluator=composite_evaluator,
    )

    request = EvaluateScenarioRequest(
        scenario_id="fixture-scenario-1",
        frameworks=["UNKNOWN_FRAMEWORK_XYZ"],
    )

    with pytest.raises(UnsupportedFrameworkError):
        use_case.execute(request)
