"""EN: Application layer tests validating use cases and orchestration logic. | ES: Pruebas de la capa de aplicacion que validan casos de uso y logica de orquestacion."""

import pytest

from application.dtos import EvaluateScenarioRequest, SubmitDecisionRequest
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
from domain.entities import (
    CaseStudy,
    DecisionImpactResult,
    DecisionOption,
    EthicalAssessment,
    EthicalDimension,
    LinguisticArtifact,
    Scenario,
    TaskType,
)
from domain.exceptions import (
    CaseStudyNotFoundError,
    InvalidDecisionOptionError,
    ScenarioNotFoundError,
    UnsupportedFrameworkError,
)
from domain.frameworks.eu_ai_act import EUAIActEvaluator
from domain.frameworks.ieee_standards import IEEEStandardsEvaluator
from domain.interfaces import (
    IAssessmentRepository,
    ICaseStudyRepository,
    IDecisionImpactRepository,
    IScenarioRepository,
)


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


class MockCaseStudyRepository(ICaseStudyRepository):
    """EN: Mock case study repository for unit testing. | ES: Repositorio simulado de casos de estudio para pruebas unitarias."""

    def __init__(self, initial_cases: list[CaseStudy] | None = None) -> None:
        self._data: dict[str, CaseStudy] = {c.id: c for c in (initial_cases or [])}

    def get_by_id(self, case_id: str) -> CaseStudy | None:
        return self._data.get(case_id)

    def list_all(self) -> list[CaseStudy]:
        return list(self._data.values())

    def save(self, case_study: CaseStudy) -> None:
        self._data[case_study.id] = case_study


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


class MockDecisionImpactRepository(IDecisionImpactRepository):
    """EN: Mock decision impact repository. | ES: Repositorio simulado de impacto de decision."""

    def __init__(self) -> None:
        self.saved_impacts: dict[str, DecisionImpactResult] = {}

    def save(self, result: DecisionImpactResult) -> None:
        self.saved_impacts[result.decision_id] = result

    def get_by_id(self, decision_id: str) -> DecisionImpactResult | None:
        return self.saved_impacts.get(decision_id)

    def list_by_case(self, case_id: str) -> list[DecisionImpactResult]:
        return [r for r in self.saved_impacts.values() if r.case_id == case_id]


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


