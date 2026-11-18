"""EN: Unit tests verifying complex NLP case studies and domain model integrity. | ES: Pruebas unitarias que verifican casos de estudio complejos de NLP e integridad del modelo de dominio."""

from domain.entities import EthicalDimension
from infrastructure.repositories.in_memory_repository import InMemoryCaseStudyRepository


def test_seeded_case_studies_completeness() -> None:
    """EN: Verify that all three complex NLP case studies are correctly seeded and configured. | ES: Verificar que los tres casos de estudio complejos de NLP esten correctamente inicializados y configurados."""
    repo = InMemoryCaseStudyRepository()
    cases = repo.list_all()

    assert len(cases) == 3
    case_ids = {c.id for c in cases}
    assert "cs-recruitment-llm-001" in case_ids
    assert "cs-forensic-stylometry-002" in case_ids
    assert "cs-dataset-provenance-003" in case_ids

    for case in cases:
        assert len(case.title) > 5
        assert len(case.dilemma) > 20
        assert len(case.decision_options) >= 3
        assert len(case.linguistic_artifacts) >= 2
        assert len(case.regulatory_implications) >= 2

        # EN: Verify baseline matrix contains all 3 pillars | ES: Verificar que la matriz base contenga los 3 pilares
        for dim in EthicalDimension:
            assert dim in case.baseline_matrix
            assert 0.0 <= case.baseline_matrix[dim] <= 1.0

        # EN: Verify to_scenario conversion | ES: Verificar conversion to_scenario
        scenario = case.to_scenario()
        assert scenario.id == case.id
        assert scenario.title == case.title
        assert len(scenario.artifacts) == len(case.linguistic_artifacts)


def test_recruitment_case_study_options() -> None:
    """EN: Test recruitment parsing case study has specific value-aligned option. | ES: Probar que el caso de estudio de analisis de contratacion tenga una opcion especifica alineada con valores."""
    repo = InMemoryCaseStudyRepository()
    case = repo.get_by_id("cs-recruitment-llm-001")
    assert case is not None

    option_ids = [o.id for o in case.decision_options]
    assert "opt-recruit-status-quo" in option_ids
    assert "opt-recruit-heuristic-masking" in option_ids
    assert "opt-recruit-fairness-oversight" in option_ids

    oversight_opt = next(o for o in case.decision_options if o.id == "opt-recruit-fairness-oversight")
    assert oversight_opt.dimension_modifiers[EthicalDimension.FAIRNESS] > 0.40
    assert oversight_opt.dimension_modifiers[EthicalDimension.ACCOUNTABILITY] > 0.40


def test_forensic_stylometry_case_study() -> None:
    """EN: Test forensic stylometry case study has scientific transparency option. | ES: Probar que el caso de estudio de estilometria forense tenga la opcion de transparencia cientifica."""
    repo = InMemoryCaseStudyRepository()
    case = repo.get_by_id("cs-forensic-stylometry-002")
    assert case is not None
    assert case.domain_category == "law_enforcement"

    option = next(o for o in case.decision_options if o.id == "opt-forensic-scientific-transparency")
    assert option.dimension_modifiers[EthicalDimension.TRANSPARENCY] >= 0.50


def test_dataset_provenance_case_study() -> None:
    """EN: Test dataset provenance case study and governance option. | ES: Probar caso de estudio de procedencia de datos y opcion de gobernanza."""
    repo = InMemoryCaseStudyRepository()
    case = repo.get_by_id("cs-dataset-provenance-003")
    assert case is not None

    option = next(o for o in case.decision_options if o.id == "opt-provenance-rigorous-governance")
    assert option.dimension_modifiers[EthicalDimension.ACCOUNTABILITY] >= 0.50
