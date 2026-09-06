/** EN: Scenario selector component for browsing computational linguistics benchmarks. | ES: Componente selector de escenarios para explorar referencias de linguistica computacional. */

import { actions, appStore } from "../state/store.ts";
import { Scenario } from "../types/index.ts";

export class ScenarioSelectorComponent {
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
    // EN: Subscribe to state changes to update scenario cards and artifact details | ES: Suscribirse a cambios de estado para actualizar tarjetas de escenarios y detalles de artefactos
    appStore.subscribe((state) => {
      this.render(state.scenarios, state.selectedScenarioId);
    });
  }

  private render(scenarios: Scenario[], selectedId: string | null): void {
    if (scenarios.length === 0) {
      this.container.innerHTML = `
        <div class="panel-loading">
          <p>EN: Loading computational linguistics benchmarks... | ES: Cargando escenarios de referencia de linguistica computacional...</p>
        </div>
      `;
      return;
    }

    const selected = scenarios.find((s) => s.id === selectedId) || scenarios[0];

    this.container.innerHTML = `
      <div class="scenarios-layout">
        <div class="scenarios-sidebar">
          <h3 class="panel-subtitle">EN: Benchmark Scenarios | ES: Escenarios de Referencia</h3>
          <div class="scenario-list">
            ${scenarios
              .map(
                (s) => `
              <button 
                type="button" 
                class="scenario-card ${s.id === selected.id ? "active" : ""}" 
                data-id="${s.id}"
              >
                <div class="scenario-card-header">
                  <span class="badge-category">${s.domain_category}</span>
                  <span class="badge-task">${s.task_type}</span>
                </div>
                <h4 class="scenario-card-title">${s.title}</h4>
                <p class="scenario-card-desc">${s.description.slice(0, 95)}...</p>
              </button>
            `
              )
              .join("")}
          </div>
        </div>

        <div class="scenario-detail">
          <div class="detail-header">
            <h3 class="detail-title">${selected.title}</h3>
            <div class="detail-meta">
              <span class="meta-tag">ID: ${selected.id}</span>
              <span class="meta-tag">Domain: ${selected.domain_category}</span>
              <span class="meta-tag">Task: ${selected.task_type}</span>
            </div>
          </div>
          <p class="detail-description">${selected.description}</p>

          <div class="artifacts-container">
            <h4 class="artifacts-title">EN: Linguistic Artifacts Sample Corpus | ES: Corpus Muestra de Artefactos Linguisticos</h4>
            <div class="table-responsive">
              <table class="artifacts-table">
                <thead>
                  <tr>
                    <th>Sample Text</th>
                    <th>Dialect / Variety</th>
                    <th>Expected</th>
                    <th>Observed</th>
                    <th>Confidence</th>
                  </tr>
                </thead>
                <tbody>
                  ${selected.artifacts
                    .map(
                      (a) => `
                    <tr class="${a.observed_output !== a.expected_output ? "row-disparity" : ""}">
                      <td class="cell-text">"${a.text_sample}"</td>
                      <td><span class="badge-variety">${a.dialect_or_variety}</span></td>
                      <td><span class="badge-expected">${a.expected_output}</span></td>
                      <td>
                        <span class="badge-observed ${
                          a.observed_output === a.expected_output ? "match" : "mismatch"
                        }">
                          ${a.observed_output}
                        </span>
                      </td>
                      <td>${(a.confidence_score * 100).toFixed(1)}%</td>
                    </tr>
                  `
                    )
                    .join("")}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    `;

    // EN: Attach event listeners to scenario buttons | ES: Adjuntar escuchadores de eventos a botones de escenarios
    const buttons = this.container.querySelectorAll<HTMLButtonElement>(".scenario-card");
    buttons.forEach((btn) => {
      btn.addEventListener("click", () => {
        const id = btn.getAttribute("data-id");
        if (id) {
          actions.selectScenario(id);
        }
      });
    });
  }
}
