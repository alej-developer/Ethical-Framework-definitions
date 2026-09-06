/** EN: TypeScript type definitions for domain entities and application state. | ES: Definiciones de tipos TypeScript para entidades de dominio y estado de la aplicacion. */

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

export interface LinguisticArtifact {
  text_sample: string;
  dialect_or_variety: string;
  protected_attribute: string;
  expected_output: string;
  observed_output: string;
  confidence_score: number;
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

export interface FrameworkMetadata {
  id: string;
  name: string;
  jurisdiction: string;
  focus_areas: string[];
}

export interface AppState {
  scenarios: Scenario[];
  selectedScenarioId: string | null;
  selectedFrameworks: string[];
  currentAssessment: EthicalAssessment | null;
  isLoading: boolean;
  errorMessage: string | null;
}
