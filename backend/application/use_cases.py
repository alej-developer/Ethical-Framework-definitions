"""EN: Application use cases orchestrating domain entities and persistence ports. | ES: Casos de uso de la aplicacion que orquestan entidades de dominio y puertos de persistencia."""

import uuid
from datetime import UTC, datetime

from application.dtos import (
    CaseStudyDTO,
    CaseStudySummaryDTO,
    DecisionImpactResponseDTO,
    DecisionOptionDTO,
    DimensionScoreDTO,
    EthicalAssessmentDTO,
    EthicalFindingDTO,
    EvaluateScenarioRequest,
    EvaluationMetricDTO,
    FrameworkAssessmentDTO,
    LinguisticArtifactDTO,
    MultidimensionalMatrixDTO,
    ScenarioDTO,
    SubmitDecisionRequest,
)
from application.evaluators.composite_evaluator import CompositeEvaluator
from application.evaluators.matrix_evaluator import MatrixEvaluator
from domain.entities import (
    CaseStudy,
    DecisionImpactResult,
    DecisionOption,
    EthicalAssessment,
    Scenario,
)
from domain.exceptions import (
    CaseStudyNotFoundError,
    InvalidDecisionOptionError,
    ScenarioNotFoundError,
)
from domain.interfaces import (
    IAssessmentRepository,
    ICaseStudyRepository,
    IDecisionImpactRepository,
    IScenarioRepository,
)


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
        self._scenario_repository = scenario_repository

    def execute(self) -> list[ScenarioDTO]:
        """EN: Retrieve all scenarios and map them to DTO representations. | ES: Recuperar todos los escenarios y mapearlos a representaciones DTO."""
        scenarios = self._scenario_repository.list_all()
        return [self._map_scenario(s) for s in scenarios]

    def _map_scenario(self, scenario: Scenario) -> ScenarioDTO:
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


# EN: Use cases for Complex NLP Case Studies and Decision Evaluation | ES: Casos de uso para Casos de Estudio Complejos de NLP y Evaluacion de Decisiones


class ListCaseStudiesUseCase:
    """EN: Use case for listing all computational linguistics case studies. | ES: Caso de uso para listar todos los casos de estudio de linguistica computacional."""

    def __init__(self, case_study_repository: ICaseStudyRepository) -> None:
        self._case_study_repository = case_study_repository

    def execute(self) -> list[CaseStudySummaryDTO]:
        """EN: Query all case studies and return summary DTOs. | ES: Consultar todos los casos de estudio y retornar DTOs de resumen."""
        studies = self._case_study_repository.list_all()
        return [
            CaseStudySummaryDTO(
                id=c.id,
                title=c.title,
                nlp_domain=c.nlp_domain,
                dilemma=c.dilemma,
                domain_category=c.domain_category,
                task_type=c.task_type.value,
                available_options_count=len(c.decision_options),
            )
            for c in studies
        ]


class GetCaseStudyUseCase:
    """EN: Use case for fetching complete case study specifications. | ES: Caso de uso para obtener especificaciones completas de casos de estudio."""

    def __init__(self, case_study_repository: ICaseStudyRepository) -> None:
        self._case_study_repository = case_study_repository

    def execute(self, case_id: str) -> CaseStudyDTO:
        """EN: Retrieve case study by ID, raising CaseStudyNotFoundError if absent. | ES: Recuperar caso de estudio por ID, lanzando CaseStudyNotFoundError si esta ausente."""
        case_study = self._case_study_repository.get_by_id(case_id)
        if case_study is None:
            raise CaseStudyNotFoundError(case_id)

        return self._map_case_study(case_study)

    def _map_case_study(self, case_study: CaseStudy) -> CaseStudyDTO:
        artifacts = [
            LinguisticArtifactDTO(
                text_sample=a.text_sample,
                dialect_or_variety=a.dialect_or_variety,
                protected_attribute=a.protected_attribute,
                expected_output=a.expected_output,
                observed_output=a.observed_output,
                confidence_score=a.confidence_score,
            )
            for a in case_study.linguistic_artifacts
        ]

        options = [
            DecisionOptionDTO(
                id=o.id,
                title=o.title,
                description=o.description,
                strategy=o.strategy,
                dimension_modifiers={k.value: v for k, v in o.dimension_modifiers.items()},
                rationale=o.rationale,
            )
            for o in case_study.decision_options
        ]

        baseline = {k.value: v for k, v in case_study.baseline_matrix.items()}

        return CaseStudyDTO(
            id=case_study.id,
            title=case_study.title,
            nlp_domain=case_study.nlp_domain,
            dilemma=case_study.dilemma,
            context_description=case_study.context_description,
            task_type=case_study.task_type.value,
            domain_category=case_study.domain_category,
            linguistic_artifacts=artifacts,
            baseline_matrix=baseline,
            decision_options=options,
            regulatory_implications=case_study.regulatory_implications,
            metadata=case_study.metadata,
        )


