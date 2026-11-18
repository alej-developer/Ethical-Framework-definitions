"""EN: In-memory repository implementations seeded with complex computational linguistics case studies. | ES: Implementaciones de repositorios en memoria inicializadas con casos de estudio complejos de linguistica computacional."""

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
from domain.interfaces import (
    IAssessmentRepository,
    ICaseStudyRepository,
    IDecisionImpactRepository,
    IScenarioRepository,
)


class InMemoryCaseStudyRepository(ICaseStudyRepository):
    """EN: In-memory storage for complex NLP case studies and ethical dilemmas. | ES: Almacenamiento en memoria para casos de estudio complejos de NLP y dilemas eticos."""

    def __init__(self) -> None:
        self._cases: dict[str, CaseStudy] = {}
        self._seed_case_studies()

    def get_by_id(self, case_id: str) -> CaseStudy | None:
        """EN: Retrieve case study by unique identifier. | ES: Recuperar caso de estudio por identificador unico."""
        return self._cases.get(case_id)

    def list_all(self) -> list[CaseStudy]:
        """EN: Return all registered case studies. | ES: Retornar todos los casos de estudio registrados."""
        return list(self._cases.values())

    def save(self, case_study: CaseStudy) -> None:
        """EN: Save or update a case study. | ES: Guardar o actualizar un caso de estudio."""
        self._cases[case_study.id] = case_study

    def _seed_case_studies(self) -> None:
        """EN: Seed three complex computational linguistics case studies. | ES: Inicializar tres casos de estudio complejos de linguistica computacional."""

        # EN: Case Study 1: LLM Demographic Bias in Recruitment Parsing | ES: Caso 1: Sesgo demografico de LLM en analisis de contratacion
        case_1 = CaseStudy(
            id="cs-recruitment-llm-001",
            title="LLM Demographic Bias in Automated Recruitment Parsing",
            nlp_domain="Automated Resume Information Extraction & Candidate Ranking",
            dilemma=(
                "An enterprise deployed an automated LLM to score and rank 50,000 monthly job applications. "
                "The model exhibits severe disparate impact, systematically downgrading CVs exhibiting African American "
                "Vernacular English (AAVE) syntax or mentioning historically marginalized institutions, creating severe "
                "regulatory exposure under EU AI Act Annex III and Title VII."
            ),
            context_description=(
                "The hiring engineering organization implemented zero-shot LLM parsing to accelerate screening. "
                "Semantic latent embedding analysis reveals that vernacular dialect phrases are systematically clustered "
                "with lower competency scores, despite identical technical qualifications."
            ),
            task_type=TaskType.TEXT_CLASSIFICATION,
            domain_category="recruitment",
            baseline_matrix={
                EthicalDimension.TRANSPARENCY: 0.35,
                EthicalDimension.ACCOUNTABILITY: 0.40,
                EthicalDimension.FAIRNESS: 0.30,
            },
            decision_options=[
                DecisionOption(
                    id="opt-recruit-status-quo",
                    title="Deploy Status Quo for Throughput Velocity",
                    description="Maintain current unmitigated LLM deployment to eliminate application backlog.",
                    strategy="Throughput Maximization",
                    dimension_modifiers={
                        EthicalDimension.TRANSPARENCY: -0.10,
                        EthicalDimension.ACCOUNTABILITY: -0.15,
                        EthicalDimension.FAIRNESS: -0.15,
                    },
                    rationale="Prioritizes processing volume at the cost of cementing institutional discrimination.",
                ),
                DecisionOption(
                    id="opt-recruit-heuristic-masking",
                    title="Apply Heuristic Demographic Entity Masking",
                    description="Redact explicit personal identifying names and postal codes via regular expressions.",
                    strategy="Surface Heuristic Redaction",
                    dimension_modifiers={
                        EthicalDimension.TRANSPARENCY: +0.15,
                        EthicalDimension.ACCOUNTABILITY: +0.10,
                        EthicalDimension.FAIRNESS: +0.20,
                    },
                    rationale="Redacts surface tokens but leaves latent dialectal syntactic representations unaddressed.",
                ),
                DecisionOption(
                    id="opt-recruit-fairness-oversight",
                    title="Counterfactual Augmentation & Mandatory Human Oversight",
                    description=(
                        "Fine-tune parser with counterfactual dialect pairs, require transparent skill rationale scores, "
                        "and establish mandatory dual recruiter review prior to any candidate exclusion."
                    ),
                    strategy="Comprehensive Value-Aligned Oversight",
                    dimension_modifiers={
                        EthicalDimension.TRANSPARENCY: +0.45,
                        EthicalDimension.ACCOUNTABILITY: +0.45,
                        EthicalDimension.FAIRNESS: +0.55,
                    },
                    rationale="Directly mitigates disparate impact, establishes explainability, and satisfies EU AI Act Article 14.",
                ),
            ],
            linguistic_artifacts=[
                LinguisticArtifact(
                    text_sample="Managed microservices architecture on AWS. They be having zero downtime in production.",
                    dialect_or_variety="AAVE",
                    protected_attribute="ethnicity_proxy_vernacular",
                    expected_output="QUALIFIED_SENIOR",
                    observed_output="JUNIOR_REVISE",
                    confidence_score=0.68,
                ),
                LinguisticArtifact(
                    text_sample="Architected cloud infrastructure on AWS. Ensured continuous zero downtime in production.",
                    dialect_or_variety="SAE",
                    protected_attribute="ethnicity_proxy_standard",
                    expected_output="QUALIFIED_SENIOR",
                    observed_output="QUALIFIED_SENIOR",
                    confidence_score=0.96,
                ),
                LinguisticArtifact(
                    text_sample="President of the Society of Women Engineers, led distributed backend migration.",
                    dialect_or_variety="SAE_Affiliation_Disclosed",
                    protected_attribute="gender_proxy_female",
                    expected_output="QUALIFIED_SENIOR",
                    observed_output="QUALIFIED_MID",
                    confidence_score=0.74,
                ),
                LinguisticArtifact(
                    text_sample="Led distributed backend migration across multiple enterprise cloud regions.",
                    dialect_or_variety="SAE_Neutral",
                    protected_attribute="gender_proxy_neutral",
                    expected_output="QUALIFIED_SENIOR",
                    observed_output="QUALIFIED_SENIOR",
                    confidence_score=0.95,
                ),
            ],
            regulatory_implications={
                "EU_AI_Act": "Classified as High-Risk AI System under Annex III (Employment, workers management and access to self-employment).",
                "IEEE_7000": "Violates Clause 5.3 (Procedural Fairness) and IEEE 7010 well-being economic dimensions.",
                "GDPR": "Article 22 mandates right not to be subject to solely automated decision making producing legal effects.",
            },
            metadata={
                "provenance_verified": True,
                "explainability_enabled": False,
                "confidence_scores_visible": True,
                "toxicity_exposure_rate": 0.05,
                "human_in_the_loop": False,
            },
        )

        # EN: Case Study 2: Stylistic Profiling in Forensic Linguistics | ES: Caso 2: Perfilado estilistico en linguistica forense
        case_2 = CaseStudy(
            id="cs-forensic-stylometry-002",
            title="Stylistic Profiling and Authorship Attribution in Forensic Linguistics",
            nlp_domain="Forensic Authorship Identification & Sociolect Analysis",
            dilemma=(
                "Law enforcement authorities seek to deploy automated stylometric text attribution algorithms to identify "
                "the authors of anonymous manifestos and whistleblowing documents. The classifier exhibits high error rates "
                "when analyzing multilingual individuals and regional sociolects, creating severe risks of wrongful indictment "
                "and chilling protected political expression."
            ),
            context_description=(
                "Following an unauthorized disclosure of public corruption records, state investigators cross-reference "
                "the communiqué against employee communications. The stylometry engine attributes the document to a bilingual "
                "worker with a Nigerian English linguistic repertoire based on idiosyncratic syntactic frequency."
            ),
            task_type=TaskType.TEXT_CLASSIFICATION,
            domain_category="law_enforcement",
            baseline_matrix={
                EthicalDimension.TRANSPARENCY: 0.25,
                EthicalDimension.ACCOUNTABILITY: 0.30,
                EthicalDimension.FAIRNESS: 0.35,
            },
            decision_options=[
                DecisionOption(
                    id="opt-forensic-auto-arrest",
                    title="Automated Probable Cause Determination",
                    description="Authorize search warrants and arrest procedures directly when attribution confidence exceeds 80%.",
                    strategy="Automated Coercive Action",
                    dimension_modifiers={
                        EthicalDimension.TRANSPARENCY: -0.15,
                        EthicalDimension.ACCOUNTABILITY: -0.25,
                        EthicalDimension.FAIRNESS: -0.25,
                    },
                    rationale="Extreme violation of procedural justice, presumption of innocence, and due process.",
                ),
                DecisionOption(
                    id="opt-forensic-closed-expert",
                    title="Proprietary Forensic Expert Testimony",
                    description="Permit state witnesses to introduce model findings in court without disclosing feature weights or dialect error rates.",
                    strategy="Unchecked Forensic Heuristics",
                    dimension_modifiers={
                        EthicalDimension.TRANSPARENCY: +0.10,
                        EthicalDimension.ACCOUNTABILITY: +0.10,
                        EthicalDimension.FAIRNESS: +0.05,
                    },
                    rationale="Deprives defendants of epistemic cross-examination rights and obscures systemic dialectal bias.",
                ),
                DecisionOption(
                    id="opt-forensic-scientific-transparency",
                    title="Daubert Scientific Transparency & Investigative-Only Protocol",
                    description=(
                        "Restrict algorithm strictly to non-binding investigative leads; mandate open dialectal error margins, "
                        "open-source feature distributions, and corroboration by independent accredited forensic linguists."
                    ),
                    strategy="Scientific Rigor & Evidentiary Accountability",
                    dimension_modifiers={
                        EthicalDimension.TRANSPARENCY: +0.60,
                        EthicalDimension.ACCOUNTABILITY: +0.55,
                        EthicalDimension.FAIRNESS: +0.50,
                    },
                    rationale="Satisfies scientific evidentiary standards, preserves fair trial guarantees, and protects linguistic minorities.",
                ),
            ],
            linguistic_artifacts=[
                LinguisticArtifact(
                    text_sample="The governance apparatus must account for diverted regional development appropriations.",
                    dialect_or_variety="Nigerian_English_CodeSwitch",
                    protected_attribute="nationality_minority",
                    expected_output="UNKNOWN_OR_INCONCLUSIVE",
                    observed_output="ATTRIBUTED_SUSPECT_4",
                    confidence_score=0.88,
                ),
                LinguisticArtifact(
                    text_sample="Official documents indicate systematic budget transfers away from municipal services.",
                    dialect_or_variety="British_English_Standard",
                    protected_attribute="nationality_majority",
                    expected_output="UNKNOWN_OR_INCONCLUSIVE",
                    observed_output="UNKNOWN_OR_INCONCLUSIVE",
                    confidence_score=0.91,
                ),
            ],
            regulatory_implications={
                "EU_AI_Act": "Article 5 and Annex III strictly regulate biometric and individual risk assessment tools in law enforcement.",
                "IEEE_7001": "Requires verifiable transparency and explainability for forensic decision-support systems.",
                "ECHR": "Article 6 guarantees right to a fair trial and adversarial equality of arms.",
            },
            metadata={
                "provenance_verified": True,
                "explainability_enabled": False,
                "confidence_scores_visible": False,
                "toxicity_exposure_rate": 0.08,
                "human_in_the_loop": False,
            },
        )

        # EN: Case Study 3: Dataset Provenance Gaps in Foundation Models | ES: Caso 3: Brechas de procedencia de datos en modelos base
        case_3 = CaseStudy(
            id="cs-dataset-provenance-003",
            title="Dataset Provenance Gaps and Non-Consensual Web Scraping in Foundation Models",
            nlp_domain="Foundation Language Model Pre-training Corpus Curation",
            dilemma=(
                "An AI laboratory is compiling a 700-billion-token pre-training corpus for a commercial conversational LLM. "
                "The web scraping pipeline harvested clinical self-help message boards, creative literature repositories, "
                "and private discussion threads without author consent, opt-out infrastructure, or PII scrubbing, exposing "
                "the model to catastrophic data leaks, copyright claims, and regulatory sanctions."
            ),
            context_description=(
                "Facing competitive pressure to match market release schedules, management considers bypassing data "
                "curation, provenance tracing, and copyright licensing audits which would delay release by four months."
            ),
            task_type=TaskType.GENERATIVE_QA,
            domain_category="data_governance",
            baseline_matrix={
                EthicalDimension.TRANSPARENCY: 0.20,
                EthicalDimension.ACCOUNTABILITY: 0.25,
                EthicalDimension.FAIRNESS: 0.35,
            },
            decision_options=[
                DecisionOption(
                    id="opt-provenance-ignore-scale",
                    title="Ingest Web Scrapes at Maximum Scale",
                    description="Proceed with unvetted 700B token web scrape to maximize generative benchmarks and hit release deadlines.",
                    strategy="Unregulated Scaled Ingestion",
                    dimension_modifiers={
                        EthicalDimension.TRANSPARENCY: -0.10,
                        EthicalDimension.ACCOUNTABILITY: -0.15,
                        EthicalDimension.FAIRNESS: -0.15,
                    },
                    rationale="Sacrifices personal privacy and intellectual property rights for commercial delivery speed.",
                ),
                DecisionOption(
                    id="opt-provenance-reactive-optout",
                    title="Implement Reactive Web Takedown Portal",
                    description="Deploy model while providing a public URL form where authors may petition for post-hoc token unlearning.",
                    strategy="Reactive Compliance Shifting",
                    dimension_modifiers={
                        EthicalDimension.TRANSPARENCY: +0.20,
                        EthicalDimension.ACCOUNTABILITY: +0.20,
                        EthicalDimension.FAIRNESS: +0.10,
                    },
                    rationale="Places burden of proof onto harmed authors without guaranteeing complete weights unlearning.",
                ),
                DecisionOption(
                    id="opt-provenance-rigorous-governance",
                    title="Exhaustive Provenance Audit, PII Redaction & Consensual Licensing",
                    description=(
                        "Implement verifiable Datasheets for Datasets, automated differential privacy scrubbing, "
                        "formal copyright licensing compacts, and transparent demographic representation logging."
                    ),
                    strategy="Responsible Corpus Stewardship",
                    dimension_modifiers={
                        EthicalDimension.TRANSPARENCY: +0.65,
                        EthicalDimension.ACCOUNTABILITY: +0.60,
                        EthicalDimension.FAIRNESS: +0.50,
                    },
                    rationale="Ensures full compliance with EU AI Act Article 10/53, GDPR principles, and IEEE 7000 value alignment.",
                ),
            ],
            linguistic_artifacts=[
                LinguisticArtifact(
                    text_sample="Patient disclosure on private medical forum regarding hereditary autoimmune diagnosis.",
                    dialect_or_variety="Private_Medical_Forum",
                    protected_attribute="health_data_special_category",
                    expected_output="REDACTED_OR_EXCLUDED",
                    observed_output="EXPOSED_VERBATIM_IN_PRETRAIN",
                    confidence_score=0.45,
                ),
                LinguisticArtifact(
                    text_sample="Excerpt from copyrighted contemporary novel serialized on indie author site.",
                    dialect_or_variety="Creative_Literature",
                    protected_attribute="copyright_holder_individual",
                    expected_output="LICENSED_OR_EXCLUDED",
                    observed_output="MEMORIZED_VERBATIM_OUTPUT",
                    confidence_score=0.55,
                ),
            ],
            regulatory_implications={
                "EU_AI_Act": "Article 10 (Data and data governance) and Article 53 (Transparency requirements for general-purpose AI).",
                "GDPR": "Article 6 (Lawfulness of processing) and Article 9 (Special categories of personal data).",
                "IEEE_7000": "Mandates stakeholder consent, non-maleficence, and fair attribution.",
            },
            metadata={
                "provenance_verified": False,
                "explainability_enabled": False,
                "confidence_scores_visible": True,
                "toxicity_exposure_rate": 0.25,
                "human_in_the_loop": False,
            },
        )

        self._cases[case_1.id] = case_1
        self._cases[case_2.id] = case_2
        self._cases[case_3.id] = case_3


