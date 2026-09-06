/** EN: Custom reactive state manager implementing Observer pattern with atomic state subscriptions. | ES: Gestor de estado reactivo personalizado que implementa el patron Observer con suscripciones atomicas. */

import {
  AppState,
  CaseStudy,
  CaseStudySummary,
  DecisionImpactResponse,
  Language,
} from "../types/index.ts";

export type Listener<T> = (state: T) => void;

export class Store<T> {
  private state: T;
  private listeners: Set<Listener<T>> = new Set();

  constructor(initialState: T) {
    // EN: Initialize internal state object | ES: Inicializar objeto de estado interno
    this.state = initialState;
  }

  public getState(): T {
    // EN: Return state snapshot immutably | ES: Retornar captura de estado de forma inmutable
    return this.state;
  }

  public setState(updater: Partial<T> | ((prevState: T) => Partial<T>)): void {
    // EN: Update state and trigger subscribed observers | ES: Actualizar estado y activar observadores suscritos
    const patch = typeof updater === "function" ? updater(this.state) : updater;
    this.state = { ...this.state, ...patch };
    this.notify();
  }

  public subscribe(listener: Listener<T>): () => void {
    // EN: Register observer listener and immediately emit current state | ES: Registrar oyente observador y emitir inmediatamente el estado actual
    this.listeners.add(listener);
    listener(this.state);
    return () => {
      this.listeners.delete(listener);
    };
  }

  private notify(): void {
    // EN: Notify all active subscribers of updated state | ES: Notificar a todos los suscriptores activos del estado actualizado
    for (const listener of this.listeners) {
      listener(this.state);
    }
  }
}

const initialAppState: AppState = {
  language: "en",
  cases: [],
  selectedCaseId: null,
  currentCase: null,
  selectedOptionId: null,
  userRationale: "",
  selectedFrameworks: ["EU_AI_ACT", "IEEE_7000_SERIES"],
  latestImpact: null,
  isLoading: false,
  errorMessage: null,
};

// EN: Application-wide reactive store singleton | ES: Instancia unica de almacen reactivo para toda la aplicacion
export const appStore = new Store<AppState>(initialAppState);

export const actions = {
  setLanguage: (language: Language): void => {
    appStore.setState({ language });
  },

  setCaseList: (cases: CaseStudySummary[]): void => {
    const firstId = cases.length > 0 ? cases[0].id : null;
    appStore.setState({
      cases,
      selectedCaseId: firstId,
      errorMessage: null,
    });
  },

  setCurrentCase: (currentCase: CaseStudy): void => {
    // EN: Auto-select first decision option if available | ES: Seleccionar automaticamente la primera opcion de decision si esta disponible
    const firstOpt = currentCase.decision_options.length > 0 ? currentCase.decision_options[0].id : null;
    appStore.setState({
      currentCase,
      selectedCaseId: currentCase.id,
      selectedOptionId: firstOpt,
      latestImpact: null,
      errorMessage: null,
    });
  },

  selectOption: (optionId: string): void => {
    appStore.setState({ selectedOptionId: optionId });
  },

  setUserRationale: (rationale: string): void => {
    appStore.setState({ userRationale: rationale });
  },

  toggleFramework: (frameworkId: string): void => {
    const current = appStore.getState().selectedFrameworks;
    const exists = current.includes(frameworkId);
    let next: string[];
    if (exists) {
      // EN: Ensure at least one framework remains active | ES: Asegurar que al menos un marco permanezca activo
      next = current.length > 1 ? current.filter((f) => f !== frameworkId) : current;
    } else {
      next = [...current, frameworkId];
    }
    appStore.setState({ selectedFrameworks: next });
  },

  setLoading: (isLoading: boolean): void => {
    appStore.setState({ isLoading });
  },

  setImpactResult: (impact: DecisionImpactResponse): void => {
    appStore.setState({
      latestImpact: impact,
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

  clearError: (): void => {
    appStore.setState({ errorMessage: null });
  },
};
