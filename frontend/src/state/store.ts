/** EN: Custom reactive state manager implementing Observer pattern with atomic state subscriptions. | ES: Gestor de estado reactivo personalizado que implementa el patron Observer con suscripciones atomicas. */

import { ApiService } from "../services/api.ts";
import {
  AppState,
  CaseStudy,
  CaseStudySummary,
  DecisionImpactResponse,
  FailedOperation,
  FrameworkInfo,
  Language,
} from "../types/index.ts";

export type Listener<T> = (state: T) => void;
export type Selector<T, S> = (state: T) => S;
export type EqualityFn<S> = (a: S, b: S) => boolean;

export function shallowEqual<S>(a: S, b: S): boolean {
  if (Object.is(a, b)) {
    return true;
  }
  if (typeof a !== "object" || a === null || typeof b !== "object" || b === null) {
    return false;
  }
  const keysA = Object.keys(a) as (keyof S)[];
  const keysB = Object.keys(b) as (keyof S)[];
  if (keysA.length !== keysB.length) {
    return false;
  }
  for (const key of keysA) {
    if (!Object.prototype.hasOwnProperty.call(b, key) || !Object.is(a[key], b[key])) {
      return false;
    }
  }
  return true;
}

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
    const nextState = { ...this.state, ...patch };
    if (shallowEqual(this.state, nextState)) {
      return;
    }
    this.state = nextState;
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

  public subscribeSelector<S>(
    selector: Selector<T, S>,
    listener: (selected: S, prevSelected: S | undefined) => void,
    isEqual: EqualityFn<S> = shallowEqual,
  ): () => void {
    // EN: Subscribe to a derived slice of state and emit only when slice changes | ES: Suscribirse a una porcion derivada del estado y emitir solo cuando cambia
    const state = {
      hasPrev: false,
      currentSlice: undefined as unknown as S,
    };

    return this.subscribe((nextState) => {
      const nextSlice = selector(nextState);
      if (!state.hasPrev || !isEqual(state.currentSlice, nextSlice)) {
        const prevSlice = state.hasPrev ? state.currentSlice : undefined;
        state.currentSlice = nextSlice;
        state.hasPrev = true;
        listener(nextSlice, prevSlice);
      }
    });
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
  availableFrameworks: [],
  latestImpact: null,
  isLoading: false,
  errorMessage: null,
  lastFailedOperation: null,
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
      lastFailedOperation: null,
    });
  },

  setAvailableFrameworks: (availableFrameworks: FrameworkInfo[]): void => {
    // EN: Drop selected ids the backend no longer supports, falling back to the first entry | ES: Descartar ids seleccionados que el backend ya no soporta, usando la primera entrada como respaldo
    const known = new Set(availableFrameworks.map((f) => f.id));
    const kept = appStore.getState().selectedFrameworks.filter((id) => known.has(id));
    const selectedFrameworks = kept.length > 0 ? kept : availableFrameworks.slice(0, 1).map((f) => f.id);
    appStore.setState({ availableFrameworks, selectedFrameworks });
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
      lastFailedOperation: null,
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
      lastFailedOperation: null,
    });
  },

  setError: (errorMessage: string | null, failedOperation: FailedOperation | null = null): void => {
    appStore.setState({
      errorMessage,
      isLoading: false,
      lastFailedOperation: failedOperation ?? appStore.getState().lastFailedOperation,
    });
  },

  clearError: (): void => {
    appStore.setState({ errorMessage: null, lastFailedOperation: null });
  },

  loadInitialCases: async (): Promise<void> => {
    try {
      actions.setLoading(true);
      const [caseSummaries, frameworks] = await Promise.all([
        ApiService.fetchCaseStudies(),
        ApiService.fetchFrameworks(),
      ]);
      actions.setAvailableFrameworks(frameworks);
      actions.setCaseList(caseSummaries);

      if (caseSummaries.length > 0) {
        await actions.loadCaseStudy(caseSummaries[0].id);
      }
    } catch (err: unknown) {
      const errorMsg =
        err instanceof Error
          ? err.message
          : "Failed to connect to AI Ethics Simulator backend.";
      actions.setError(
        `Connection error: ${errorMsg}. Please ensure the FastAPI backend service is running on port 8000.`,
        { type: "LOAD_CASES" },
      );
    } finally {
      actions.setLoading(false);
    }
  },

  loadCaseStudy: async (caseId: string): Promise<void> => {
    actions.setLoading(true);
    try {
      const caseData = await ApiService.fetchCaseStudy(caseId);
      actions.setCurrentCase(caseData);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Failed to load case study.";
      actions.setError(msg, { type: "LOAD_CASE_DETAIL", caseId });
    } finally {
      actions.setLoading(false);
    }
  },

  submitDecisionEvaluation: async (
    caseId: string,
    selectedOptionId: string,
    userRationale: string,
    frameworks: string[],
  ): Promise<void> => {
    actions.setLoading(true);
    try {
      const impact = await ApiService.submitDecision(
        caseId,
        selectedOptionId,
        userRationale,
        frameworks,
      );
      actions.setImpactResult(impact);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Decision evaluation failed.";
      actions.setError(msg, {
        type: "SUBMIT_DECISION",
        caseId,
        selectedOptionId,
        userRationale,
        frameworks,
      });
    } finally {
      actions.setLoading(false);
    }
  },

  retryLastOperation: async (): Promise<void> => {
    const { lastFailedOperation, cases, selectedCaseId, currentCase, selectedOptionId, userRationale, selectedFrameworks } =
      appStore.getState();

    if (lastFailedOperation) {
      if (lastFailedOperation.type === "LOAD_CASES") {
        await actions.loadInitialCases();
        return;
      }
      if (lastFailedOperation.type === "LOAD_CASE_DETAIL") {
        await actions.loadCaseStudy(lastFailedOperation.caseId);
        return;
      }
      if (lastFailedOperation.type === "SUBMIT_DECISION") {
        await actions.submitDecisionEvaluation(
          lastFailedOperation.caseId,
          lastFailedOperation.selectedOptionId,
          lastFailedOperation.userRationale,
          lastFailedOperation.frameworks,
        );
        return;
      }
    }

    // EN: Fallback inference when error was set without an explicit operation descriptor | ES: Inferencia de respaldo cuando el error se fijo sin descriptor explicito de operacion
    if (cases.length === 0) {
      await actions.loadInitialCases();
    } else if (!currentCase && selectedCaseId) {
      await actions.loadCaseStudy(selectedCaseId);
    } else if (currentCase && selectedOptionId && userRationale.trim().length >= 10) {
      await actions.submitDecisionEvaluation(
        currentCase.id,
        selectedOptionId,
        userRationale,
        selectedFrameworks,
      );
    } else {
      actions.clearError();
    }
  },
};
