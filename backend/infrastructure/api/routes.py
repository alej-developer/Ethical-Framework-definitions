"""EN: FastAPI route definitions for case studies, decisions, evaluations, and health endpoints. | ES: Definiciones de rutas FastAPI para casos de estudio, decisiones, evaluaciones y puntos finales de salud."""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status

from application.dtos import (
    CaseStudyDTO,
    CaseStudySummaryDTO,
    DecisionImpactResponseDTO,
    EthicalAssessmentDTO,
    EvaluateScenarioRequest,
    ScenarioDTO,
    SubmitDecisionRequest,
)
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
from domain.entities import BindingLevel, FrameworkRegion, FrameworkType
from domain.frameworks import build_default_evaluators
from infrastructure.repositories.in_memory_repository import (
    InMemoryAssessmentRepository,
    InMemoryCaseStudyRepository,
    InMemoryDecisionImpactRepository,
    InMemoryScenarioRepository,
)

router = APIRouter(prefix="/api/v1", tags=["AI Ethics Simulator"])

# EN: Singleton persistence and evaluator services for dependency injection | ES: Servicios de evaluacion y persistencia unicos para inyeccion de dependencias
_case_study_repo = InMemoryCaseStudyRepository()
_scenario_repo = InMemoryScenarioRepository(_case_study_repo)
_assessment_repo = InMemoryAssessmentRepository()
_decision_impact_repo = InMemoryDecisionImpactRepository()
_matrix_evaluator = MatrixEvaluator()
_composite_evaluator = CompositeEvaluator(evaluators=build_default_evaluators())


# EN: Dependency provider functions | ES: Funciones proveedoras de dependencias


def get_list_case_studies_use_case() -> ListCaseStudiesUseCase:
    """EN: Dependency provider for ListCaseStudiesUseCase. | ES: Proveedor de dependencia para ListCaseStudiesUseCase."""
    return ListCaseStudiesUseCase(_case_study_repo)


def get_case_study_use_case() -> GetCaseStudyUseCase:
    """EN: Dependency provider for GetCaseStudyUseCase. | ES: Proveedor de dependencia para GetCaseStudyUseCase."""
    return GetCaseStudyUseCase(_case_study_repo)


def get_submit_decision_use_case() -> SubmitDecisionUseCase:
    """EN: Dependency provider for SubmitDecisionUseCase. | ES: Proveedor de dependencia para SubmitDecisionUseCase."""
    return SubmitDecisionUseCase(
        case_study_repository=_case_study_repo,
        decision_impact_repository=_decision_impact_repo,
        matrix_evaluator=_matrix_evaluator,
        composite_evaluator=_composite_evaluator,
    )


def get_decision_impact_use_case() -> GetDecisionImpactUseCase:
    """EN: Dependency provider for GetDecisionImpactUseCase. | ES: Proveedor de dependencia para GetDecisionImpactUseCase."""
    return GetDecisionImpactUseCase(_decision_impact_repo)


def get_list_scenarios_use_case() -> ListScenariosUseCase:
    """EN: Dependency provider for ListScenariosUseCase. | ES: Proveedor de dependencia para ListScenariosUseCase."""
    return ListScenariosUseCase(_scenario_repo)


def get_scenario_use_case() -> GetScenarioUseCase:
    """EN: Dependency provider for GetScenarioUseCase. | ES: Proveedor de dependencia para GetScenarioUseCase."""
    return GetScenarioUseCase(_scenario_repo)


def get_evaluate_scenario_use_case() -> EvaluateScenarioUseCase:
    """EN: Dependency provider for EvaluateScenarioUseCase. | ES: Proveedor de dependencia para EvaluateScenarioUseCase."""
    return EvaluateScenarioUseCase(
        scenario_repository=_scenario_repo,
        assessment_repository=_assessment_repo,
        composite_evaluator=_composite_evaluator,
    )


