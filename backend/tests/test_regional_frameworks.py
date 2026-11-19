"""EN: Contract tests for regional regulatory framework evaluators. | ES: Pruebas de contrato para los evaluadores de marcos regulatorios regionales."""

import pytest

from domain.entities import (
    BindingLevel,
    ComplianceStatus,
    FrameworkRegion,
    FrameworkType,
    LinguisticArtifact,
    RiskTier,
    Scenario,
    TaskType,
)
from domain.frameworks import (
    AUContinentalAIEvaluator,
    BrazilPL2338Evaluator,
    ChinaAIRegulationsEvaluator,
    CoEAIConventionEvaluator,
    ColoradoAIActEvaluator,
    IndiaDPDPAIEvaluator,
    ISO42001Evaluator,
    JapanAIActEvaluator,
    KoreaAIBasicActEvaluator,
    NISTAIRMFEvaluator,
    PeruAILaw31814Evaluator,
    SingaporeAIGovernanceEvaluator,
    UKAIGovernanceEvaluator,
    build_default_evaluators,
)
from domain.interfaces import IEthicalEvaluator

# EN: (evaluator class, framework, region, binding level) | ES: (clase evaluadora, marco, region, nivel de vinculacion)
REGIONAL_CASES = [
    (UKAIGovernanceEvaluator, FrameworkType.UK_AI_GOVERNANCE, FrameworkRegion.EUROPE, BindingLevel.VOLUNTARY_STANDARD),
    (CoEAIConventionEvaluator, FrameworkType.COE_AI_CONVENTION, FrameworkRegion.EUROPE, BindingLevel.LEGALLY_BINDING),
    (NISTAIRMFEvaluator, FrameworkType.NIST_AI_RMF, FrameworkRegion.AMERICAS, BindingLevel.VOLUNTARY_STANDARD),
    (ColoradoAIActEvaluator, FrameworkType.COLORADO_AI_ACT, FrameworkRegion.AMERICAS, BindingLevel.LEGALLY_BINDING),
    (BrazilPL2338Evaluator, FrameworkType.BRAZIL_PL_2338, FrameworkRegion.AMERICAS, BindingLevel.PROPOSED_LEGISLATION),
    (PeruAILaw31814Evaluator, FrameworkType.PERU_AI_LAW_31814, FrameworkRegion.AMERICAS, BindingLevel.LEGALLY_BINDING),
    (KoreaAIBasicActEvaluator, FrameworkType.KOREA_AI_BASIC_ACT, FrameworkRegion.ASIA_PACIFIC, BindingLevel.LEGALLY_BINDING),
    (ChinaAIRegulationsEvaluator, FrameworkType.CHINA_AI_REGULATIONS, FrameworkRegion.ASIA_PACIFIC, BindingLevel.LEGALLY_BINDING),
    (JapanAIActEvaluator, FrameworkType.JAPAN_AI_ACT, FrameworkRegion.ASIA_PACIFIC, BindingLevel.VOLUNTARY_STANDARD),
    (SingaporeAIGovernanceEvaluator, FrameworkType.SINGAPORE_AI_GOVERNANCE, FrameworkRegion.ASIA_PACIFIC, BindingLevel.VOLUNTARY_STANDARD),
    (IndiaDPDPAIEvaluator, FrameworkType.INDIA_DPDP_AI, FrameworkRegion.ASIA_PACIFIC, BindingLevel.LEGALLY_BINDING),
    (AUContinentalAIEvaluator, FrameworkType.AU_CONTINENTAL_AI, FrameworkRegion.AFRICA, BindingLevel.VOLUNTARY_STANDARD),
    (ISO42001Evaluator, FrameworkType.ISO_IEC_42001, FrameworkRegion.INTERNATIONAL, BindingLevel.VOLUNTARY_STANDARD),
]


