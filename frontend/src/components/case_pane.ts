/** EN: Left split pane component rendering linguistic case study context, corpus artifacts, and baseline matrix. | ES: Componente del panel izquierdo que renderiza el contexto del caso linguistico, artefactos del corpus y matriz base. */

import { getTranslation } from "../i18n/translations.ts";
import { actions, appStore } from "../state/store.ts";
import { CaseStudy, CaseStudySummary, Language } from "../types/index.ts";
import { escapeHtml } from "../utils/escape_html.ts";

export class CasePaneComponent {
  private container: HTMLElement;

  constructor(containerId: string) {
    const el = document.getElementById(containerId);
    if (!el) {
      throw new Error(`Element with ID '${containerId}' was not found.`);
    }
    this.container = el;
    this.init();
  }

  private init(): void {
    appStore.subscribeSelector(
      (state) => ({
        cases: state.cases,
        currentCase: state.currentCase,
        selectedCaseId: state.selectedCaseId,
        language: state.language,
        isLoading: state.isLoading,
      }),
      (slice, prevSlice) => {
        // EN: If only isLoading changed and the pane DOM already exists, update loading attributes without rebuilding the DOM | ES: Si solo cambio isLoading y el DOM del panel ya existe, actualizar atributos de carga sin reconstruir el DOM
        if (
          prevSlice &&
          prevSlice.cases === slice.cases &&
          prevSlice.currentCase === slice.currentCase &&
          prevSlice.selectedCaseId === slice.selectedCaseId &&
          prevSlice.language === slice.language &&
          prevSlice.isLoading !== slice.isLoading
        ) {
          this.updateLoadingState(slice.isLoading);
          return;
        }
        this.render(
          slice.cases,
          slice.currentCase,
          slice.selectedCaseId,
          slice.language,
          slice.isLoading,
        );
      },
    );
  }

  private updateLoadingState(isLoading: boolean): void {
    const pane = this.container.querySelector<HTMLElement>(".pane");
    if (pane) {
      pane.setAttribute("aria-busy", isLoading ? "true" : "false");
      pane.classList.toggle("is-loading", isLoading);
    }
    const tabButtons = this.container.querySelectorAll<HTMLButtonElement>(".case-tab-btn");
    tabButtons.forEach((btn) => {
      btn.disabled = isLoading;
    });
  }