# EN: Health and Metadata Endpoints | ES: Puntos Finales de Salud y Metadatos


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="EN: Health Check Probe | ES: Sondeo de Verificacion de Salud",
    description="EN: Returns service operational readiness and architectural compliance. | ES: Retorna la preparacion operativa del servicio y cumplimiento arquitectonico.",
)
def health_check() -> dict[str, str]:
    """EN: Health check probe verifying service responsiveness. | ES: Sondeo de verificacion de salud que valida la capacidad de respuesta del servicio."""
    return {
        "status": "healthy",
        "service": "ai-ethics-simulator-backend",
        "architecture": "Clean Architecture / SOLID",
    }


@router.get(
    "/frameworks",
    status_code=status.HTTP_200_OK,
    summary="EN: List Supported Ethical Frameworks | ES: Listar Marcos Eticos Soportados",
    description="EN: Returns metadata regarding supported statutory and technical AI ethics frameworks. | ES: Retorna metadatos sobre los marcos estatutarios y tecnicos de etica en IA soportados.",
)
def list_frameworks() -> list[dict[str, Any]]:
    """EN: Return metadata and descriptions for supported ethical evaluation frameworks. | ES: Retornar metadatos y descripciones para los marcos de evaluacion etica soportados."""
    return [{"id": framework.value, **FRAMEWORK_CATALOGUE[framework]} for framework in FrameworkType]


@router.get(
    "/frameworks/reference",
    status_code=status.HTTP_200_OK,
    summary="EN: List Global Reference AI Legislation | ES: Listar Legislacion Global de IA de Consulta",
    description="EN: Returns a curated consultation catalogue of additional global AI laws, bills, strategies and international instruments outside the 15 executable evaluators. | ES: Retorna un catalogo de consulta con legislaciones, proyectos de ley, estrategias e instrumentos internacionales adicionales de IA fuera de los 15 evaluadores ejecutables.",
)
def list_reference_frameworks() -> list[dict[str, Any]]:
    """EN: Return consultation-only global AI legislation catalogue. | ES: Retornar catalogo global de legislacion de IA solo para consulta."""
    return GLOBAL_REFERENCE_LEGISLATION


