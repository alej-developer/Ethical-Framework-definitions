/** EN: Right split pane component rendering interactive decision tree, rationale input, and real-time EU AI Act / matrix compliance metrics. | ES: Componente del panel derecho que renderiza el arbol de decision interactivo, entrada de justificacion y metricas de cumplimiento en tiempo real. */

import { getTranslation, Translations } from "../i18n/translations.ts";
import { actions, appStore } from "../state/store.ts";
import {
  BindingLevel,
  CaseStudy,
  DecisionImpactResponse,
  FrameworkInfo,
  FrameworkRegion,
  Language,
} from "../types/index.ts";
import { escapeHtml } from "../utils/escape_html.ts";

// EN: Display order and label keys for regions and binding levels | ES: Orden de visualizacion y claves de etiqueta para regiones y niveles de vinculacion
const REGION_ORDER: FrameworkRegion[] = ["EUROPE", "AMERICAS", "ASIA_PACIFIC", "AFRICA", "INTERNATIONAL"];
const REGION_LABEL: Record<FrameworkRegion, keyof Translations> = {
  EUROPE: "regionEurope",
  AMERICAS: "regionAmericas",
  ASIA_PACIFIC: "regionAsiaPacific",
  AFRICA: "regionAfrica",
  INTERNATIONAL: "regionInternational",
};
const BINDING_LABEL: Record<BindingLevel, keyof Translations> = {
  LEGALLY_BINDING: "bindingLegallyBinding",
  VOLUNTARY_STANDARD: "bindingVoluntaryStandard",
  PROPOSED_LEGISLATION: "bindingProposedLegislation",
};