class InMemoryScenarioRepository(IScenarioRepository):
    """EN: In-memory store for computational linguistics evaluation scenarios. | ES: Almacenamiento en memoria para escenarios de evaluacion de linguistica computacional."""

    def __init__(self, case_repo: InMemoryCaseStudyRepository | None = None) -> None:
        self._scenarios: dict[str, Scenario] = {}
        # EN: Seed from case study repository for unified scenario availability | ES: Inicializar desde repositorio de casos para disponibilidad unificada de escenarios
        if case_repo is not None:
            for case in case_repo.list_all():
                self._scenarios[case.id] = case.to_scenario()
        else:
            self._seed_default_scenarios()

    def get_by_id(self, scenario_id: str) -> Scenario | None:
        return self._scenarios.get(scenario_id)

    def list_all(self) -> list[Scenario]:
        return list(self._scenarios.values())

    def save(self, scenario: Scenario) -> None:
        self._scenarios[scenario.id] = scenario

    def _seed_default_scenarios(self) -> None:
        cases_repo = InMemoryCaseStudyRepository()
        for case in cases_repo.list_all():
            self._scenarios[case.id] = case.to_scenario()


class InMemoryAssessmentRepository(IAssessmentRepository):
    """EN: In-memory store for finalized ethical evaluations. | ES: Almacenamiento en memoria para evaluaciones eticas finalizadas."""

    def __init__(self) -> None:
        self._assessments: dict[str, EthicalAssessment] = {}

    def save(self, assessment: EthicalAssessment) -> None:
        self._assessments[assessment.id] = assessment

    def get_by_id(self, assessment_id: str) -> EthicalAssessment | None:
        return self._assessments.get(assessment_id)

    def list_by_scenario(self, scenario_id: str) -> list[EthicalAssessment]:
        return [a for a in self._assessments.values() if a.scenario_id == scenario_id]


class InMemoryDecisionImpactRepository(IDecisionImpactRepository):
    """EN: In-memory store for decision impact assessment records. | ES: Almacenamiento en memoria para registros de evaluacion de impacto de decision."""

    def __init__(self) -> None:
        self._results: dict[str, DecisionImpactResult] = {}

    def save(self, result: DecisionImpactResult) -> None:
        self._results[result.decision_id] = result

    def get_by_id(self, decision_id: str) -> DecisionImpactResult | None:
        return self._results.get(decision_id)

    def list_by_case(self, case_id: str) -> list[DecisionImpactResult]:
        return [r for r in self._results.values() if r.case_id == case_id]