# EN: Presentation metadata per framework; must cover every FrameworkType | ES: Metadatos de presentacion por marco; debe cubrir todos los FrameworkType
FRAMEWORK_CATALOGUE: dict[FrameworkType, dict[str, Any]] = {
    FrameworkType.EU_AI_ACT: {
        "name": "EU Artificial Intelligence Act (Regulation EU 2024/1689)",
        "jurisdiction": "European Union",
        "region": FrameworkRegion.EUROPE.value,
        "binding_level": BindingLevel.LEGALLY_BINDING.value,
        "focus_areas": [
            "Prohibited AI practices",
            "High-risk computational linguistics (Annex III)",
            "Data governance & dialectal non-discrimination (Article 10)",
            "Linguistic transparency & watermarking (Article 50)",
        ],
    },
    FrameworkType.UK_AI_GOVERNANCE: {
        "name": "UK Pro-Innovation AI Regulation Principles (DSIT White Paper, 2023)",
        "jurisdiction": "United Kingdom",
        "region": FrameworkRegion.EUROPE.value,
        "binding_level": BindingLevel.VOLUNTARY_STANDARD.value,
        "focus_areas": [
            "Safety, security & robustness",
            "Appropriate transparency & explainability",
            "Fairness across linguistic varieties",
            "Accountability & governance",
            "Contestability & redress",
        ],
    },
    FrameworkType.COE_AI_CONVENTION: {
        "name": "Council of Europe Framework Convention on AI (CETS No. 225, 2024)",
        "jurisdiction": "Council of Europe (International Treaty)",
        "region": FrameworkRegion.EUROPE.value,
        "binding_level": BindingLevel.LEGALLY_BINDING.value,
        "focus_areas": [
            "Human rights, democracy & rule of law",
            "Equality & non-discrimination (Article 10)",
            "Procedural safeguards & effective remedies (Articles 14-15)",
            "Privacy & data governance (Article 11)",
        ],
    },
    FrameworkType.NIST_AI_RMF: {
        "name": "NIST AI Risk Management Framework 1.0 (NIST AI 100-1)",
        "jurisdiction": "United States",
        "region": FrameworkRegion.AMERICAS.value,
        "binding_level": BindingLevel.VOLUNTARY_STANDARD.value,
        "focus_areas": [
            "GOVERN, MAP, MEASURE and MANAGE functions",
            "Validity, reliability & safety",
            "Accountability, transparency & explainability",
            "Harmful bias management",
        ],
    },
    FrameworkType.COLORADO_AI_ACT: {
        "name": "Colorado Artificial Intelligence Act (SB 24-205, 2024)",
        "jurisdiction": "United States (Colorado)",
        "region": FrameworkRegion.AMERICAS.value,
        "binding_level": BindingLevel.LEGALLY_BINDING.value,
        "focus_areas": [
            "Duty of reasonable care against algorithmic discrimination",
            "Consequential decisions (employment, healthcare, legal)",
            "Consumer notice & adverse decision explanations",
            "Right to human review & annual impact assessments",
        ],
    },
    FrameworkType.BRAZIL_PL_2338: {
        "name": "Brazil AI Bill (PL 2338/2023)",
        "jurisdiction": "Brazil",
        "region": FrameworkRegion.AMERICAS.value,
        "binding_level": BindingLevel.PROPOSED_LEGISLATION.value,
        "focus_areas": [
            "Excessive-risk prohibitions",
            "High-risk classification",
            "Algorithmic impact assessment",
            "Non-discrimination",
        ],
    },
    FrameworkType.PERU_AI_LAW_31814: {
        "name": "Peru AI Law (Ley N. 31814, 2023)",
        "jurisdiction": "Peru",
        "region": FrameworkRegion.AMERICAS.value,
        "binding_level": BindingLevel.LEGALLY_BINDING.value,
        "focus_areas": [
            "Risk-based AI governance",
            "Fundamental rights & non-discrimination",
            "Human supervision & citizen transparency",
            "Personal data governance",
        ],
    },
    FrameworkType.KOREA_AI_BASIC_ACT: {
        "name": "Korea Framework Act on AI Development and Establishment of Trust (AI Basic Act)",
        "jurisdiction": "Republic of Korea",
        "region": FrameworkRegion.ASIA_PACIFIC.value,
        "binding_level": BindingLevel.LEGALLY_BINDING.value,
        "focus_areas": [
            "AI use notice & generative content labeling",
            "Explanation of high-impact outcomes",
            "Human oversight of high-impact AI",
            "Fairness of outcomes",
        ],
    },
    FrameworkType.CHINA_AI_REGULATIONS: {
        "name": "China Generative AI, Deep Synthesis and AI Content Labeling Rules",
        "jurisdiction": "People's Republic of China",
        "region": FrameworkRegion.ASIA_PACIFIC.value,
        "binding_level": BindingLevel.LEGALLY_BINDING.value,
        "focus_areas": [
            "Synthetic content labeling",
            "Lawful training data",
            "Content safety",
            "Non-discrimination",
        ],
    },
    FrameworkType.JAPAN_AI_ACT: {
        "name": "Japan AI Promotion Act (2025) and AI Guidelines for Business",
        "jurisdiction": "Japan",
        "region": FrameworkRegion.ASIA_PACIFIC.value,
        "binding_level": BindingLevel.VOLUNTARY_STANDARD.value,
        "focus_areas": [
            "Human-centricity & safety",
            "Fairness",
            "Transparency to stakeholders",
            "Accountability & traceability",
        ],
    },
    FrameworkType.SINGAPORE_AI_GOVERNANCE: {
        "name": "Singapore Model AI Governance Framework (incl. Generative AI edition)",
        "jurisdiction": "Singapore",
        "region": FrameworkRegion.ASIA_PACIFIC.value,
        "binding_level": BindingLevel.VOLUNTARY_STANDARD.value,
        "focus_areas": [
            "Internal governance",
            "Human involvement proportionate to risk",
            "Operations management & bias minimisation",
            "Stakeholder communication",
        ],
    },
    FrameworkType.INDIA_DPDP_AI: {
        "name": "India Digital Personal Data Protection Act 2023 (applied to AI)",
        "jurisdiction": "India",
        "region": FrameworkRegion.ASIA_PACIFIC.value,
        "binding_level": BindingLevel.LEGALLY_BINDING.value,
        "focus_areas": [
            "Lawful consent & notice",
            "Data accuracy for automated decisions",
            "Correction, erasure & grievance rights",
        ],
    },
    FrameworkType.AU_CONTINENTAL_AI: {
        "name": "African Union Continental Artificial Intelligence Strategy (2024)",
        "jurisdiction": "African Union",
        "region": FrameworkRegion.AFRICA.value,
        "binding_level": BindingLevel.VOLUNTARY_STANDARD.value,
        "focus_areas": [
            "Linguistic & cultural inclusion for underrepresented varieties",
            "Data sovereignty & Malabo Convention alignment",
            "Human-centric oversight & fundamental rights",
            "Stakeholder transparency",
        ],
    },
    FrameworkType.IEEE_7000_SERIES: {
        "name": "IEEE 7000-2021 and IEEE 7001-2021 Standards",
        "jurisdiction": "International",
        "region": FrameworkRegion.INTERNATIONAL.value,
        "binding_level": BindingLevel.VOLUNTARY_STANDARD.value,
        "focus_areas": [
            "Ethical value-driven system design",
            "Stakeholder well-being and harm avoidance",
            "Multi-tiered algorithmic transparency",
            "Procedural fairness across demographic dialects",
        ],
    },
    FrameworkType.ISO_IEC_42001: {
        "name": "ISO/IEC 42001:2023 Artificial Intelligence Management System (AIMS)",
        "jurisdiction": "International (ISO/IEC)",
        "region": FrameworkRegion.INTERNATIONAL.value,
        "binding_level": BindingLevel.VOLUNTARY_STANDARD.value,
        "focus_areas": [
            "Certifiable AI management system lifecycle",
            "AI System Impact Assessment (Clause 6.1.4)",
            "Data provenance & quality gates (Annex A.7)",
            "Human oversight & stakeholder documentation (Annex A.8-A.9)",
        ],
    },
}

