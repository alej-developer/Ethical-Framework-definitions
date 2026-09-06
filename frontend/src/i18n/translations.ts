/** EN: Centralized internationalization dictionary providing runtime English and Spanish translations. | ES: Diccionario de internacionalizacion centralizado que proporciona traducciones en tiempo de ejecucion en ingles y espanol. */

export type Language = "en" | "es";

export interface Translations {
  appTitle: string;
  appSubtitle: string;
  architectureBadge: string;
  skipToContent: string;
  languageToggle: string;
  caseStudiesSectionTitle: string;
  caseStudiesSectionDesc: string;
  selectCasePrompt: string;
  dilemmaHeading: string;
  contextHeading: string;
  artifactsHeading: string;
  artifactsDesc: string;
  colSampleText: string;
  colVariety: string;
  colExpected: string;
  colObserved: string;
  colConfidence: string;
  baselineMatrixHeading: string;
  baselineMatrixDesc: string;
  regulatoryHeading: string;
  decisionTreeHeading: string;
  decisionTreeDesc: string;
  optionStrategyLabel: string;
  rationaleHeading: string;
  rationalePlaceholder: string;
  rationaleMinCharsNote: string;
  frameworksHeading: string;
  frameworkEU: string;
  frameworkEUDesc: string;
  frameworkIEEE: string;
  frameworkIEEEDesc: string;
  submitButtonText: string;
  evaluatingText: string;
  evaluationResultsHeading: string;
  overallAlignmentHeading: string;
  dimensionTransparency: string;
  dimensionAccountability: string;
  dimensionFairness: string;
  baselineLabel: string;
  decisionLabel: string;
  deltaLabel: string;
  riskTierLabel: string;
  complianceStatusLabel: string;
  tradeOffHeading: string;
  recommendationsHeading: string;
  emptyStateTitle: string;
  emptyStateDesc: string;
  errorTitle: string;
  retryButtonText: string;
  statusMinimalRisk: string;
  statusSpecificTransparencyRisk: string;
  statusHighRisk: string;
  statusUnacceptableRisk: string;
  verdictCompliant: string;
  verdictPartiallyCompliant: string;
  verdictNonCompliant: string;
  verdictProhibited: string;
}

