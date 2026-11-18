/** EN: TypeScript type definitions for domain entities, API payloads, and UI application state. | ES: Definiciones de tipos TypeScript para entidades de dominio, cargas API y estado de la aplicacion UI. */

export type Language = "en" | "es";

export type RiskTier =
  | "UNACCEPTABLE_RISK"
  | "HIGH_RISK"
  | "SPECIFIC_TRANSPARENCY_RISK"
  | "MINIMAL_RISK";

export type ComplianceStatus =
  | "COMPLIANT"
  | "PARTIALLY_COMPLIANT"
  | "NON_COMPLIANT"
  | "PROHIBITED";

export type FrameworkRegion = "EUROPE" | "AMERICAS" | "ASIA_PACIFIC" | "AFRICA" | "INTERNATIONAL";

export type BindingLevel = "LEGALLY_BINDING" | "VOLUNTARY_STANDARD" | "PROPOSED_LEGISLATION";

export type AlignmentStatus =
  | "FULLY_ALIGNED"
  | "SUBSTANTIALLY_ALIGNED"
  | "PARTIALLY_ALIGNED"
  | "NOT_ALIGNED";

/** EN: Framework catalogue entry returned by GET /api/v1/frameworks. | ES: Entrada del catalogo de marcos devuelta por GET /api/v1/frameworks. */
export interface FrameworkInfo {
  id: string;
  name: string;
  jurisdiction: string;
  region: FrameworkRegion;
  binding_level: BindingLevel;
  focus_areas: string[];
}

export interface LinguisticArtifact {
  text_sample: string;
  dialect_or_variety: string;
  protected_attribute: string;
  expected_output: string;
  observed_output: string;
  confidence_score: number;
  geographic_region?: string | null;
  geographic_source?: string | null;
}

export interface DecisionOption {
  id: string;
  title: string;
  description: string;
  strategy: string;
  dimension_modifiers: Record<string, number>;
  rationale: string;
}

export interface CaseStudySummary {
  id: string;
  title: string;
  nlp_domain: string;
  dilemma: string;
  domain_category: string;
  task_type: string;
  available_options_count: number;
}

export interface CaseStudy {
  id: string;
  title: string;
  nlp_domain: string;
  dilemma: string;
  context_description: string;
  task_type: string;
  domain_category: string;
  linguistic_artifacts: LinguisticArtifact[];
  baseline_matrix: Record<string, number>;
  decision_options: DecisionOption[];
  regulatory_implications: Record<string, string>;
  metadata: Record<string, unknown>;
}

export interface DimensionScore {
  dimension: string;
  baseline_score: number;
  decision_score: number;
  delta: number;
  rationale: string;
}

export interface MultidimensionalMatrix {
  transparency: DimensionScore;
  accountability: DimensionScore;
  fairness: DimensionScore;
  overall_alignment: number;
}

export interface EvaluationMetric {
  name: string;
  score: number;
  threshold: number;
  passed: boolean;
  description: string;
}

export interface EthicalFinding {
  framework: string;
  category: string;
  severity: "CRITICAL" | "HIGH" | "MEDIUM" | "LOW";
  message: string;
  recommendation: string;
}

export interface FrameworkAssessment {
  framework: string;
  risk_tier: RiskTier;
  compliance_status: ComplianceStatus;
  metrics: EvaluationMetric[];
  findings: EthicalFinding[];
  recommendations: string[];
  binding_level: BindingLevel;
  alignment_status: AlignmentStatus | null;
  region: FrameworkRegion | null;
}

export interface DecisionImpactResponse {
  decision_id: string;
  case_id: string;
  selected_option: DecisionOption;
  matrix: MultidimensionalMatrix;
  framework_assessments: FrameworkAssessment[];
  overall_risk_tier: RiskTier;
  overall_compliance: ComplianceStatus;
  trade_off_analysis: string;
  recommendations: string[];
  created_at: string;
}

export interface Scenario {
  id: string;
  title: string;
  description: string;
  domain_category: string;
  task_type: string;
  artifacts: LinguisticArtifact[];
  metadata: Record<string, unknown>;
}

export interface EthicalAssessment {
  id: string;
  scenario_id: string;
  created_at: string;
  framework_assessments: FrameworkAssessment[];
  overall_risk_tier: RiskTier;
  overall_compliance: ComplianceStatus;
  executive_summary: string;
}

export interface StandardErrorResponse {
  error: {
    code: string;
    message: string;
    status_code: number;
    details?: unknown;
    timestamp: string;
  };
}

export type FailedOperation =
  | { type: "LOAD_CASES" }
  | { type: "LOAD_CASE_DETAIL"; caseId: string }
  | {
      type: "SUBMIT_DECISION";
      caseId: string;
      selectedOptionId: string;
      userRationale: string;
      frameworks: string[];
    };

export interface AppState {
  language: Language;
  cases: CaseStudySummary[];
  selectedCaseId: string | null;
  currentCase: CaseStudy | null;
  selectedArtifactIndex: number | null;
  selectedOptionId: string | null;
  userRationale: string;
  selectedFrameworks: string[];
  availableFrameworks: FrameworkInfo[];
  latestImpact: DecisionImpactResponse | null;
  isLoading: boolean;
  errorMessage: string | null;
  lastFailedOperation: FailedOperation | null;
}