# EN: Consultation-only global AI legislation catalogue covering additional jurisdictions and international instruments | ES: Catalogo global de legislacion de IA solo para consulta que cubre jurisdicciones e instrumentos internacionales adicionales
GLOBAL_REFERENCE_LEGISLATION: list[dict[str, Any]] = [
    # Europe
    {
        "id": "REF_GDPR_ART22",
        "name": "EU General Data Protection Regulation (GDPR, Article 22)",
        "jurisdiction": "European Union / EEA",
        "region": FrameworkRegion.EUROPE.value,
        "binding_level": BindingLevel.LEGALLY_BINDING.value,
        "year": "2018",
        "summary": "Right not to be subject to solely automated decision-making, including profiling, producing legal or similarly significant effects.",
        "official_reference": "Regulation (EU) 2016/679, Articles 5, 6, 9 and 22",
    },
    {
        "id": "REF_SPAIN_AESIA",
        "name": "Spain Royal Decree 729/2023 (AESIA Statute)",
        "jurisdiction": "Spain",
        "region": FrameworkRegion.EUROPE.value,
        "binding_level": BindingLevel.LEGALLY_BINDING.value,
        "year": "2023",
        "summary": "Establishes the Spanish Agency for the Supervision of Artificial Intelligence (AESIA), the first national AI supervisory authority in the EU.",
        "official_reference": "Real Decreto 729/2023, BOE",
    },
    {
        "id": "REF_ITALY_AI_LAW",
        "name": "Italy National AI Law (Law No. 132/2025 / DDL 1146)",
        "jurisdiction": "Italy",
        "region": FrameworkRegion.EUROPE.value,
        "binding_level": BindingLevel.LEGALLY_BINDING.value,
        "year": "2025",
        "summary": "National framework complementing the EU AI Act on healthcare, labor, copyright, public administration, and judicial AI uses.",
        "official_reference": "Legge sull'intelligenza artificiale (Senato DDL 1146)",
    },
    {
        "id": "REF_SWITZERLAND_AI",
        "name": "Switzerland Federal Council AI Regulatory Approach",
        "jurisdiction": "Switzerland",
        "region": FrameworkRegion.EUROPE.value,
        "binding_level": BindingLevel.PROPOSED_LEGISLATION.value,
        "year": "2025",
        "summary": "Sector-specific regulatory strategy aligned with ratification of the Council of Europe AI Convention rather than a single horizontal act.",
        "official_reference": "Swiss Federal Council / OFCOM AI Overview (2025)",
    },
    # Americas
    {
        "id": "REF_NYC_LL144",
        "name": "New York City Local Law 144 (Automated Employment Decision Tools)",
        "jurisdiction": "United States (New York City)",
        "region": FrameworkRegion.AMERICAS.value,
        "binding_level": BindingLevel.LEGALLY_BINDING.value,
        "year": "2023",
        "summary": "Requires annual independent bias audits, public audit summaries, and candidate notices before using automated hiring tools.",
        "official_reference": "NYC Admin. Code § 20-870 et seq. (DCWP Rules)",
    },
    {
        "id": "REF_CALIFORNIA_SB942",
        "name": "California AI Transparency Act (SB 942)",
        "jurisdiction": "United States (California)",
        "region": FrameworkRegion.AMERICAS.value,
        "binding_level": BindingLevel.LEGALLY_BINDING.value,
        "year": "2024",
        "summary": "Mandates AI detection tools and latent/manifest provenance disclosures for large-scale generative AI providers.",
        "official_reference": "California Bus. & Prof. Code §§ 22757.1-22757.5",
    },
    {
        "id": "REF_CANADA_GENAI_CODE",
        "name": "Canada Voluntary Code of Conduct on Generative AI (and AIDA reference)",
        "jurisdiction": "Canada",
        "region": FrameworkRegion.AMERICAS.value,
        "binding_level": BindingLevel.VOLUNTARY_STANDARD.value,
        "year": "2023",
        "summary": "Voluntary commitments on accountability, safety, fairness, transparency, and human oversight following the prorogation of Bill C-27 (AIDA).",
        "official_reference": "ISED Canada Voluntary Code of Conduct (2023)",
    },
    {
        "id": "REF_CHILE_AI_BILL",
        "name": "Chile Artificial Intelligence Regulation Bill (Boletin 16.821-19)",
        "jurisdiction": "Chile",
        "region": FrameworkRegion.AMERICAS.value,
        "binding_level": BindingLevel.PROPOSED_LEGISLATION.value,
        "year": "2024",
        "summary": "Risk-based legislative proposal inspired by the EU AI Act establishing prohibited practices, high-risk duties, and institutional governance.",
        "official_reference": "Camara de Diputadas y Diputados de Chile, Boletin 16.821-19",
    },
    {
        "id": "REF_COLOMBIA_CONPES_4144",
        "name": "Colombia National Artificial Intelligence Policy (CONPES 4144)",
        "jurisdiction": "Colombia",
        "region": FrameworkRegion.AMERICAS.value,
        "binding_level": BindingLevel.VOLUNTARY_STANDARD.value,
        "year": "2025",
        "summary": "National public policy roadmap addressing ethical AI governance, data infrastructure, risk management, and talent development.",
        "official_reference": "DNP Colombia, Documento CONPES 4144 (2025)",
    },
    # Asia-Pacific
    {
        "id": "REF_AUSTRALIA_AI_SAFETY",
        "name": "Australia Voluntary AI Safety Standard & Proposed Mandatory Guardrails",
        "jurisdiction": "Australia",
        "region": FrameworkRegion.ASIA_PACIFIC.value,
        "binding_level": BindingLevel.VOLUNTARY_STANDARD.value,
        "year": "2024",
        "summary": "Ten voluntary guardrails covering accountability, risk management, testing, transparency, and human control in high-risk settings.",
        "official_reference": "Australian Dept. of Industry, Science and Resources (2024)",
    },
    {
        "id": "REF_ASEAN_AI_GUIDE",
        "name": "ASEAN Guide on AI Governance and Ethics (incl. Generative AI Expansion)",
        "jurisdiction": "ASEAN (Southeast Asia)",
        "region": FrameworkRegion.ASIA_PACIFIC.value,
        "binding_level": BindingLevel.VOLUNTARY_STANDARD.value,
        "year": "2024",
        "summary": "Regional interoperability guide promoting transparency, fairness, human-centricity, and risk-based governance across ASEAN member states.",
        "official_reference": "ASEAN Digital Ministers' Meeting (ADGMIN, 2024-2025)",
    },
    {
        "id": "REF_NZ_ALGORITHM_CHARTER",
        "name": "Algorithm Charter for Aotearoa New Zealand",
        "jurisdiction": "New Zealand",
        "region": FrameworkRegion.ASIA_PACIFIC.value,
        "binding_level": BindingLevel.VOLUNTARY_STANDARD.value,
        "year": "2020",
        "summary": "Public-sector commitment to transparency, Treaty of Waitangi partnership, bias mitigation, and human oversight in government algorithms.",
        "official_reference": "Stats NZ / data.govt.nz Algorithm Charter",
    },
    {
        "id": "REF_TAIWAN_AI_BASIC_ACT",
        "name": "Taiwan Draft Artificial Intelligence Basic Act",
        "jurisdiction": "Taiwan",
        "region": FrameworkRegion.ASIA_PACIFIC.value,
        "binding_level": BindingLevel.PROPOSED_LEGISLATION.value,
        "year": "2024",
        "summary": "Framework bill establishing seven core AI principles (sustainability, human autonomy, privacy, transparency, fairness, accountability, security).",
        "official_reference": "National Science and Technology Council (NSTC, 2024)",
    },
    # Africa
    {
        "id": "REF_SOUTH_AFRICA_AI_POLICY",
        "name": "South Africa National AI Policy Framework",
        "jurisdiction": "South Africa",
        "region": FrameworkRegion.AFRICA.value,
        "binding_level": BindingLevel.VOLUNTARY_STANDARD.value,
        "year": "2024",
        "summary": "National policy framework emphasizing ethical AI, POPIA data protection alignment, bias prevention, and inclusive digital development.",
        "official_reference": "DCDT South Africa, National AI Policy Framework (2024)",
    },
    {
        "id": "REF_NIGERIA_NAIS",
        "name": "Nigeria National Artificial Intelligence Strategy (NAIS)",
        "jurisdiction": "Nigeria",
        "region": FrameworkRegion.AFRICA.value,
        "binding_level": BindingLevel.VOLUNTARY_STANDARD.value,
        "year": "2024",
        "summary": "National strategy prioritizing local language datasets, ethical governance, NDPA data privacy compliance, and inclusive innovation.",
        "official_reference": "Federal Ministry of Communications, Innovation & Digital Economy (2024)",
    },
    {
        "id": "REF_KENYA_AI_STRATEGY",
        "name": "Kenya National Artificial Intelligence Strategy (2025-2030)",
        "jurisdiction": "Kenya",
        "region": FrameworkRegion.AFRICA.value,
        "binding_level": BindingLevel.VOLUNTARY_STANDARD.value,
        "year": "2025",
        "summary": "Five-year governance and innovation framework aligned with Kenya's Data Protection Act and ethical AI standards.",
        "official_reference": "Ministry of Information, Communications and the Digital Economy (2025)",
    },
    {
        "id": "REF_RWANDA_AI_POLICY",
        "name": "Rwanda National Artificial Intelligence Policy",
        "jurisdiction": "Rwanda",
        "region": FrameworkRegion.AFRICA.value,
        "binding_level": BindingLevel.VOLUNTARY_STANDARD.value,
        "year": "2023",
        "summary": "Responsible AI adoption roadmap combining ethical guidelines, data governance, and public-sector capacity building.",
        "official_reference": "Ministry of ICT and Innovation, Republic of Rwanda (2023)",
    },
    # International
    {
        "id": "REF_UNESCO_AI_ETHICS",
        "name": "UNESCO Recommendation on the Ethics of Artificial Intelligence",
        "jurisdiction": "Global (193 UNESCO Member States)",
        "region": FrameworkRegion.INTERNATIONAL.value,
        "binding_level": BindingLevel.VOLUNTARY_STANDARD.value,
        "year": "2021",
        "summary": "First global normative instrument on AI ethics covering proportionality, fairness, linguistic diversity, and Ethical Impact Assessment (EIA).",
        "official_reference": "UNESCO SHS/BIO/PI/2021/1 (Adopted Nov. 2021)",
    },
    {
        "id": "REF_OECD_AI_PRINCIPLES",
        "name": "OECD Recommendation of the Council on Artificial Intelligence",
        "jurisdiction": "OECD & Adherent Countries",
        "region": FrameworkRegion.INTERNATIONAL.value,
        "binding_level": BindingLevel.VOLUNTARY_STANDARD.value,
        "year": "2024",
        "summary": "Intergovernmental principles for trustworthy AI (updated May 2024) addressing human rights, transparency, robustness, and accountability.",
        "official_reference": "OECD/LEGAL/0449 (Revised May 2024)",
    },
    {
        "id": "REF_UNGA_AI_RES",
        "name": "UN General Assembly Resolution on Safe, Secure and Trustworthy AI",
        "jurisdiction": "United Nations (193 Member States)",
        "region": FrameworkRegion.INTERNATIONAL.value,
        "binding_level": BindingLevel.VOLUNTARY_STANDARD.value,
        "year": "2024",
        "summary": "Consensus UN resolution affirming human rights, non-discrimination, privacy, and sustainable development throughout the AI lifecycle.",
        "official_reference": "UNGA Resolution A/RES/78/265 (March 2024)",
    },
    {
        "id": "REF_G7_HIROSHIMA",
        "name": "G7 Hiroshima AI Process International Guiding Principles & Code of Conduct",
        "jurisdiction": "G7 & International Partners",
        "region": FrameworkRegion.INTERNATIONAL.value,
        "binding_level": BindingLevel.VOLUNTARY_STANDARD.value,
        "year": "2023",
        "summary": "Voluntary international principles and reporting framework for organizations developing advanced and generative AI systems.",
        "official_reference": "G7 Hiroshima AI Process (Oct. 2023)",
    },
]


