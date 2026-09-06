"""EN: Composite evaluator implementing Open-Closed Principle for multi-framework audits. | ES: Evaluador compuesto que implementa el principio Abierto-Cerrado para auditorias de multiples marcos."""

import uuid

from domain.entities import (
    EthicalAssessment,
    FrameworkAssessment,
    FrameworkType,
    Scenario,
)
from domain.exceptions import UnsupportedFrameworkError
from domain.interfaces import IEthicalEvaluator


class CompositeEvaluator:
    """EN: Aggregates multiple ethical framework evaluators into a unified evaluation pipeline. | ES: Agrega multiples evaluadores de marcos eticos en una tuberia de evaluacion unificada."""

    def __init__(self, evaluators: list[IEthicalEvaluator]) -> None:
        # EN: Map evaluators by framework type to allow OCP extension | ES: Mapear evaluadores por tipo de marco para permitir extension segun OCP
        self._evaluators: dict[FrameworkType, IEthicalEvaluator] = {ev.framework: ev for ev in evaluators}

    def register_evaluator(self, evaluator: IEthicalEvaluator) -> None:
        """EN: Register an additional ethical framework evaluator dynamically. | ES: Registrar dinamicamente un evaluador de marco etico adicional."""
        self._evaluators[evaluator.framework] = evaluator

    def evaluate_scenario(
        self,
        scenario: Scenario,
        framework_names: list[str],
    ) -> EthicalAssessment:
        """EN: Execute evaluations across specified frameworks and build consolidated assessment. | ES: Ejecutar evaluaciones a traves de los marcos especificados y construir la evaluacion consolidada."""
        framework_assessments: list[FrameworkAssessment] = []

        for name in framework_names:
            try:
                ft = FrameworkType(name)
            except ValueError as exc:
                raise UnsupportedFrameworkError(name) from exc

            if ft not in self._evaluators:
                raise UnsupportedFrameworkError(name)

            evaluator = self._evaluators[ft]
            assessment = evaluator.evaluate(scenario)
            framework_assessments.append(assessment)

        # EN: Synthesize high-level executive summary | ES: Sintetizar resumen ejecutivo de alto nivel
        summary = self._build_executive_summary(scenario, framework_assessments)
        assessment_id = str(uuid.uuid4())

        return EthicalAssessment.create(
            assessment_id=assessment_id,
            scenario_id=scenario.id,
            framework_assessments=framework_assessments,
            executive_summary=summary,
        )

    def _build_executive_summary(
        self,
        scenario: Scenario,
        assessments: list[FrameworkAssessment],
    ) -> str:
        """EN: Construct readable executive summary of ethical findings across frameworks. | ES: Construir un resumen ejecutivo legible de hallazgos eticos a traves de los marcos."""
        framework_summaries: list[str] = []

        for fa in assessments:
            passed_metrics = sum(1 for m in fa.metrics if m.passed)
            total_metrics = len(fa.metrics)
            findings_count = len(fa.findings)
            status_text = fa.compliance_status.value
            framework_summaries.append(
                f"[{fa.framework.value}]: Status={status_text}, "
                f"Metrics Passed={passed_metrics}/{total_metrics}, "
                f"Defects Identified={findings_count}."
            )

        details = " ".join(framework_summaries)
        return (
            f"Evaluation conducted for scenario '{scenario.title}' across " f"{len(assessments)} frameworks. {details}"
        )
