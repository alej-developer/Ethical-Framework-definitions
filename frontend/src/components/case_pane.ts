/** EN: Left split pane component rendering linguistic case study context, corpus artifacts, and baseline matrix. | ES: Componente del panel izquierdo que renderiza el contexto del caso linguistico, artefactos del corpus y matriz base. */

import { getTranslation } from "../i18n/translations.ts";
import { ApiService } from "../services/api.ts";
import { actions, appStore } from "../state/store.ts";
import { CaseStudy, CaseStudySummary, Language } from "../types/index.ts";

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
    appStore.subscribe((state) => {
      this.render(state.cases, state.currentCase, state.selectedCaseId, state.language);
    });
  }

  private render(
    cases: CaseStudySummary[],
    currentCase: CaseStudy | null,
    selectedId: string | null,
    lang: Language,
  ): void {
    const sectionTitle = getTranslation("caseStudiesSectionTitle", lang);
    const sectionDesc = getTranslation("caseStudiesSectionDesc", lang);

    if (cases.length === 0) {
      this.container.innerHTML = `
        <div class="pane" role="region" aria-labelledby="left-pane-heading">
          <div class="pane-header">
            <h2 id="left-pane-heading" class="pane-title">${sectionTitle}</h2>
            <p class="pane-subtitle">${sectionDesc}</p>
          </div>
          <div class="pane-content">
            <div class="empty-state">
              <p class="empty-state-title">${getTranslation("emptyStateTitle", lang)}</p>
              <p class="empty-state-text">Loading computational linguistics cases...</p>
            </div>
          </div>
        </div>
      `;
      return;
    }

    this.container.innerHTML = `
      <div class="pane" role="region" aria-labelledby="left-pane-heading">
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
              data-id="${c.id}"
              aria-selected="${c.id === selectedId ? "true" : "false"}"
              role="tab"
            >
              ${c.title.split(":")[0] || c.title}
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
              <p class="empty-state-text">Loading selected case specification...</p>
            </div>
          `
              : `
            <!-- EN: Case Header & Metadata | ES: Cabecera y Metadatos del Caso -->
            <div class="section-block">
              <h3 class="case-headline">${currentCase.title}</h3>
              <div class="case-meta-row">
                <span class="meta-chip">DOMAIN: ${currentCase.nlp_domain}</span>
                <span class="meta-chip">TASK: ${currentCase.task_type}</span>
                <span class="meta-chip">CATEGORY: ${currentCase.domain_category}</span>
              </div>
            </div>

            <!-- EN: Ethical Dilemma Callout | ES: Cuadro de Dilema Etico -->
            <div class="section-block">
              <span class="section-label">${getTranslation("dilemmaHeading", lang)}</span>
              <div class="dilemma-callout" role="alert">
                <p>${currentCase.dilemma}</p>
              </div>
            </div>

            <!-- EN: Operational Context Narrative | ES: Narrativa del Contexto Operativo -->
            <div class="section-block">
              <span class="section-label">${getTranslation("contextHeading", lang)}</span>
              <p class="context-body">${currentCase.context_description}</p>
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
                        <td class="sample-text">"${a.text_sample}"</td>
                        <td><span class="meta-chip">${a.dialect_or_variety}</span></td>
                        <td>${a.expected_output}</td>
                        <td>
                          <span class="status-badge ${
                            a.observed_output === a.expected_output ? "match" : "mismatch"
                          }">
                            ${a.observed_output}
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
                    <strong>${framework.replace(/_/g, " ")}</strong>
                    <span>${text}</span>
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
          actions.setLoading(true);
          try {
            const caseData = await ApiService.fetchCaseStudy(id);
            actions.setCurrentCase(caseData);
          } catch (err: unknown) {
            const msg = err instanceof Error ? err.message : "Failed to load case study.";
            actions.setError(msg);
          } finally {
            actions.setLoading(false);
          }
        }
      });
    });
  }
}