# EN: Case Studies Endpoints | ES: Puntos Finales de Casos de Estudio


@router.get(
    "/cases",
    response_model=list[CaseStudySummaryDTO],
    status_code=status.HTTP_200_OK,
    summary="EN: Fetch All Complex NLP Case Studies | ES: Obtener Todos los Casos de Estudio Complejos de NLP",
    description="EN: Retrieves summaries of complex computational linguistics ethical dilemmas. | ES: Recupera resumenes de dilemas eticos complejos en linguistica computacional.",
)
def get_case_studies(
    use_case: Annotated[ListCaseStudiesUseCase, Depends(get_list_case_studies_use_case)],
) -> list[CaseStudySummaryDTO]:
    """EN: Retrieve all registered computational linguistics case studies. | ES: Recuperar todos los casos de estudio de linguistica computacional registrados."""
    return use_case.execute()


@router.get(
    "/cases/{case_id}",
    response_model=CaseStudyDTO,
    status_code=status.HTTP_200_OK,
    summary="EN: Fetch Specific Case Study Details | ES: Obtener Detalles de Caso de Estudio Especifico",
    description="EN: Retrieves full specification, artifacts, baseline matrix, and decision options for a case study. | ES: Recupera la especificacion completa, artefactos, matriz base y opciones de decision para un caso de estudio.",
)
def get_case_study(
    case_id: str,
    use_case: Annotated[GetCaseStudyUseCase, Depends(get_case_study_use_case)],
) -> CaseStudyDTO:
    """EN: Retrieve specific case study specification by identifier. | ES: Recuperar la especificacion de un caso de estudio por identificador."""
    return use_case.execute(case_id)


