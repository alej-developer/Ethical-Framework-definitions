/** EN: Framework selector and evaluation trigger component. | ES: Componente selector de marcos y activador de evaluacion. */

import { ApiService } from "../services/api.ts";
import { actions, appStore } from "../state/store.ts";

export class FrameworkSelectorComponent {
  private container: HTMLElement;

  constructor(containerId: string) {
    const el = document.getElementById(containerId);
    if (!el) {
      throw new Error(`Element with id '${containerId}' was not found.`);
    }
    this.container = el;
    this.init();
  }

  private init(): void {
    appStore.subscribe((state) => {
      this.render(state.selectedFrameworks, state.isLoading, state.selectedScenarioId);
    });
  }

  private render(
    selectedFrameworks: string[],
    isLoading: boolean,
    selectedScenarioId: string | null,
  ): void {
    const isEUSelected = selectedFrameworks.includes("EU_AI_ACT");
    const isIEEESelected = selectedFrameworks.includes("IEEE_7000_SERIES");

    this.container.innerHTML = `
      <div class="framework-controls-panel">
        <div class="framework-options">
          <h3 class="panel-subtitle">EN: Ethical Framework Directives | ES: Directivas de Marcos Eticos</h3>
          <div class="framework-toggles">
            <label class="framework-toggle-card ${isEUSelected ? "selected" : ""}">
              <input 
                type="checkbox" 
                class="framework-checkbox" 
                value="EU_AI_ACT" 
                ${isEUSelected ? "checked" : ""}
              />
              <div class="toggle-content">
                <span class="framework-code">REGULATION EU 2024/1689</span>
                <strong class="framework-title">EU Artificial Intelligence Act</strong>
                <p class="framework-desc">
                  EN: Audits prohibited practices (Art. 5), high-risk classification (Annex III), dialectal bias parity (Art. 10), and transparency (Art. 50).
                  | ES: Audita practicas prohibidas (Art. 5), clasificacion de alto riesgo (Anexo III), paridad de sesgo dialectal (Art. 10) y transparencia (Art. 50).
                </p>
              </div>
            </label>

            <label class="framework-toggle-card ${isIEEESelected ? "selected" : ""}">
              <input 
                type="checkbox" 
                class="framework-checkbox" 
                value="IEEE_7000_SERIES" 
                ${isIEEESelected ? "checked" : ""}
              />
              <div class="toggle-content">
                <span class="framework-code">IEEE STD 7000 & 7001</span>
                <strong class="framework-title">IEEE Standards for Ethical AI</strong>
                <p class="framework-desc">
                  EN: Measures value-based system design, psychological harm prevention, well-being index, and multi-stakeholder algorithmic transparency.
                  | ES: Mide diseno de sistemas basado en valores, prevencion de dano psicologico, indice de bienestar y transparencia algoritmica para partes interesadas.
                </p>
              </div>
            </label>
          </div>
        </div>

        <div class="action-footer">
          <button 
            type="button" 
            id="btn-run-evaluation" 
            class="btn-primary" 
            ${isLoading || !selectedScenarioId ? "disabled" : ""}
          >
            ${isLoading ? "Simulating Ethical Audit..." : "Execute Ethical Simulation Audit"}
          </button>
        </div>
      </div>
    `;

    // EN: Attach event listeners to checkboxes | ES: Adjuntar escuchadores de eventos a casillas de verificacion
    const checkboxes = this.container.querySelectorAll<HTMLInputElement>(".framework-checkbox");
    checkboxes.forEach((cb) => {
      cb.addEventListener("change", () => {
        actions.toggleFramework(cb.value);
      });
    });

    // EN: Attach event listener to evaluation trigger button | ES: Adjuntar escuchador de eventos al boton de ejecucion de evaluacion
    const runBtn = this.container.querySelector<HTMLButtonElement>("#btn-run-evaluation");
    if (runBtn) {
      runBtn.addEventListener("click", () => {
        this.executeEvaluation();
      });
    }
  }

  private async executeEvaluation(): Promise<void> {
    const state = appStore.getState();
    if (!state.selectedScenarioId) {
      return;
    }

    actions.setLoading(true);
    try {
      const assessment = await ApiService.evaluateScenario(
        state.selectedScenarioId,
        state.selectedFrameworks,
      );
      actions.setAssessment(assessment);
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : "Unexpected evaluation failure.";
      actions.setError(message);
    }
  }
}