class SubmitDecisionUseCase:
    """EN: Use case orchestrating decision evaluation against the multidimensional matrix and international frameworks. | ES: Caso de uso que orquesta la evaluacion de decisiones frente a la matriz multidimensional y marcos internacionales."""

    def __init__(
        self,
        case_study_repository: ICaseStudyRepository,
        decision_impact_repository: IDecisionImpactRepository,
        matrix_evaluator: MatrixEvaluator,
        composite_evaluator: CompositeEvaluator,
    ) -> None:
        self._case_study_repository = case_study_repository
        self._decision_impact_repository = decision_impact_repository
        self._matrix_evaluator = matrix_evaluator
        self._composite_evaluator = composite_evaluator

    def execute(self, request: SubmitDecisionRequest) -> DecisionImpactResponseDTO:
        """EN: Execute multidimensional and regulatory evaluation for submitted user decision. | ES: Ejecutar evaluacion multidimensional y regulatoria para la decision enviada por el usuario."""
        case_study = self._case_study_repository.get_by_id(request.case_id)
        if case_study is None:
            raise CaseStudyNotFoundError(request.case_id)

        selected_option = next(
            (opt for opt in case_study.decision_options if opt.id == request.selected_option_id),
            None,
        )
        if selected_option is None:
            raise InvalidDecisionOptionError(request.case_id, request.selected_option_id)

        # EN: 1. Evaluate against multidimensional ethical matrix (Transparency, Accountability, Fairness) | ES: 1. Evaluar frente a la matriz etica multidimensional (Transparencia, Rendicion de Cuentas, Equidad)
        matrix = self._matrix_evaluator.evaluate(
            case_study=case_study,
            selected_option=selected_option,
            custom_weights=request.custom_weights,
        )

        trade_off = self._matrix_evaluator.generate_trade_off_analysis(
            case_study=case_study,
            option=selected_option,
            matrix=matrix,
        )

        # EN: 2. Cross-evaluate with regulatory frameworks (EU AI Act & IEEE Standards) | ES: 2. Realizar evaluacion cruzada con marcos regulatorios (Ley de IA de la UE y Normas IEEE)
        scenario_for_eval = self._adapt_scenario_with_decision(case_study, selected_option)
        framework_assessment = self._composite_evaluator.evaluate_scenario(
            scenario=scenario_for_eval,
            framework_names=request.frameworks,
        )

        # EN: 3. Consolidate recommendations | ES: 3. Consolidar recomendaciones
        consolidated_recommendations: list[str] = []
        for fa in framework_assessment.framework_assessments:
            consolidated_recommendations.extend(fa.recommendations)

        if matrix.transparency.decision_score < 0.60:
            consolidated_recommendations.append(
                "Augment transparency logs and external model card documentation (IEEE 7001)."
            )
        if matrix.fairness.decision_score < 0.70:
            consolidated_recommendations.append(
                "Conduct counterfactual dialectal data augmentation to mitigate disparate impact (EU AI Act Art. 10)."
            )

        # EN: 4. Construct and persist decision impact result | ES: 4. Construir y persistir resultado de impacto de decision
        decision_id = f"dec-{uuid.uuid4().hex[:8]}"
        result = DecisionImpactResult(
            decision_id=decision_id,
            case_id=case_study.id,
            selected_option=selected_option,
            matrix=matrix,
            framework_assessments=framework_assessment.framework_assessments,
            overall_risk_tier=framework_assessment.overall_risk_tier,
            overall_compliance=framework_assessment.overall_compliance,
            trade_off_analysis=trade_off,
            recommendations=list(dict.fromkeys(consolidated_recommendations)),
            created_at=datetime.now(UTC),
        )

        self._decision_impact_repository.save(result)
        return self._map_to_response_dto(result)

    def _adapt_scenario_with_decision(self, case_study: CaseStudy, option: DecisionOption) -> Scenario:
        """EN: Adapt scenario metadata reflecting chosen decision intervention. | ES: Adaptar metadatos del escenario reflejando la intervencion de decision elegida."""
        scenario = case_study.to_scenario()
        # EN: Enhance metadata based on intervention strategy | ES: Mejorar metadatos segun la estrategia de intervencion
        if "oversight" in option.id.lower() or "governance" in option.id.lower():
            scenario.metadata["human_in_the_loop"] = True
        if "transparency" in option.id.lower() or "provenance" in option.id.lower():
            scenario.metadata["explainability_enabled"] = True
            scenario.metadata["confidence_scores_visible"] = True
            scenario.metadata["provenance_verified"] = True
        return scenario

    def _map_to_response_dto(self, result: DecisionImpactResult) -> DecisionImpactResponseDTO:
        """EN: Map domain DecisionImpactResult to application response DTO. | ES: Mapear DecisionImpactResult de dominio al DTO de respuesta de la aplicacion."""
        opt_dto = DecisionOptionDTO(
            id=result.selected_option.id,
            title=result.selected_option.title,
            description=result.selected_option.description,
            strategy=result.selected_option.strategy,
            dimension_modifiers={k.value: v for k, v in result.selected_option.dimension_modifiers.items()},
            rationale=result.selected_option.rationale,
        )

        matrix_dto = MultidimensionalMatrixDTO(
            transparency=DimensionScoreDTO(
                dimension=result.matrix.transparency.dimension.value,
                baseline_score=result.matrix.transparency.baseline_score,
                decision_score=result.matrix.transparency.decision_score,
                delta=result.matrix.transparency.delta,
                rationale=result.matrix.transparency.rationale,
            ),
            accountability=DimensionScoreDTO(
                dimension=result.matrix.accountability.dimension.value,
                baseline_score=result.matrix.accountability.baseline_score,
                decision_score=result.matrix.accountability.decision_score,
                delta=result.matrix.accountability.delta,
                rationale=result.matrix.accountability.rationale,
            ),
            fairness=DimensionScoreDTO(
                dimension=result.matrix.fairness.dimension.value,
                baseline_score=result.matrix.fairness.baseline_score,
                decision_score=result.matrix.fairness.decision_score,
                delta=result.matrix.fairness.delta,
                rationale=result.matrix.fairness.rationale,
            ),
            overall_alignment=result.matrix.overall_alignment,
        )

        framework_dtos: list[FrameworkAssessmentDTO] = []
        for fa in result.framework_assessments:
            m_dtos = [
                EvaluationMetricDTO(
                    name=m.name,
                    score=m.score,
                    threshold=m.threshold,
                    passed=m.passed,
                    description=m.description,
                )
                for m in fa.metrics
            ]
            f_dtos = [
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
                    metrics=m_dtos,
                    findings=f_dtos,
                    recommendations=fa.recommendations,
                )
            )

        return DecisionImpactResponseDTO(
            decision_id=result.decision_id,
            case_id=result.case_id,
            selected_option=opt_dto,
            matrix=matrix_dto,
            framework_assessments=framework_dtos,
            overall_risk_tier=result.overall_risk_tier.value,
            overall_compliance=result.overall_compliance.value,
            trade_off_analysis=result.trade_off_analysis,
            recommendations=result.recommendations,
            created_at=result.created_at,
        )


class GetDecisionImpactUseCase:
    """EN: Use case for fetching past decision impact calculation by ID. | ES: Caso de uso para obtener el calculo de impacto de decision previo por ID."""

    def __init__(self, decision_impact_repository: IDecisionImpactRepository) -> None:
        self._decision_impact_repository = decision_impact_repository

    def execute(self, decision_id: str) -> DecisionImpactResponseDTO | None:
        """EN: Retrieve decision impact result by ID. | ES: Recuperar resultado de impacto de decision por ID."""
        result = self._decision_impact_repository.get_by_id(decision_id)
        if result is None:
            return None

        # EN: Map using SubmitDecisionUseCase helper | ES: Mapear usando auxiliar de SubmitDecisionUseCase
        dummy_matrix_evaluator = MatrixEvaluator()
        dummy_composite = CompositeEvaluator([])
        submit_use_case = SubmitDecisionUseCase(
            case_study_repository=None,  # type: ignore[arg-type]
            decision_impact_repository=self._decision_impact_repository,
            matrix_evaluator=dummy_matrix_evaluator,
            composite_evaluator=dummy_composite,
        )
        return submit_use_case._map_to_response_dto(result)