# EN: Decision Submission and Evaluation Endpoints | ES: Puntos Finales de Envio y Evaluacion de Decisiones


@router.post(
    "/decisions",
    response_model=DecisionImpactResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="EN: Submit Ethical Decision and Calculate Impact | ES: Enviar Decision Etica y Calcular Impacto",
    description="EN: Evaluates chosen decision against multidimensional matrix (Transparency, Accountability, Fairness) and international frameworks. | ES: Evalua la decision elegida frente a la matriz multidimensional (Transparencia, Rendicion de Cuentas, Equidad) y marcos internacionales.",
)
def submit_decision(
    request: SubmitDecisionRequest,
    use_case: Annotated[SubmitDecisionUseCase, Depends(get_submit_decision_use_case)],
) -> DecisionImpactResponseDTO:
    """EN: Submit decision option, compute multidimensional impact and regulatory audit. | ES: Enviar opcion de decision, calcular impacto multidimensional y auditoria regulatoria."""
    return use_case.execute(request)


@router.get(
    "/evaluations/{evaluation_id}",
    response_model=DecisionImpactResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="EN: Fetch Decision Impact Calculation Result | ES: Obtener Resultado de Calculo de Impacto de Decision",
    description="EN: Retrieves a previously computed decision impact evaluation by identifier. | ES: Recupera una evaluacion de impacto de decision previamente calculada por identificador.",
)
def get_decision_impact(
    evaluation_id: str,
    use_case: Annotated[GetDecisionImpactUseCase, Depends(get_decision_impact_use_case)],
) -> DecisionImpactResponseDTO:
    """EN: Retrieve stored decision impact evaluation. | ES: Recuperar evaluacion de impacto de decision almacenada."""
    result = use_case.execute(evaluation_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Evaluation with id '{evaluation_id}' was not found.",
        )
    return result