def _biased_triage_scenario() -> Scenario:
    """EN: High-impact clinical scenario with a dialectal accuracy gap. | ES: Escenario clinico de alto impacto con brecha de exactitud dialectal."""
    return Scenario(
        id="regional-triage-001",
        title="Emergency Triage",
        description="Clinical triage with dialectal disparity.",
        domain_category="clinical_triage",
        task_type=TaskType.CLINICAL_TRIAGE,
        artifacts=[
            LinguisticArtifact("Severe pain in chest.", "Formal", "group_a", "URGENT", "URGENT", 0.9),
            LinguisticArtifact("Hurts real bad.", "Vernacular", "group_b", "URGENT", "LOW_PRIORITY", 0.4),
        ],
        metadata={"human_in_the_loop": False},
    )


def _prohibited_scenario() -> Scenario:
    """EN: Social scoring scenario falling into a prohibited domain. | ES: Escenario de puntuacion social perteneciente a un dominio prohibido."""
    return Scenario(
        id="regional-prohibited-001",
        title="Social Scoring System",
        description="Linguistic scoring of citizen trustworthiness.",
        domain_category="social_scoring",
        task_type=TaskType.TEXT_CLASSIFICATION,
        artifacts=[],
        metadata={},
    )


@pytest.mark.parametrize(("evaluator_cls", "framework", "region", "binding"), REGIONAL_CASES)
def test_regional_evaluator_metadata_contract(
    evaluator_cls: type[IEthicalEvaluator],
    framework: FrameworkType,
    region: FrameworkRegion,
    binding: BindingLevel,
) -> None:
    """EN: Each evaluator reports its framework, region and binding level. | ES: Cada evaluador informa su marco, region y nivel de vinculacion."""
    evaluator = evaluator_cls()
    assessment = evaluator.evaluate(_biased_triage_scenario())

    assert evaluator.framework == framework
    assert assessment.framework == framework
    assert assessment.region == region
    assert assessment.binding_level == binding
    assert len(assessment.metrics) > 0
    assert len(assessment.recommendations) > 0
    assert all(f.framework == framework for f in assessment.findings)


@pytest.mark.parametrize(("evaluator_cls", "framework", "region", "binding"), REGIONAL_CASES)
def test_alignment_status_only_for_non_binding_frameworks(
    evaluator_cls: type[IEthicalEvaluator],
    framework: FrameworkType,
    region: FrameworkRegion,
    binding: BindingLevel,
) -> None:
    """EN: Alignment verdict is set only for soft-law or proposed frameworks. | ES: El veredicto de alineacion solo se fija en marcos de soft-law o propuestos."""
    assessment = evaluator_cls().evaluate(_biased_triage_scenario())

    if binding == BindingLevel.LEGALLY_BINDING:
        assert assessment.alignment_status is None
    else:
        assert assessment.alignment_status is not None


@pytest.mark.parametrize(
    "evaluator_cls",
    [BrazilPL2338Evaluator, ChinaAIRegulationsEvaluator, CoEAIConventionEvaluator, PeruAILaw31814Evaluator],
)
def test_prohibited_domain_yields_unacceptable_risk(
    evaluator_cls: type[IEthicalEvaluator],
) -> None:
    """EN: Frameworks with explicit prohibitions flag social scoring. | ES: Los marcos con prohibiciones explicitas marcan la puntuacion social."""
    assessment = evaluator_cls().evaluate(_prohibited_scenario())

    assert assessment.risk_tier == RiskTier.UNACCEPTABLE_RISK
    assert assessment.compliance_status == ComplianceStatus.PROHIBITED


def test_default_registry_covers_every_framework_type() -> None:
    """EN: The default registry instantiates exactly one evaluator per FrameworkType. | ES: El registro por defecto instancia exactamente un evaluador por FrameworkType."""
    evaluators = build_default_evaluators()
    frameworks = [e.framework for e in evaluators]

    assert all(isinstance(e, IEthicalEvaluator) for e in evaluators)
    assert len(frameworks) == len(set(frameworks))
    assert set(frameworks) == set(FrameworkType)
