"""EN: Unit tests for the Multidimensional Ethical Matrix evaluation engine. | ES: Pruebas unitarias para el motor de evaluacion de matriz etica multidimensional."""

from application.evaluators.matrix_evaluator import MatrixEvaluator
from domain.entities import (
    CaseStudy,
    DecisionOption,
    EthicalDimension,
    LinguisticArtifact,
    TaskType,
)


def _create_fixture_case() -> CaseStudy:
    """EN: Helper creating standard case study fixture. | ES: Auxiliar que crea un accesorio de caso de estudio estandar."""
    return CaseStudy(
        id="fixture-cs-01",
        title="Test Case Study",
        nlp_domain="NLP Testing",
        dilemma="A synthetic dilemma for testing.",
        context_description="Testing context description.",
        task_type=TaskType.TEXT_CLASSIFICATION,
        domain_category="testing",
        baseline_matrix={
            EthicalDimension.TRANSPARENCY: 0.50,
            EthicalDimension.ACCOUNTABILITY: 0.50,
            EthicalDimension.FAIRNESS: 0.50,
        },
        decision_options=[
            DecisionOption(
                id="opt-positive",
                title="Positive Option",
                description="Improves all dimensions.",
                strategy="Improvement",
                dimension_modifiers={
                    EthicalDimension.TRANSPARENCY: +0.20,
                    EthicalDimension.ACCOUNTABILITY: +0.30,
                    EthicalDimension.FAIRNESS: +0.25,
                },
                rationale="Positive boost to all pillars.",
            ),
            DecisionOption(
                id="opt-tradeoff",
                title="Tradeoff Option",
                description="Improves fairness but degrades transparency.",
                strategy="Tradeoff",
                dimension_modifiers={
                    EthicalDimension.TRANSPARENCY: -0.20,
                    EthicalDimension.ACCOUNTABILITY: 0.0,
                    EthicalDimension.FAIRNESS: +0.30,
                },
                rationale="Fairness prioritized over transparency.",
            ),
            DecisionOption(
                id="opt-overflow",
                title="Overflow Option",
                description="Tests clamping boundaries.",
                strategy="Boundary Test",
                dimension_modifiers={
                    EthicalDimension.TRANSPARENCY: +0.90,
                    EthicalDimension.ACCOUNTABILITY: -0.90,
                    EthicalDimension.FAIRNESS: 0.0,
                },
                rationale="Tests clamping boundaries between 0 and 1.",
            ),
        ],
        regulatory_implications={"test": "rule"},
        linguistic_artifacts=[
            LinguisticArtifact(
                text_sample="Hello test",
                dialect_or_variety="Standard",
                protected_attribute="none",
                expected_output="OK",
                observed_output="OK",
                confidence_score=0.9,
            )
        ],
    )


def test_matrix_evaluation_scores_and_deltas() -> None:
    """EN: Test calculation of dimension scores and positive deltas. | ES: Probar calculo de puntuaciones de dimensiones y deltas positivos."""
    case = _create_fixture_case()
    evaluator = MatrixEvaluator()
    option = case.decision_options[0]

    matrix = evaluator.evaluate(case, option)

    assert matrix.transparency.baseline_score == 0.50
    assert matrix.transparency.decision_score == 0.70
    assert matrix.transparency.delta == 0.20

    assert matrix.accountability.baseline_score == 0.50
    assert matrix.accountability.decision_score == 0.80
    assert matrix.accountability.delta == 0.30

    assert matrix.fairness.baseline_score == 0.50
    assert matrix.fairness.decision_score == 0.75
    assert matrix.fairness.delta == 0.25

    expected_alignment = round((0.70 + 0.80 + 0.75) / 3.0, 3)
    assert matrix.overall_alignment == expected_alignment


def test_matrix_evaluation_clamping_boundaries() -> None:
    """EN: Test scores are strictly clamped to [0.0, 1.0]. | ES: Probar que las puntuaciones esten estrictamente limitadas a [0.0, 1.0]."""
    case = _create_fixture_case()
    evaluator = MatrixEvaluator()
    option = case.decision_options[2]  # overflow option

    matrix = evaluator.evaluate(case, option)

    # 0.50 + 0.90 = 1.40 -> clamped to 1.0
    assert matrix.transparency.decision_score == 1.0
    assert matrix.transparency.delta == 0.50

    # 0.50 - 0.90 = -0.40 -> clamped to 0.0
    assert matrix.accountability.decision_score == 0.0
    assert matrix.accountability.delta == -0.50


def test_custom_weights_normalization() -> None:
    """EN: Test custom weights calculation and normalization. | ES: Probar calculo y normalizacion de ponderaciones personalizadas."""
    case = _create_fixture_case()
    evaluator = MatrixEvaluator()
    option = case.decision_options[0]

    # Transparency=0.70, Accountability=0.80, Fairness=0.75
    # Weight only Fairness (1.0)
    custom_weights = {"FAIRNESS": 1.0, "TRANSPARENCY": 0.0, "ACCOUNTABILITY": 0.0}
    matrix = evaluator.evaluate(case, option, custom_weights=custom_weights)

    assert matrix.overall_alignment == 0.75


def test_trade_off_analysis_generation() -> None:
    """EN: Test qualitative trade-off analysis narrative contains dimensions. | ES: Probar que la narrativa de analisis de compensaciones cualitativo contenga dimensiones."""
    case = _create_fixture_case()
    evaluator = MatrixEvaluator()
    option = case.decision_options[1]  # tradeoff option

    matrix = evaluator.evaluate(case, option)
    trade_off = evaluator.generate_trade_off_analysis(case, option, matrix)

    assert "Strengthened dimensions: Fairness" in trade_off
    assert "Compromised dimensions: Transparency" in trade_off
    assert "Neutral impact on: Accountability" in trade_off