# EN: Scenarios Compatibility Endpoints | ES: Puntos Finales de Compatibilidad de Escenarios


@router.get(
    "/scenarios",
    response_model=list[ScenarioDTO],
    status_code=status.HTTP_200_OK,
    summary="EN: List Scenarios | ES: Listar Escenarios",
)
def get_scenarios(
    use_case: Annotated[ListScenariosUseCase, Depends(get_list_scenarios_use_case)],
) -> list[ScenarioDTO]:
    """EN: Retrieve all registered computational linguistics scenarios. | ES: Recuperar todos los escenarios de linguistica computacional registrados."""
    return use_case.execute()


@router.get(
    "/scenarios/{scenario_id}",
    response_model=ScenarioDTO,
    status_code=status.HTTP_200_OK,
    summary="EN: Get Scenario by ID | ES: Obtener Escenario por ID",
)
def get_scenario(
    scenario_id: str,
    use_case: Annotated[GetScenarioUseCase, Depends(get_scenario_use_case)],
) -> ScenarioDTO:
    """EN: Retrieve a specific scenario by its unique identifier. | ES: Recuperar un escenario especifico por su identificador unico."""
    return use_case.execute(scenario_id)


@router.post(
    "/evaluations",
    response_model=EthicalAssessmentDTO,
    status_code=status.HTTP_201_CREATED,
    summary="EN: Evaluate Scenario | ES: Evaluar Escenario",
)
def evaluate_scenario(
    request: EvaluateScenarioRequest,
    use_case: Annotated[EvaluateScenarioUseCase, Depends(get_evaluate_scenario_use_case)],
) -> EthicalAssessmentDTO:
    """EN: Execute ethical evaluation on a specified scenario across chosen frameworks. | ES: Ejecutar evaluacion etica sobre un escenario especificado a traves de los marcos elegidos."""
    return use_case.execute(request)
