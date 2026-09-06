"""EN: Domain layer unit tests verifying business entities and ethical evaluators. | ES: Pruebas unitarias de la capa de dominio que verifican entidades de negocio y evaluadores eticos."""

from domain.entities import (
    ComplianceStatus,
    FrameworkAssessment,
    FrameworkType,
    LinguisticArtifact,
    RiskTier,
    Scenario,
    TaskType,
)
from domain.frameworks.eu_ai_act import EUAIActEvaluator
from domain.frameworks.ieee_standards import IEEEStandardsEvaluator


def test_scenario_creation() -> None:
    """EN: Test instantiation of computational linguistics Scenario entity. | ES: Probar instanciacion de la entidad Scenario de linguistica computacional."""
    artifact = LinguisticArtifact(
        text_sample="Sample text for evaluation.",
        dialect_or_variety="SAE",
        protected_attribute="standard",
        expected_output="BENIGN",
        observed_output="BENIGN",
        confidence_score=0.95,
    )
    scenario = Scenario(
        id="test-001",
        title="Test Scenario",
        description="A unit testing scenario.",
        domain_category="sentiment_analysis",
        task_type=TaskType.TEXT_CLASSIFICATION,
        artifacts=[artifact],
        metadata={"provenance_verified": True},
    )

    assert scenario.id == "test-001"
    assert len(scenario.artifacts) == 1
    assert scenario.task_type == TaskType.TEXT_CLASSIFICATION


def test_eu_ai_act_evaluator_high_risk() -> None:
    """EN: Verify EU AI Act evaluator identifies high risk under Annex III criteria. | ES: Verificar que el evaluador de la Ley de IA de la UE identifique alto riesgo segun criterios del Anexo III."""
    evaluator = EUAIActEvaluator()
    assert evaluator.framework == FrameworkType.EU_AI_ACT

    scenario = Scenario(
        id="clinical-001",
        title="Emergency Triage",
        description="Clinical triage scenario.",
        domain_category="clinical_triage",
        task_type=TaskType.CLINICAL_TRIAGE,
        artifacts=[
            LinguisticArtifact(
                text_sample="Severe pain in chest.",
                dialect_or_variety="Formal",
                protected_attribute="group_a",
                expected_output="URGENT",
                observed_output="URGENT",
                confidence_score=0.9,
            ),
            LinguisticArtifact(
                text_sample="Hurts real bad.",
                dialect_or_variety="Vernacular",
                protected_attribute="group_b",
                expected_output="URGENT",
                observed_output="LOW_PRIORITY",
                confidence_score=0.4,
            ),
        ],
        metadata={"human_in_the_loop": False},
    )

    assessment: FrameworkAssessment = evaluator.evaluate(scenario)

    assert assessment.framework == FrameworkType.EU_AI_ACT
    assert assessment.risk_tier == RiskTier.HIGH_RISK
    assert assessment.compliance_status in [
        ComplianceStatus.PARTIALLY_COMPLIANT,
        ComplianceStatus.NON_COMPLIANT,
    ]
    assert len(assessment.metrics) >= 3
    assert len(assessment.findings) > 0


def test_eu_ai_act_evaluator_unacceptable_risk() -> None:
    """EN: Verify EU AI Act evaluator flags prohibited domain practices. | ES: Verificar que el evaluador de la Ley de IA de la UE marque practicas de dominio prohibidas."""
    evaluator = EUAIActEvaluator()
    scenario = Scenario(
        id="prohibited-001",
        title="Social Scoring System",
        description="Linguistic scoring of citizen social trustworthiness.",
        domain_category="social_scoring",
        task_type=TaskType.TEXT_CLASSIFICATION,
        artifacts=[],
        metadata={},
    )

    assessment = evaluator.evaluate(scenario)
    assert assessment.risk_tier == RiskTier.UNACCEPTABLE_RISK
    assert assessment.compliance_status == ComplianceStatus.PROHIBITED
    assert any(f.severity == "CRITICAL" for f in assessment.findings)


def test_ieee_standards_evaluator_transparency() -> None:
    """EN: Test IEEE 7000/7001 evaluator calculates transparency deficit correctly. | ES: Probar que el evaluador IEEE 7000/7001 calcule el deficit de transparencia correctamente."""
    evaluator = IEEEStandardsEvaluator()
    assert evaluator.framework == FrameworkType.IEEE_7000_SERIES

    scenario = Scenario(
        id="ieee-test-001",
        title="Translation System",
        description="Translation without explainability.",
        domain_category="general_translation",
        task_type=TaskType.MACHINE_TRANSLATION,
        artifacts=[
            LinguisticArtifact(
                text_sample="Hello world",
                dialect_or_variety="English",
                protected_attribute="default",
                expected_output="Hola mundo",
                observed_output="Hola mundo",
                confidence_score=0.92,
            )
        ],
        metadata={
            "explainability_enabled": False,
            "confidence_scores_visible": False,
            "toxicity_exposure_rate": 0.05,
        },
    )

    assessment = evaluator.evaluate(scenario)
    assert assessment.framework == FrameworkType.IEEE_7000_SERIES
    transparency_metric = next(
        (m for m in assessment.metrics if m.name == "Algorithmic Transparency Index"),
        None,
    )
    assert transparency_metric is not None
    assert not transparency_metric.passed
