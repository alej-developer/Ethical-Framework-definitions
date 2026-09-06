"""EN: Multidimensional ethical matrix evaluation engine assessing Transparency, Accountability, and Fairness. | ES: Motor de evaluacion de matriz etica multidimensional que evalua Transparencia, Rendicion de Cuentas y Equidad."""

from domain.entities import (
    CaseStudy,
    DecisionOption,
    DimensionScore,
    EthicalDimension,
    MultidimensionalMatrix,
)


class MatrixEvaluator:
    """EN: Evaluates decision options against predefined multidimensional ethical criteria. | ES: Evalua opciones de decision frente a criterios eticos multidimensionales predefinidos."""

    def evaluate(
        self,
        case_study: CaseStudy,
        selected_option: DecisionOption,
        custom_weights: dict[str, float] | None = None,
    ) -> MultidimensionalMatrix:
        """EN: Calculate dimension scores, deltas, and overall alignment score. | ES: Calcular puntuaciones de dimensiones, deltas y puntuacion de alineacion general."""
        # EN: Resolve dimension weights (default uniform 1/3 each) | ES: Resolver ponderaciones de dimensiones (por defecto uniforme 1/3 cada una)
        weights = self._resolve_weights(custom_weights)

        # EN: Calculate individual dimension evaluations | ES: Calcular evaluaciones de dimensiones individuales
        transparency_score = self._compute_dimension_score(
            case_study=case_study,
            option=selected_option,
            dimension=EthicalDimension.TRANSPARENCY,
        )

        accountability_score = self._compute_dimension_score(
            case_study=case_study,
            option=selected_option,
            dimension=EthicalDimension.ACCOUNTABILITY,
        )

        fairness_score = self._compute_dimension_score(
            case_study=case_study,
            option=selected_option,
            dimension=EthicalDimension.FAIRNESS,
        )

        # EN: Calculate overall weighted alignment index | ES: Calcular indice de alineacion ponderado general
        overall_alignment = round(
            weights[EthicalDimension.TRANSPARENCY] * transparency_score.decision_score
            + weights[EthicalDimension.ACCOUNTABILITY] * accountability_score.decision_score
            + weights[EthicalDimension.FAIRNESS] * fairness_score.decision_score,
            3,
        )

        return MultidimensionalMatrix(
            transparency=transparency_score,
            accountability=accountability_score,
            fairness=fairness_score,
            overall_alignment=overall_alignment,
        )

    def generate_trade_off_analysis(
        self,
        case_study: CaseStudy,
        option: DecisionOption,
        matrix: MultidimensionalMatrix,
    ) -> str:
        """EN: Formulate qualitative trade-off analysis explaining ethical tensions. | ES: Formular analisis de compensaciones cualitativo que explica las tensiones eticas."""
        deltas = {
            "Transparency": matrix.transparency.delta,
            "Accountability": matrix.accountability.delta,
            "Fairness": matrix.fairness.delta,
        }

        improved = [dim for dim, d in deltas.items() if d > 0]
        degraded = [dim for dim, d in deltas.items() if d < 0]
        neutral = [dim for dim, d in deltas.items() if d == 0]

        parts: list[str] = [
            f"Strategy '{option.title}' yielded an overall alignment index of {matrix.overall_alignment}."
        ]

        if improved:
            parts.append(f"Strengthened dimensions: {', '.join(improved)}.")
        if degraded:
            parts.append(f"Compromised dimensions: {', '.join(degraded)}.")
        if neutral:
            parts.append(f"Neutral impact on: {', '.join(neutral)}.")

        parts.append(f"Operational context: {option.rationale}")
        return " ".join(parts)

    def _compute_dimension_score(
        self,
        case_study: CaseStudy,
        option: DecisionOption,
        dimension: EthicalDimension,
    ) -> DimensionScore:
        """EN: Compute individual dimension score with clamping [0.0, 1.0] and rationale. | ES: Calcular puntuacion de dimension individual con limitacion [0.0, 1.0] y justificacion."""
        baseline = case_study.baseline_matrix.get(dimension, 0.5)
        modifier = option.dimension_modifiers.get(dimension, 0.0)
        decision_score = max(0.0, min(1.0, round(baseline + modifier, 3)))
        delta = round(decision_score - baseline, 3)

        rationale = (
            f"Baseline {dimension.value} was {baseline}. "
            f"Decision modifier of {modifier:+.2f} shifted the score to {decision_score} "
            f"(Delta: {delta:+.2f})."
        )

        return DimensionScore(
            dimension=dimension,
            baseline_score=baseline,
            decision_score=decision_score,
            delta=delta,
            rationale=rationale,
        )

    def _resolve_weights(self, custom_weights: dict[str, float] | None) -> dict[EthicalDimension, float]:
        """EN: Normalize dimension weights to sum to 1.0. | ES: Normalizar ponderaciones de dimensiones para que sumen 1.0."""
        default_weights: dict[EthicalDimension, float] = {
            EthicalDimension.TRANSPARENCY: 1.0 / 3.0,
            EthicalDimension.ACCOUNTABILITY: 1.0 / 3.0,
            EthicalDimension.FAIRNESS: 1.0 / 3.0,
        }

        if not custom_weights:
            return default_weights

        total = sum(custom_weights.values())
        if total <= 0:
            return default_weights

        normalized: dict[EthicalDimension, float] = {}
        for dim in EthicalDimension:
            raw_w = custom_weights.get(dim.value, custom_weights.get(dim.name, 1.0 / 3.0))
            normalized[dim] = raw_w / total

        return normalized