export const dictionary: Record<Language, Translations> = {
  en: {
    appTitle: "AI Ethics Interactive Simulator",
    appSubtitle: "Computational Linguistics Statutory & Value-Alignment Engine",
    architectureBadge: "Clean Architecture / SOLID",
    skipToContent: "Skip to main content",
    languageToggle: "ES",
    caseStudiesSectionTitle: "1. Linguistic Case Study",
    caseStudiesSectionDesc: "Empirical failure modes and benchmark evaluation corpus",
    selectCasePrompt: "Select Case Study",
    dilemmaHeading: "Ethical Dilemma",
    contextHeading: "Operational Context",
    artifactsHeading: "Linguistic Artifacts Corpus",
    artifactsDesc: "Sample tokens evaluated across dialects and demographic varieties",
    colSampleText: "Sample Text",
    colVariety: "Dialect / Variety",
    colExpected: "Expected Output",
    colObserved: "Observed Output",
    colConfidence: "Confidence",
    baselineMatrixHeading: "Predefined Baseline Ethical Matrix",
    baselineMatrixDesc: "Initial quantitative scores prior to user decision intervention",
    regulatoryHeading: "Statutory & Regulatory Implications",
    decisionTreeHeading: "2. Decision Tree & Policy Intervention",
    decisionTreeDesc: "Select an architectural intervention to address the ethical dilemma",
    optionStrategyLabel: "Strategy",
    rationaleHeading: "Decision Justification & Rationale",
    rationalePlaceholder: "Articulate your ethical reasoning and justification for the chosen intervention strategy (minimum 10 characters)...",
    rationaleMinCharsNote: "Minimum 10 characters required for statutory audit logging.",
    frameworksHeading: "Target Statutory Frameworks",
    frameworkEU: "EU AI Act (Regulation EU 2024/1689)",
    frameworkEUDesc: "Prohibited practices, Annex III high-risk compliance, Art. 10 bias parity, Art. 14 oversight.",
    frameworkIEEE: "IEEE Standards (IEEE Std 7000 & 7001)",
    frameworkIEEEDesc: "Stakeholder well-being protection, value elicitation, algorithmic transparency index.",
    submitButtonText: "Execute Ethical Evaluation",
    evaluatingText: "Simulating Impact Across Frameworks...",
    evaluationResultsHeading: "3. Real-Time Impact & Statutory Compliance",
    overallAlignmentHeading: "Consolidated Ethical Alignment Index",
    dimensionTransparency: "Transparency",
    dimensionAccountability: "Accountability",
    dimensionFairness: "Fairness",
    baselineLabel: "Baseline",
    decisionLabel: "Decision",
    deltaLabel: "Delta",
    riskTierLabel: "EU AI Act Risk Tier",
    complianceStatusLabel: "Statutory Compliance Verdict",
    tradeOffHeading: "Qualitative Trade-Off Analysis",
    recommendationsHeading: "Statutory Remediation Directives",
    emptyStateTitle: "Simulation Pending",
    emptyStateDesc: "Select a decision alternative from the tree above and click 'Execute Ethical Evaluation' to compute real-time statutory metrics.",
    errorTitle: "Simulation Error",
    retryButtonText: "Dismiss",
    statusMinimalRisk: "Minimal Risk",
    statusSpecificTransparencyRisk: "Specific Transparency Risk",
    statusHighRisk: "High Risk (Annex III)",
    statusUnacceptableRisk: "Unacceptable Risk (Prohibited)",
    verdictCompliant: "Compliant",
    verdictPartiallyCompliant: "Partially Compliant",
    verdictNonCompliant: "Non-Compliant",
    verdictProhibited: "Prohibited by Law",
  },
  es: {
    appTitle: "Simulador Interactivo de Etica en IA",
    appSubtitle: "Motor de Cumplimiento Estatutario y Alineacion de Valores para Linguistica Computacional",
    architectureBadge: "Arquitectura Limpia / SOLID",
    skipToContent: "Saltar al contenido principal",
    languageToggle: "EN",
    caseStudiesSectionTitle: "1. Caso de Estudio Linguistico",
    caseStudiesSectionDesc: "Modos de fallo empiricos y corpus de evaluacion de referencia",
    selectCasePrompt: "Seleccionar Caso de Estudio",
    dilemmaHeading: "Dilema Etico",
    contextHeading: "Contexto Operativo",
    artifactsHeading: "Corpus de Artefactos Linguisticos",
    artifactsDesc: "Muestras textuales evaluadas a traves de dialectos y variedades demograficas",
    colSampleText: "Texto de Muestra",
    colVariety: "Dialecto / Variedad",
    colExpected: "Salida Esperada",
    colObserved: "Salida Observada",
    colConfidence: "Confianza",
    baselineMatrixHeading: "Matriz Etica Base Predefinida",
    baselineMatrixDesc: "Puntuaciones cuantitativas iniciales previas a la intervencion del usuario",
    regulatoryHeading: "Implicaciones Estatutarias y Regulatorias",
    decisionTreeHeading: "2. Arbol de Decision e Intervencion de Politicas",
    decisionTreeDesc: "Seleccione una intervencion arquitectonica para abordar el dilema etico",
    optionStrategyLabel: "Estrategia",
    rationaleHeading: "Justificacion y Razonamiento de la Decision",
    rationalePlaceholder: "Articule su razonamiento etico y justificacion para la estrategia elegida (minimo 10 caracteres)...",
    rationaleMinCharsNote: "Se requieren minimo 10 caracteres para el registro de auditoria estatutaria.",
    frameworksHeading: "Marcos Estatutarios Objetivo",
    frameworkEU: "Ley de IA de la UE (Reglamento UE 2024/1689)",
    frameworkEUDesc: "Practicas prohibidas, alto riesgo Anexo III, paridad de sesgo Art. 10, supervision humana Art. 14.",
    frameworkIEEE: "Normas IEEE (IEEE Std 7000 y 7001)",
    frameworkIEEEDesc: "Proteccion del bienestar, elicitacion de valores, indice de transparencia algoritmica.",
    submitButtonText: "Ejecutar Evaluacion Etica",
    evaluatingText: "Simulando Impacto a Traves de los Marcos...",
    evaluationResultsHeading: "3. Impacto en Tiempo Real y Cumplimiento Estatutario",
    overallAlignmentHeading: "Indice Consolidado de Alineacion Etica",
    dimensionTransparency: "Transparencia",
    dimensionAccountability: "Rendicion de Cuentas",
    dimensionFairness: "Equidad",
    baselineLabel: "Base",
    decisionLabel: "Decision",
    deltaLabel: "Delta",
    riskTierLabel: "Nivel de Riesgo Ley de IA UE",
    complianceStatusLabel: "Veredicto de Cumplimiento Estatutario",
    tradeOffHeading: "Analisis Cualitativo de Compensaciones",
    recommendationsHeading: "Directivas Estatutarias de Subsanacion",
    emptyStateTitle: "Simulacion Pendiente",
    emptyStateDesc: "Seleccione una alternativa de decision del arbol superior y haga clic en 'Ejecutar Evaluacion Etica' para calcular metricas estatutarias en tiempo real.",
    errorTitle: "Error de Simulacion",
    retryButtonText: "Cerrar",
    statusMinimalRisk: "Riesgo Minimo",
    statusSpecificTransparencyRisk: "Riesgo Especifico de Transparencia",
    statusHighRisk: "Alto Riesgo (Anexo III)",
    statusUnacceptableRisk: "Riesgo Inaceptable (Prohibido)",
    verdictCompliant: "Cumple",
    verdictPartiallyCompliant: "Cumplimiento Parcial",
    verdictNonCompliant: "No Cumple",
    verdictProhibited: "Prohibido por Ley",
  },
};

export function getTranslation(key: keyof Translations, lang: Language): string {
  // EN: Retrieve translation by key and language | ES: Recuperar traduccion por clave e idioma
  return dictionary[lang][key] || dictionary.en[key] || String(key);
}
