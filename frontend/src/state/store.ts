/** EN: Lightweight custom reactive state store implementing Observer pattern. | ES: Almacen de estado reactivo personalizado y ligero que implementa el patron Observer. */

import { AppState, EthicalAssessment, Scenario } from "../types/index.ts";

export type Listener<T> = (state: T) => void;

export class Store<T> {
  private state: T;
  private listeners: Set<Listener<T>> = new Set();

  constructor(initialState: T) {
    // EN: Initialize internal state | ES: Inicializar estado interno
    this.state = initialState;
  }

  public getState(): T {
    // EN: Retrieve current snapshot of state immutably | ES: Obtener captura actual del estado de forma inmutable
    return this.state;
  }

  public setState(updater: Partial<T> | ((prevState: T) => Partial<T>)): void {
    // EN: Compute next state and notify subscribed observers | ES: Calcular el siguiente estado y notificar a los observadores suscritos
    const updates = typeof updater === "function" ? updater(this.state) : updater;
    this.state = { ...this.state, ...updates };
    this.notify();
  }

  public subscribe(listener: Listener<T>): () => void {
    // EN: Add listener and return unsubscribe function | ES: Agregar oyente y retornar funcion de cancelacion de suscripcion
    this.listeners.add(listener);
    listener(this.state);
    return () => {
      this.listeners.delete(listener);
    };
  }

  private notify(): void {
    // EN: Broadcast state update to all active listeners | ES: Transmitir actualizacion de estado a todos los oyentes activos
    for (const listener of this.listeners) {
      listener(this.state);
    }
  }
}

const initialAppState: AppState = {
  scenarios: [],
  selectedScenarioId: null,
  selectedFrameworks: ["EU_AI_ACT", "IEEE_7000_SERIES"],
  currentAssessment: null,
  isLoading: false,
  errorMessage: null,
};

// EN: Singleton store instance for application lifecycle | ES: Instancia unica de almacen para el ciclo de vida de la aplicacion
export const appStore = new Store<AppState>(initialAppState);

export const actions = {
  setScenarios: (scenarios: Scenario[]): void => {
    appStore.setState({
      scenarios,
      selectedScenarioId: scenarios.length > 0 ? scenarios[0].id : null,
      errorMessage: null,
    });
  },

  selectScenario: (scenarioId: string): void => {
    appStore.setState({
      selectedScenarioId: scenarioId,
      currentAssessment: null,
      errorMessage: null,
    });
  },

  toggleFramework: (frameworkId: string): void => {
    const current = appStore.getState().selectedFrameworks;
    const exists = current.includes(frameworkId);
    let next: string[];
    if (exists) {
      // EN: Prevent deselecting all frameworks | ES: Evitar deseleccionar todos los marcos
      next = current.length > 1 ? current.filter((f) => f !== frameworkId) : current;
    } else {
      next = [...current, frameworkId];
    }
    appStore.setState({ selectedFrameworks: next });
  },

  setLoading: (isLoading: boolean): void => {
    appStore.setState({ isLoading });
  },

  setAssessment: (assessment: EthicalAssessment): void => {
    appStore.setState({
      currentAssessment: assessment,
      isLoading: false,
      errorMessage: null,
    });
  },

  setError: (errorMessage: string | null): void => {
    appStore.setState({
      errorMessage,
      isLoading: false,
    });
  },
};