@pytest.fixture
def sample_case_study() -> CaseStudy:
    """EN: Fixture providing a standard case study entity. | ES: Accesorio que proporciona una entidad de caso de estudio estandar."""
    return CaseStudy(
        id="cs-fixture-001",
        title="Recruitment Bias Test",
        nlp_domain="Information Extraction",
        dilemma="Dilemma regarding fairness vs throughput.",
        context_description="Context description.",
        task_type=TaskType.TEXT_CLASSIFICATION,
        domain_category="recruitment",
        baseline_matrix={
            EthicalDimension.TRANSPARENCY: 0.40,
            EthicalDimension.ACCOUNTABILITY: 0.40,
            EthicalDimension.FAIRNESS: 0.30,
        },
        decision_options=[
            DecisionOption(
                id="opt-fixture-oversight",
                title="Mandate Oversight",
                description="Oversight intervention.",
                strategy="Governance",
                dimension_modifiers={
                    EthicalDimension.TRANSPARENCY: +0.30,
                    EthicalDimension.ACCOUNTABILITY: +0.40,
                    EthicalDimension.FAIRNESS: +0.40,
                },
                rationale="Improves fairness and accountability.",
            ),
            DecisionOption(
                id="opt-fixture-speed",
                title="Maximize Speed",
                description="Speed intervention.",
                strategy="Speed",
                dimension_modifiers={
                    EthicalDimension.TRANSPARENCY: -0.10,
                    EthicalDimension.ACCOUNTABILITY: -0.20,
                    EthicalDimension.FAIRNESS: -0.20,
                },
                rationale="Degrades fairness.",
            ),
        ],
        linguistic_artifacts=[
            LinguisticArtifact(
                text_sample="Sample candidate resume.",
                dialect_or_variety="AAVE",
                protected_attribute="ethnicity_proxy",
                expected_output="ADVANCE",
                observed_output="ADVANCE",
                confidence_score=0.92,
            )
        ],
        regulatory_implications={"EU_AI_Act": "High Risk Annex III"},
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


# EN: Tests for Case Study and Decision Use Cases | ES: Pruebas para Casos de Uso de Casos de Estudio y Decisiones


def test_list_case_studies_use_case(sample_case_study: CaseStudy) -> None:
    """EN: Verify ListCaseStudiesUseCase returns summary DTOs. | ES: Verificar que ListCaseStudiesUseCase retorne DTOs de resumen."""
    repo = MockCaseStudyRepository([sample_case_study])
    use_case = ListCaseStudiesUseCase(repo)

    result = use_case.execute()

    assert len(result) == 1
    assert result[0].id == "cs-fixture-001"
    assert result[0].available_options_count == 2


def test_get_case_study_use_case_success(sample_case_study: CaseStudy) -> None:
    """EN: Verify GetCaseStudyUseCase retrieves full details. | ES: Verificar que GetCaseStudyUseCase recupere detalles completos."""
    repo = MockCaseStudyRepository([sample_case_study])
    use_case = GetCaseStudyUseCase(repo)

    result = use_case.execute("cs-fixture-001")

    assert result.id == "cs-fixture-001"
    assert len(result.decision_options) == 2
    assert len(result.linguistic_artifacts) == 1


def test_get_case_study_use_case_not_found() -> None:
    """EN: Verify GetCaseStudyUseCase raises CaseStudyNotFoundError. | ES: Verificar que GetCaseStudyUseCase lance CaseStudyNotFoundError."""
    repo = MockCaseStudyRepository([])
    use_case = GetCaseStudyUseCase(repo)

    with pytest.raises(CaseStudyNotFoundError):
        use_case.execute("unknown-case-id")


def test_submit_decision_use_case_success(sample_case_study: CaseStudy) -> None:
    """EN: Test decision submission, matrix calculation, and repository persistence. | ES: Probar envio de decision, calculo de matriz y persistencia en repositorio."""
    case_repo = MockCaseStudyRepository([sample_case_study])
    impact_repo = MockDecisionImpactRepository()
    matrix_eval = MatrixEvaluator()
    composite_eval = CompositeEvaluator([EUAIActEvaluator(), IEEEStandardsEvaluator()])

    use_case = SubmitDecisionUseCase(
        case_study_repository=case_repo,
        decision_impact_repository=impact_repo,
        matrix_evaluator=matrix_eval,
        composite_evaluator=composite_eval,
    )

    request = SubmitDecisionRequest(
        case_id="cs-fixture-001",
        selected_option_id="opt-fixture-oversight",
        user_rationale="Thorough ethical justification ensuring human verification.",
        frameworks=["EU_AI_ACT", "IEEE_7000_SERIES"],
    )

    response = use_case.execute(request)

    assert response.case_id == "cs-fixture-001"
    assert response.selected_option.id == "opt-fixture-oversight"
    assert response.matrix.fairness.decision_score == 0.70  # 0.30 + 0.40
    assert response.matrix.fairness.delta == 0.40
    assert response.matrix.transparency.decision_score == 0.70  # 0.40 + 0.30
    assert len(response.framework_assessments) == 2
    assert len(impact_repo.saved_impacts) == 1

    # EN: Test GetDecisionImpactUseCase retrieves stored result | ES: Probar que GetDecisionImpactUseCase recupere el resultado guardado
    get_impact_uc = GetDecisionImpactUseCase(impact_repo)
    retrieved = get_impact_uc.execute(response.decision_id)
    assert retrieved is not None
    assert retrieved.decision_id == response.decision_id


def test_submit_decision_case_not_found() -> None:
    """EN: Verify CaseStudyNotFoundError when submitting for invalid case ID. | ES: Verificar CaseStudyNotFoundError al enviar para ID de caso invalido."""
    case_repo = MockCaseStudyRepository([])
    impact_repo = MockDecisionImpactRepository()
    use_case = SubmitDecisionUseCase(
        case_study_repository=case_repo,
        decision_impact_repository=impact_repo,
        matrix_evaluator=MatrixEvaluator(),
        composite_evaluator=CompositeEvaluator([]),
    )

    request = SubmitDecisionRequest(
        case_id="unknown-case",
        selected_option_id="any-opt",
        user_rationale="Valid rationale with enough characters.",
    )

    with pytest.raises(CaseStudyNotFoundError):
        use_case.execute(request)


def test_submit_decision_invalid_option(sample_case_study: CaseStudy) -> None:
    """EN: Verify InvalidDecisionOptionError when option does not belong to case. | ES: Verificar InvalidDecisionOptionError cuando la opcion no pertenece al caso."""
    case_repo = MockCaseStudyRepository([sample_case_study])
    impact_repo = MockDecisionImpactRepository()
    use_case = SubmitDecisionUseCase(
        case_study_repository=case_repo,
        decision_impact_repository=impact_repo,
        matrix_evaluator=MatrixEvaluator(),
        composite_evaluator=CompositeEvaluator([]),
    )

    request = SubmitDecisionRequest(
        case_id="cs-fixture-001",
        selected_option_id="non-existent-option",
        user_rationale="Valid rationale with enough characters.",
    )

    with pytest.raises(InvalidDecisionOptionError):
        use_case.execute(request)


def test_get_decision_impact_not_found() -> None:
    """EN: Verify GetDecisionImpactUseCase returns None for unknown decision ID. | ES: Verificar que GetDecisionImpactUseCase retorne None para ID de decision desconocido."""
    impact_repo = MockDecisionImpactRepository()
    use_case = GetDecisionImpactUseCase(impact_repo)

    result = use_case.execute("unknown-dec-id")
    assert result is None