  private render(
    cases: CaseStudySummary[],
    currentCase: CaseStudy | null,
    selectedId: string | null,
    lang: Language,
    isLoading = false,
  ): void {
    const sectionTitle = getTranslation("caseStudiesSectionTitle", lang);
    const sectionDesc = getTranslation("caseStudiesSectionDesc", lang);

    if (cases.length === 0) {
      this.container.innerHTML = `
        <div class="pane ${isLoading ? "is-loading" : ""}" role="region" aria-labelledby="left-pane-heading" aria-busy="${isLoading ? "true" : "false"}">
          <div class="pane-header">
            <h2 id="left-pane-heading" class="pane-title">${sectionTitle}</h2>
            <p class="pane-subtitle">${sectionDesc}</p>
          </div>
          <div class="pane-content">
            <div class="empty-state">
              <p class="empty-state-title">${getTranslation("emptyStateTitle", lang)}</p>
              <p class="empty-state-text">${getTranslation("loadingCasesText", lang)}</p>
            </div>
          </div>
        </div>
      `;
      return;
    }

    this.container.innerHTML = `
      <div class="pane ${isLoading ? "is-loading" : ""}" role="region" aria-labelledby="left-pane-heading" aria-busy="${isLoading ? "true" : "false"}">
        <div class="pane-header">
          <h2 id="left-pane-heading" class="pane-title">${sectionTitle}</h2>
          <p class="pane-subtitle">${sectionDesc}</p>
        </div>

        <!-- EN: Case Studies Selector Tabs | ES: Pestanas de Seleccion de Casos de Estudio -->
        <nav class="case-tabs-nav" aria-label="Linguistic Case Studies Selector">
          ${cases
            .map(
              (c) => `
            <button 
              type="button" 
              class="case-tab-btn" 
              data-id="${escapeHtml(c.id)}"
              aria-selected="${c.id === selectedId ? "true" : "false"}"
              role="tab"
              ${isLoading ? "disabled" : ""}
            >
              ${escapeHtml(c.title.split(":")[0] || c.title)}
            </button>
          `
            )
            .join("")}
        </nav>

        <div class="pane-content">
          ${
            !currentCase
              ? `
            <div class="empty-state">
              <p class="empty-state-title">${getTranslation("emptyStateTitle", lang)}</p>
              <p class="empty-state-text">${getTranslation("loadingCaseSpecText", lang)}</p>
            </div>
          `
              : `
            <!-- EN: Case Header & Metadata | ES: Cabecera y Metadatos del Caso -->
            <div class="section-block">
              <h3 class="case-headline">${escapeHtml(currentCase.title)}</h3>
              <div class="case-meta-row">
                <span class="meta-chip">DOMAIN: ${escapeHtml(currentCase.nlp_domain)}</span>
                <span class="meta-chip">TASK: ${escapeHtml(currentCase.task_type)}</span>
                <span class="meta-chip">CATEGORY: ${escapeHtml(currentCase.domain_category)}</span>
              </div>
            </div>

            <!-- EN: Ethical Dilemma Callout | ES: Cuadro de Dilema Etico -->
            <div class="section-block">
              <span class="section-label">${getTranslation("dilemmaHeading", lang)}</span>
              <div class="dilemma-callout" role="alert">
                <p>${escapeHtml(currentCase.dilemma)}</p>
              </div>
            </div>

            <!-- EN: Operational Context Narrative | ES: Narrativa del Contexto Operativo -->
            <div class="section-block">
              <span class="section-label">${getTranslation("contextHeading", lang)}</span>
              <p class="context-body">${escapeHtml(currentCase.context_description)}</p>
            </div>

            <!-- EN: Linguistic Artifacts Corpus Table | ES: Tabla de Artefactos del Corpus Linguistico -->
            <div class="section-block">
              <span class="section-label">${getTranslation("artifactsHeading", lang)}</span>
              <div class="table-wrapper">
                <table class="data-table" aria-label="${getTranslation("artifactsHeading", lang)}">
                  <thead>
                    <tr>
                      <th scope="col">${getTranslation("colSampleText", lang)}</th>
                      <th scope="col">${getTranslation("colVariety", lang)}</th>
                      <th scope="col">${getTranslation("colExpected", lang)}</th>
                      <th scope="col">${getTranslation("colObserved", lang)}</th>
                      <th scope="col">${getTranslation("colConfidence", lang)}</th>
                    </tr>
                  </thead>
                  <tbody>
                    ${currentCase.linguistic_artifacts
                      .map(
                        (a) => `
                      <tr class="${a.observed_output !== a.expected_output ? "disparity-row" : ""}">
                        <td class="sample-text">"${escapeHtml(a.text_sample)}"</td>
                        <td><span class="meta-chip">${escapeHtml(a.dialect_or_variety)}</span></td>
                        <td>${escapeHtml(a.expected_output)}</td>
                        <td>
                          <span class="status-badge ${
                            a.observed_output === a.expected_output ? "match" : "mismatch"
                          }">
                            ${escapeHtml(a.observed_output)}
                          </span>
                        </td>
                        <td class="tabular-num">${(a.confidence_score * 100).toFixed(1)}%</td>
                      </tr>
                    `
                      )
                      .join("")}
                  </tbody>
                </table>
              </div>
            </div>

            <!-- EN: Predefined Baseline Matrix Grid | ES: Cuadricula de Matriz Base Predefinida -->
            <div class="section-block">
              <span class="section-label">${getTranslation("baselineMatrixHeading", lang)}</span>
              <div class="matrix-grid">
                <div class="matrix-card">
                  <span class="matrix-dim-name">${getTranslation("dimensionTransparency", lang)}</span>
                  <span class="matrix-score-val tabular-num">${(
                    currentCase.baseline_matrix.TRANSPARENCY ?? 0.5
                  ).toFixed(2)}</span>
                </div>
                <div class="matrix-card">
                  <span class="matrix-dim-name">${getTranslation("dimensionAccountability", lang)}</span>
                  <span class="matrix-score-val tabular-num">${(
                    currentCase.baseline_matrix.ACCOUNTABILITY ?? 0.5
                  ).toFixed(2)}</span>
                </div>
                <div class="matrix-card">
                  <span class="matrix-dim-name">${getTranslation("dimensionFairness", lang)}</span>
                  <span class="matrix-score-val tabular-num">${(
                    currentCase.baseline_matrix.FAIRNESS ?? 0.5
                  ).toFixed(2)}</span>
                </div>
              </div>
            </div>

            <!-- EN: Regulatory Implications | ES: Implicaciones Regulatorias -->
            <div class="section-block">
              <span class="section-label">${getTranslation("regulatoryHeading", lang)}</span>
              <div class="regulatory-list">
                ${Object.entries(currentCase.regulatory_implications)
                  .map(
                    ([framework, text]) => `
                  <div class="reg-item">
                    <strong>${escapeHtml(framework.replace(/_/g, " "))}</strong>
                    <span>${escapeHtml(text)}</span>
                  </div>
                `
                  )
                  .join("")}
              </div>
            </div>
          `
          }
        </div>
      </div>
    `;

    // EN: Attach event listeners to tab buttons | ES: Adjuntar escuchadores de eventos a botones de pestanas
    const tabButtons = this.container.querySelectorAll<HTMLButtonElement>(".case-tab-btn");
    tabButtons.forEach((btn) => {
      btn.addEventListener("click", async () => {
        const id = btn.getAttribute("data-id");
        if (id && id !== selectedId) {
          await actions.loadCaseStudy(id);
        }
      });
    });
  }
}
