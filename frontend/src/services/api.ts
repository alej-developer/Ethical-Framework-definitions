/** EN: HTTP API client service for interacting with the Clean Architecture backend. | ES: Servicio de cliente API HTTP para interactuar con el backend de Arquitectura Limpia. */

import {
  CaseStudy,
  CaseStudySummary,
  DecisionImpactResponse,
  StandardErrorResponse,
} from "../types/index.ts";

const BASE_URL = "/api/v1";

export class ApiService {
  public static async checkHealth(): Promise<{ status: string; service: string }> {
    // EN: Verify backend connectivity | ES: Verificar conectividad con el backend
    const response = await fetch(`${BASE_URL}/health`);
    if (!response.ok) {
      throw new Error(`Health check failed with HTTP ${response.status}`);
    }
    return response.json();
  }

  public static async fetchCaseStudies(): Promise<CaseStudySummary[]> {
    // EN: Retrieve all complex computational linguistics case studies | ES: Recuperar todos los casos de estudio complejos de linguistica computacional
    const response = await fetch(`${BASE_URL}/cases`);
    if (!response.ok) {
      throw new Error(`Failed to load case studies: HTTP ${response.status}`);
    }
    return response.json();
  }

  public static async fetchCaseStudy(caseId: string): Promise<CaseStudy> {
    // EN: Fetch detailed specification and decision tree for a single case | ES: Obtener especificacion detallada y arbol de decision para un solo caso
    const response = await fetch(`${BASE_URL}/cases/${encodeURIComponent(caseId)}`);
    if (!response.ok) {
      const errJson = (await response.json().catch(() => ({}))) as StandardErrorResponse;
      const msg = errJson.error?.message || `Failed to load case study ${caseId}: HTTP ${response.status}`;
      throw new Error(msg);
    }
    return response.json();
  }

  public static async submitDecision(
    caseId: string,
    selectedOptionId: string,
    userRationale: string,
    frameworks: string[] = ["EU_AI_ACT", "IEEE_7000_SERIES"],
    customWeights?: Record<string, number>,
  ): Promise<DecisionImpactResponse> {
    // EN: Dispatch ethical decision and calculate multidimensional impact | ES: Despachar decision etica y calcular impacto multidimensional
    const response = await fetch(`${BASE_URL}/decisions`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        case_id: caseId,
        selected_option_id: selectedOptionId,
        user_rationale: userRationale,
        frameworks,
        custom_weights: customWeights,
      }),
    });

    if (!response.ok) {
      const errJson = (await response.json().catch(() => ({}))) as StandardErrorResponse;
      const msg = errJson.error?.message || `Decision submission failed with HTTP ${response.status}`;
      throw new Error(msg);
    }

    return response.json();
  }

  public static async fetchEvaluation(evaluationId: string): Promise<DecisionImpactResponse> {
    // EN: Retrieve previously stored decision evaluation result | ES: Recuperar resultado de evaluacion de decision previamente guardado
    const response = await fetch(`${BASE_URL}/evaluations/${encodeURIComponent(evaluationId)}`);
    if (!response.ok) {
      throw new Error(`Evaluation '${evaluationId}' not found: HTTP ${response.status}`);
    }
    return response.json();
  }
}
