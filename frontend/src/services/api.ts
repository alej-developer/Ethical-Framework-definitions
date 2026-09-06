/** EN: HTTP API client service for interacting with the Clean Architecture backend. | ES: Servicio de cliente API HTTP para interactuar con el backend de Arquitectura Limpia. */

import {
  EthicalAssessment,
  FrameworkMetadata,
  Scenario,
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

  public static async fetchFrameworks(): Promise<FrameworkMetadata[]> {
    // EN: Retrieve supported ethical frameworks | ES: Recuperar marcos eticos soportados
    const response = await fetch(`${BASE_URL}/frameworks`);
    if (!response.ok) {
      throw new Error(`Failed to load frameworks: HTTP ${response.status}`);
    }
    return response.json();
  }

  public static async fetchScenarios(): Promise<Scenario[]> {
    // EN: Retrieve all computational linguistics benchmark scenarios | ES: Recuperar todos los escenarios de referencia de linguistica computacional
    const response = await fetch(`${BASE_URL}/scenarios`);
    if (!response.ok) {
      throw new Error(`Failed to load scenarios: HTTP ${response.status}`);
    }
    return response.json();
  }

  public static async fetchScenario(scenarioId: string): Promise<Scenario> {
    // EN: Fetch single scenario by unique key | ES: Obtener un unico escenario por clave unica
    const response = await fetch(`${BASE_URL}/scenarios/${encodeURIComponent(scenarioId)}`);
    if (!response.ok) {
      throw new Error(`Failed to load scenario ${scenarioId}: HTTP ${response.status}`);
    }
    return response.json();
  }

  public static async evaluateScenario(
    scenarioId: string,
    frameworks: string[],
  ): Promise<EthicalAssessment> {
    // EN: Dispatch ethical audit simulation request | ES: Despachar solicitud de simulacion de auditoria etica
    const response = await fetch(`${BASE_URL}/evaluations`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        scenario_id: scenarioId,
        frameworks,
      }),
    });

    if (!response.ok) {
      const errorBody = await response.json().catch(() => ({}));
      const message = (errorBody as { detail?: string }).detail || `Evaluation failed with HTTP ${response.status}`;
      throw new Error(message);
    }

    return response.json();
  }
}