interface DecisionPaneSlice {
  currentCase: CaseStudy | null;
  selectedOptionId: string | null;
  userRationale: string;
  selectedFrameworks: string[];
  availableFrameworks: FrameworkInfo[];
  latestImpact: DecisionImpactResponse | null;
  isLoading: boolean;
  errorMessage: string | null;
  language: Language;
}

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
    appStore.subscribeSelector<DecisionPaneSlice>(
      (state) => ({
        currentCase: state.currentCase,
        selectedOptionId: state.selectedOptionId,
        userRationale: state.userRationale,
        selectedFrameworks: state.selectedFrameworks,
        availableFrameworks: state.availableFrameworks,
        latestImpact: state.latestImpact,
        isLoading: state.isLoading,
        errorMessage: state.errorMessage,
        language: state.language,
      }),
      (slice, prevSlice) => {
        // EN: Surgical DOM update when only userRationale changes so textarea preserves focus and caret | ES: Actualizacion quirurgica del DOM cuando solo cambia userRationale para que el textarea conserve foco y cursor
        if (
          prevSlice &&
          prevSlice.currentCase === slice.currentCase &&
          prevSlice.selectedOptionId === slice.selectedOptionId &&
          prevSlice.selectedFrameworks === slice.selectedFrameworks &&
          prevSlice.availableFrameworks === slice.availableFrameworks &&
          prevSlice.latestImpact === slice.latestImpact &&
          prevSlice.isLoading === slice.isLoading &&
          prevSlice.errorMessage === slice.errorMessage &&
          prevSlice.language === slice.language &&
          prevSlice.userRationale !== slice.userRationale
        ) {
          this.updateRationaleDom(slice);
          return;
        }

        this.render(
          slice.currentCase,
          slice.selectedOptionId,
          slice.userRationale,
          slice.selectedFrameworks,
          slice.availableFrameworks,
          slice.latestImpact,
          slice.isLoading,
          slice.errorMessage,
          slice.language,
        );
      },
    );
  }

  private updateRationaleDom(slice: DecisionPaneSlice): void {
    const textarea = this.container.querySelector<HTMLTextAreaElement>("#input-user-rationale");
    if (textarea && textarea.value !== slice.userRationale) {
      textarea.value = slice.userRationale;
    }

    const charCounter = this.container.querySelector<HTMLElement>("#rationale-char-count");
    if (charCounter) {
      charCounter.textContent = `${slice.userRationale.trim().length} ${getTranslation("charsLabel", slice.language)}`;
    }

    const isRationaleValid = slice.userRationale.trim().length >= 10;
    const canSubmit = Boolean(slice.currentCase && slice.selectedOptionId && isRationaleValid && !slice.isLoading);
    const submitBtn = this.container.querySelector<HTMLButtonElement>("#btn-execute-eval");
    if (submitBtn) {
      submitBtn.disabled = !canSubmit;
    }
  }

  private render(
    currentCase: CaseStudy | null,
    selectedOptionId: string | null,
    rationale: string,
    frameworks: string[],
    availableFrameworks: FrameworkInfo[],
    impact: DecisionImpactResponse | null,
    isLoading: boolean,
    errorMessage: string | null,
    lang: Language,
  ): void {
    const isRationaleValid = rationale.trim().length >= 10;
    const canSubmit = Boolean(currentCase && selectedOptionId && isRationaleValid && !isLoading);

    this.container.innerHTML = `
      <div class="pane ${isLoading ? "is-loading" : ""}" role="region" aria-labelledby="right-pane-heading" aria-busy="${isLoading ? "true" : "false"}">
        <div class="pane-header">
          <h2 id="right-pane-heading" class="pane-title">${getTranslation("decisionTreeHeading", lang)}</h2>
          <p class="pane-subtitle">${getTranslation("decisionTreeDesc", lang)}</p>
        </div>

        <div class="pane-content">
          ${
            errorMessage
              ? `
            <div class="alert-error" role="alert" aria-live="assertive">
              <span><strong>${getTranslation("errorTitle", lang)}:</strong> ${escapeHtml(errorMessage)}</span>
              <button type="button" id="btn-dismiss-error" class="btn-lang-toggle" ${isLoading ? "disabled" : ""}>${getTranslation("retryButtonText", lang)}</button>
            </div>
          `
              : ""
          }

          ${
            !currentCase
              ? `
            <div class="empty-state">
              <p class="empty-state-title">${getTranslation("emptyStateTitle", lang)}</p>
              <p class="empty-state-text">${getTranslation("selectCaseForDecisionsText", lang)}</p>
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
                    for="radio-${escapeHtml(opt.id)}"
                  >
                    <input 
                      type="radio" 
                      id="radio-${escapeHtml(opt.id)}" 
                      name="decision-option" 
                      class="decision-radio" 
                      value="${escapeHtml(opt.id)}"
                      ${opt.id === selectedOptionId ? "checked" : ""}
                      aria-checked="${opt.id === selectedOptionId ? "true" : "false"}"
                    />
                    <div class="option-body">
                      <span class="option-strategy-chip">${escapeHtml(opt.strategy)}</span>
                      <strong class="option-title">${escapeHtml(opt.title)}</strong>
                      <p class="option-desc">${escapeHtml(opt.description)}</p>
                      
                      <div class="modifier-chips-row" aria-label="Estimated Impact Modifiers">
                        ${Object.entries(opt.dimension_modifiers)
                          .map(([dim, val]) => {
                            const sign = val > 0 ? "+" : "";
                            const cls = val > 0 ? "positive" : val < 0 ? "negative" : "neutral";
                            return `<span class="modifier-chip ${cls}">${escapeHtml(dim)}: ${sign}${val.toFixed(2)}</span>`;
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
                placeholder="${escapeHtml(getTranslation("rationalePlaceholder", lang))}"
                aria-label="${escapeHtml(getTranslation("rationaleHeading", lang))}"
                aria-describedby="rationale-hint"
              >${escapeHtml(rationale)}</textarea>
              <div id="rationale-hint" class="form-hint">
                <span>${getTranslation("rationaleMinCharsNote", lang)}</span>
                <span id="rationale-char-count" class="tabular-num">${rationale.trim().length} ${getTranslation("charsLabel", lang)}</span>
              </div>
            </div>

            <!-- EN: Target Frameworks Selector | ES: Selector de Marcos Objetivo -->
            <div class="section-block">
              <span class="section-label">${getTranslation("frameworksHeading", lang)}</span>
              ${this.renderFrameworkSelector(availableFrameworks, frameworks, lang)}
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
                    lang,
                  )}
                  ${this.renderDimensionCard(
                    getTranslation("dimensionAccountability", lang),
                    impact.matrix.accountability.baseline_score,
                    impact.matrix.accountability.decision_score,
                    impact.matrix.accountability.delta,
                    lang,
                  )}
                  ${this.renderDimensionCard(
                    getTranslation("dimensionFairness", lang),
                    impact.matrix.fairness.baseline_score,
                    impact.matrix.fairness.decision_score,
                    impact.matrix.fairness.delta,
                    lang,
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
                    <p>${escapeHtml(impact.trade_off_analysis)}</p>
                  </div>
                </div>

                <!-- EN: Statutory Remediation Directives | ES: Directivas Estatutarias de Subsanacion -->
                <div class="section-block">
                  <span class="section-label">${getTranslation("recommendationsHeading", lang)}</span>
                  <ul class="recs-list">
                    ${impact.recommendations.map((rec) => `<li>${escapeHtml(rec)}</li>`).join("")}
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

    this.attachEventListeners();
  }

  private renderFrameworkSelector(available: FrameworkInfo[], selected: string[], lang: Language): string {
    // EN: Group catalogue entries by region in a fixed order | ES: Agrupar entradas del catalogo por region en orden fijo
    return REGION_ORDER.map((region) => {
      const group = available.filter((f) => f.region === region);
      if (group.length === 0) return "";
      const items = group
        .map(
          (f) => `
          <label class="reg-item framework-option" for="cb-framework-${escapeHtml(f.id)}">
            <input type="checkbox" id="cb-framework-${escapeHtml(f.id)}" class="cb-framework" value="${escapeHtml(f.id)}" ${selected.includes(f.id) ? "checked" : ""} />
            <div class="framework-option-body">
              <div class="framework-option-title-row">
                <strong>${escapeHtml(f.name)}</strong>
                <span class="meta-chip binding-chip binding-${escapeHtml(f.binding_level.toLowerCase())}">${getTranslation(BINDING_LABEL[f.binding_level], lang)}</span>
              </div>
              <span class="framework-option-desc">${escapeHtml(f.jurisdiction)} &middot; ${f.focus_areas.map((area) => escapeHtml(area)).join(" &middot; ")}</span>
            </div>
          </label>`,
        )
        .join("");
      return `
        <fieldset class="framework-region-group">
          <legend class="framework-region-legend">${getTranslation(REGION_LABEL[region], lang)}</legend>
          <div class="regulatory-list">${items}</div>
        </fieldset>`;
    }).join("");
  }

  private renderDimensionCard(name: string, baseline: number, current: number, delta: number, lang: Language): string {
    const sign = delta > 0 ? "+" : "";
    const deltaClass = delta > 0 ? "positive" : delta < 0 ? "negative" : "neutral";

    return `
      <div class="impact-card">
        <div class="impact-card-top">
          <span class="impact-dim">${escapeHtml(name)}</span>
          <span class="delta-pill ${deltaClass}">${sign}${delta.toFixed(2)}</span>
        </div>
        <div class="impact-score-row">
          <span class="impact-score-current tabular-num">${current.toFixed(2)}</span>
          <span class="impact-score-prev tabular-num">${getTranslation("wasLabel", lang)} ${baseline.toFixed(2)}</span>
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

  private attachEventListeners(): void {
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

    // EN: Submit button listener reading live state from store | ES: Escuchador de boton de envio leyendo estado vivo desde el store
    const submitBtn = this.container.querySelector<HTMLButtonElement>("#btn-execute-eval");
    if (submitBtn) {
      submitBtn.addEventListener("click", async () => {
        const { currentCase, selectedOptionId, userRationale, selectedFrameworks } = appStore.getState();
        if (currentCase && selectedOptionId && userRationale.trim().length >= 10) {
          await actions.submitDecisionEvaluation(
            currentCase.id,
            selectedOptionId,
            userRationale,
            selectedFrameworks,
          );
        }
      });
    }

    // EN: Error retry button | ES: Boton de reintento ante error
    const retryBtn = this.container.querySelector<HTMLButtonElement>("#btn-dismiss-error");
    if (retryBtn) {
      retryBtn.addEventListener("click", async () => {
        await actions.retryLastOperation();
      });
    }
  }
}
