/** EN: Right split pane component rendering interactive decision tree, rationale input, and real-time EU AI Act / matrix compliance metrics. | ES: Componente del panel derecho que renderiza el arbol de decision interactivo, entrada de justificacion y metricas de cumplimiento en tiempo real. */

import { getTranslation } from "../i18n/translations.ts";
import { ApiService } from "../services/api.ts";
import { actions, appStore } from "../state/store.ts";
import {
  CaseStudy,
  DecisionImpactResponse,
  Language,
} from "../types/index.ts";

export class DecisionPaneComponent {
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
      this.render(
        state.currentCase,
        state.selectedOptionId,
        state.userRationale,
        state.selectedFrameworks,
        state.latestImpact,
        state.isLoading,
        state.errorMessage,
        state.language,
      );
    });
  }

  private render(
    currentCase: CaseStudy | null,
    selectedOptionId: string | null,
    rationale: string,
    frameworks: string[],
    impact: DecisionImpactResponse | null,
    isLoading: boolean,
    errorMessage: string | null,
    lang: Language,
  ): void {
    const isEUSel = frameworks.includes("EU_AI_ACT");
    const isIEEESel = frameworks.includes("IEEE_7000_SERIES");
    const isRationaleValid = rationale.trim().length >= 10;
    const canSubmit = Boolean(currentCase && selectedOptionId && isRationaleValid && !isLoading);

    this.container.innerHTML = `
      <div class="pane" role="region" aria-labelledby="right-pane-heading">
        <div class="pane-header">
          <h2 id="right-pane-heading" class="pane-title">${getTranslation("decisionTreeHeading", lang)}</h2>
          <p class="pane-subtitle">${getTranslation("decisionTreeDesc", lang)}</p>
        </div>

        <div class="pane-content">
          ${
            errorMessage
              ? `
            <div class="alert-error" role="alert" aria-live="assertive">
              <span><strong>${getTranslation("errorTitle", lang)}:</strong> ${errorMessage}</span>
              <button type="button" id="btn-dismiss-error" class="btn-lang-toggle">${getTranslation("retryButtonText", lang)}</button>
            </div>
          `
              : ""
          }

          ${
            !currentCase
              ? `
            <div class="empty-state">
              <p class="empty-state-title">${getTranslation("emptyStateTitle", lang)}</p>
              <p class="empty-state-text">Select a case study to display decision alternatives.</p>
            </div>
          `
              : `
            <!-- EN: Interactive Decision Tree | ES: Arbol de Decision Interactivo -->
            <div class="section-block">
              <span class="section-label">${getTranslation("decisionTreeHeading", lang)}</span>
              <div class="decision-tree-group" role="radiogroup" aria-label="${getTranslation("decisionTreeHeading", lang)}">
                ${currentCase.decision_options
                  .map(
                    (opt) => `
                  <label 
                    class="decision-option-card ${opt.id === selectedOptionId ? "selected" : ""}" 
                    for="radio-${opt.id}"
                  >
                    <input 
                      type="radio" 
                      id="radio-${opt.id}" 
                      name="decision-option" 
                      class="decision-radio" 
                      value="${opt.id}"
                      ${opt.id === selectedOptionId ? "checked" : ""}
                      aria-checked="${opt.id === selectedOptionId ? "true" : "false"}"
                    />
                    <div class="option-body">
                      <span class="option-strategy-chip">${opt.strategy}</span>
                      <strong class="option-title">${opt.title}</strong>
                      <p class="option-desc">${opt.description}</p>
                      
                      <div class="modifier-chips-row" aria-label="Estimated Impact Modifiers">
                        ${Object.entries(opt.dimension_modifiers)
                          .map(([dim, val]) => {
                            const sign = val > 0 ? "+" : "";
                            const cls = val > 0 ? "positive" : val < 0 ? "negative" : "neutral";
                            return `<span class="modifier-chip ${cls}">${dim}: ${sign}${val.toFixed(2)}</span>`;
                          })
                          .join("")}
                      </div>
                    </div>
                  </label>
                `
                  )
                  .join("")}
              </div>
            </div>

            <!-- EN: Decision Rationale Form | ES: Formulario de Justificacion de la Decision -->
            <div class="section-block">
              <span class="section-label">${getTranslation("rationaleHeading", lang)}</span>
              <textarea 
                id="input-user-rationale" 
                class="rationale-input" 
                placeholder="${getTranslation("rationalePlaceholder", lang)}"
                aria-label="${getTranslation("rationaleHeading", lang)}"
                aria-describedby="rationale-hint"
              >${rationale}</textarea>
              <div id="rationale-hint" class="form-hint">
                <span>${getTranslation("rationaleMinCharsNote", lang)}</span>
                <span class="tabular-num">${rationale.trim().length} chars</span>
              </div>
            </div>

            <!-- EN: Target Frameworks Selector | ES: Selector de Marcos Objetivo -->
            <div class="section-block">
              <span class="section-label">${getTranslation("frameworksHeading", lang)}</span>
              <div class="regulatory-list">
                <label class="reg-item" style="cursor: pointer; display: flex; gap: var(--space-xs); align-items: center;">
                  <input type="checkbox" class="cb-framework" value="EU_AI_ACT" ${isEUSel ? "checked" : ""} />
                  <div>
                    <strong>${getTranslation("frameworkEU", lang)}</strong>
                    <span style="font-size: 0.75rem;">${getTranslation("frameworkEUDesc", lang)}</span>
                  </div>
                </label>
                <label class="reg-item" style="cursor: pointer; display: flex; gap: var(--space-xs); align-items: center;">
                  <input type="checkbox" class="cb-framework" value="IEEE_7000_SERIES" ${isIEEESel ? "checked" : ""} />
                  <div>
                    <strong>${getTranslation("frameworkIEEE", lang)}</strong>
                    <span style="font-size: 0.75rem;">${getTranslation("frameworkIEEEDesc", lang)}</span>
                  </div>
                </label>
              </div>
            </div>

            <!-- EN: Submit Evaluation Action | ES: Accion de Envio de Evaluacion -->
            <button 
              type="button" 
              id="btn-execute-eval" 
              class="btn-submit-eval" 
              ${!canSubmit ? "disabled" : ""}
              aria-busy="${isLoading ? "true" : "false"}"
            >
              ${isLoading ? getTranslation("evaluatingText", lang) : getTranslation("submitButtonText", lang)}
            </button>

            <!-- EN: Real-Time Results Dashboard | ES: Panel de Resultados en Tiempo Real -->
            <div class="results-container" aria-live="polite">
              <span class="section-label">${getTranslation("evaluationResultsHeading", lang)}</span>
              ${
                !impact
                  ? `
                <div class="empty-state">
                  <p class="empty-state-title">${getTranslation("emptyStateTitle", lang)}</p>
                  <p class="empty-state-text">${getTranslation("emptyStateDesc", lang)}</p>
                </div>
              `
                  : `
                <!-- EN: Multidimensional Matrix Impact Cards | ES: Tarjetas de Impacto de Matriz Multidimensional -->
                <div class="impact-matrix-display">
                  ${this.renderDimensionCard(
                    getTranslation("dimensionTransparency", lang),
                    impact.matrix.transparency.baseline_score,
                    impact.matrix.transparency.decision_score,
                    impact.matrix.transparency.delta,
                  )}
                  ${this.renderDimensionCard(
                    getTranslation("dimensionAccountability", lang),
                    impact.matrix.accountability.baseline_score,
                    impact.matrix.accountability.decision_score,
                    impact.matrix.accountability.delta,
                  )}
                  ${this.renderDimensionCard(
                    getTranslation("dimensionFairness", lang),
                    impact.matrix.fairness.baseline_score,
                    impact.matrix.fairness.decision_score,
                    impact.matrix.fairness.delta,
                  )}
                </div>

                <!-- EN: Overall Alignment Index | ES: Indice de Alineacion General -->
                <div class="matrix-card" style="align-items: center; text-align: center;">
                  <span class="matrix-dim-name">${getTranslation("overallAlignmentHeading", lang)}</span>
                  <span class="matrix-score-val tabular-num" style="font-size: 2.2rem;">
                    ${impact.matrix.overall_alignment.toFixed(3)}
                  </span>
                </div>

                <!-- EN: Statutory Risk Tier Banner | ES: Banner de Nivel de Riesgo Estatutario -->
                <div class="verdict-banner ${this.resolveRiskClass(impact.overall_risk_tier)}">
                  <div class="verdict-text-group">
                    <span class="verdict-sub">${getTranslation("riskTierLabel", lang)}</span>
                    <strong class="verdict-main">${this.translateRisk(impact.overall_risk_tier, lang)}</strong>
                  </div>
                  <div class="verdict-text-group" style="text-align: right;">
                    <span class="verdict-sub">${getTranslation("complianceStatusLabel", lang)}</span>
                    <strong class="verdict-main">${this.translateCompliance(impact.overall_compliance, lang)}</strong>
                  </div>
                </div>

                <!-- EN: Qualitative Trade-Off Analysis | ES: Analisis Cualitativo de Compensaciones -->
                <div class="section-block">
                  <span class="section-label">${getTranslation("tradeOffHeading", lang)}</span>
                  <div class="tradeoff-box">
                    <p>${impact.trade_off_analysis}</p>
                  </div>
                </div>

                <!-- EN: Statutory Remediation Directives | ES: Directivas Estatutarias de Subsanacion -->
                <div class="section-block">
                  <span class="section-label">${getTranslation("recommendationsHeading", lang)}</span>
                  <ul class="recs-list">
                    ${impact.recommendations.map((rec) => `<li>${rec}</li>`).join("")}
                  </ul>
                </div>
              `
              }
            </div>
          `
          }
        </div>
      </div>
    `;

    this.attachEventListeners(currentCase, selectedOptionId, rationale, frameworks);
  }

  private renderDimensionCard(name: string, baseline: number, current: number, delta: number): string {
    const sign = delta > 0 ? "+" : "";
    const deltaClass = delta > 0 ? "positive" : delta < 0 ? "negative" : "neutral";

    return `
      <div class="impact-card">
        <div class="impact-card-top">
          <span class="impact-dim">${name}</span>
          <span class="delta-pill ${deltaClass}">${sign}${delta.toFixed(2)}</span>
        </div>
        <div class="impact-score-row">
          <span class="impact-score-current tabular-num">${current.toFixed(2)}</span>
          <span class="impact-score-prev tabular-num">was ${baseline.toFixed(2)}</span>
        </div>
      </div>
    `;
  }

  private resolveRiskClass(tier: string): string {
    if (tier === "UNACCEPTABLE_RISK") return "unacceptable";
    if (tier === "HIGH_RISK") return "high-risk";
    return "compliant";
  }

  private translateRisk(tier: string, lang: Language): string {
    if (tier === "UNACCEPTABLE_RISK") return getTranslation("statusUnacceptableRisk", lang);
    if (tier === "HIGH_RISK") return getTranslation("statusHighRisk", lang);
    if (tier === "SPECIFIC_TRANSPARENCY_RISK") return getTranslation("statusSpecificTransparencyRisk", lang);
    return getTranslation("statusMinimalRisk", lang);
  }

  private translateCompliance(status: string, lang: Language): string {
    if (status === "PROHIBITED") return getTranslation("verdictProhibited", lang);
    if (status === "NON_COMPLIANT") return getTranslation("verdictNonCompliant", lang);
    if (status === "PARTIALLY_COMPLIANT") return getTranslation("verdictPartiallyCompliant", lang);
    return getTranslation("verdictCompliant", lang);
  }

  private attachEventListeners(
    currentCase: CaseStudy | null,
    selectedOptionId: string | null,
    rationale: string,
    frameworks: string[],
  ): void {
    // EN: Option selection listener | ES: Escuchador de seleccion de opcion
    const radios = this.container.querySelectorAll<HTMLInputElement>(".decision-radio");
    radios.forEach((r) => {
      r.addEventListener("change", () => {
        actions.selectOption(r.value);
      });
    });

    // EN: Rationale input listener | ES: Escuchador de entrada de justificacion
    const textarea = this.container.querySelector<HTMLTextAreaElement>("#input-user-rationale");
    if (textarea) {
      textarea.addEventListener("input", () => {
        actions.setUserRationale(textarea.value);
      });
    }

    // EN: Framework toggle listeners | ES: Escuchadores de alternancia de marcos
    const cbs = this.container.querySelectorAll<HTMLInputElement>(".cb-framework");
    cbs.forEach((cb) => {
      cb.addEventListener("change", () => {
        actions.toggleFramework(cb.value);
      });
    });

    // EN: Submit button listener | ES: Escuchador de boton de envio
    const submitBtn = this.container.querySelector<HTMLButtonElement>("#btn-execute-eval");
    if (submitBtn && currentCase && selectedOptionId) {
      submitBtn.addEventListener("click", async () => {
        actions.setLoading(true);
        try {
          const impact = await ApiService.submitDecision(
            currentCase.id,
            selectedOptionId,
            rationale,
            frameworks,
          );
          actions.setImpactResult(impact);
        } catch (err: unknown) {
          const msg = err instanceof Error ? err.message : "Decision evaluation failed.";
          actions.setError(msg);
        } finally {
          actions.setLoading(false);
        }
      });
    }

    // EN: Error dismiss button | ES: Boton de cierre de error
    const dismissBtn = this.container.querySelector<HTMLButtonElement>("#btn-dismiss-error");
    if (dismissBtn) {
      dismissBtn.addEventListener("click", () => {
        actions.clearError();
      });
    }
  }
}
