/** EN: Left split pane component rendering linguistic case study context, corpus artifacts, and baseline matrix. | ES: Componente del panel izquierdo que renderiza el contexto del caso linguistico, artefactos del corpus y matriz base. */

import { getTranslation } from "../i18n/translations.ts";
import { actions, appStore } from "../state/store.ts";
import { CaseStudy, CaseStudySummary, Language } from "../types/index.ts";
import { escapeHtml } from "../utils/escape_html.ts";

export class CasePaneComponent {
  private container: HTMLElement;
  private pendingTabFocusId: string | null = null;

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
      btn.setAttribute("aria-disabled", isLoading ? "true" : "false");
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

    const activeTabId = cases.some((c) => c.id === selectedId) ? selectedId : cases[0].id;
    const wasTabFocused = Boolean(
      this.container.querySelector(".case-tabs-nav")?.contains(document.activeElement),
    );

    this.container.innerHTML = `
      <div class="pane ${isLoading ? "is-loading" : ""}" role="region" aria-labelledby="left-pane-heading" aria-busy="${isLoading ? "true" : "false"}">
        <div class="pane-header">
          <h2 id="left-pane-heading" class="pane-title">${sectionTitle}</h2>
          <p class="pane-subtitle">${sectionDesc}</p>
        </div>

        <!-- EN: Case Studies Selector Tabs | ES: Pestanas de Seleccion de Casos de Estudio -->
        <div class="case-tabs-nav" role="tablist" aria-labelledby="left-pane-heading">
          ${cases
            .map((c) => {
              const isSelected = c.id === activeTabId;
              return `
            <button 
              type="button" 
              id="case-tab-${escapeHtml(c.id)}"
              class="case-tab-btn" 
              data-id="${escapeHtml(c.id)}"
              aria-selected="${isSelected ? "true" : "false"}"
              aria-controls="case-tabpanel"
              aria-disabled="${isLoading ? "true" : "false"}"
              tabindex="${isSelected ? "0" : "-1"}"
              role="tab"
            >
              ${escapeHtml(c.title.split(":")[0] || c.title)}
            </button>
          `;
            })
            .join("")}
        </div>

        <div
          id="case-tabpanel"
          class="pane-content"
          role="tabpanel"
          aria-labelledby="case-tab-${escapeHtml(activeTabId)}"
          tabindex="0"
        >
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

    // EN: Attach click and WAI-ARIA keyboard navigation listeners to tab buttons | ES: Adjuntar escuchadores de clic y navegacion por teclado WAI-ARIA a botones de pestanas
    const tabButtons = Array.from(this.container.querySelectorAll<HTMLButtonElement>(".case-tab-btn"));

    const activateTab = async (tabBtn: HTMLButtonElement, preserveFocus: boolean): Promise<void> => {
      if (appStore.getState().isLoading) {
        return;
      }
      const id = tabBtn.getAttribute("data-id");
      if (id && id !== selectedId) {
        this.pendingTabFocusId = preserveFocus ? id : null;
        await actions.loadCaseStudy(id);
      }
    };

    tabButtons.forEach((btn, index) => {
      btn.addEventListener("click", async () => {
        await activateTab(btn, false);
      });

      btn.addEventListener("keydown", async (event: KeyboardEvent) => {
        if (tabButtons.length === 0) return;

        let targetIndex: number | null = null;
        if (event.key === "ArrowRight") {
          targetIndex = (index + 1) % tabButtons.length;
        } else if (event.key === "ArrowLeft") {
          targetIndex = (index - 1 + tabButtons.length) % tabButtons.length;
        } else if (event.key === "Home") {
          targetIndex = 0;
        } else if (event.key === "End") {
          targetIndex = tabButtons.length - 1;
        }

        if (targetIndex !== null) {
          event.preventDefault();
          const targetTab = tabButtons[targetIndex];
          targetTab.focus();
          await activateTab(targetTab, true);
        }
      });
    });

    if (this.pendingTabFocusId || wasTabFocused) {
      const targetId = this.pendingTabFocusId ?? activeTabId;
      this.pendingTabFocusId = null;
      const targetTab = tabButtons.find((btn) => btn.getAttribute("data-id") === targetId);
      targetTab?.focus();
    }
  }
}
