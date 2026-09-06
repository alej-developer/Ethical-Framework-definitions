/** EN: Assessment view component displaying multi-framework audit results and metrics. | ES: Componente de vista de evaluacion que muestra resultados y metricas de auditoria de multiples marcos. */

import { appStore } from "../state/store.ts";
import { EthicalAssessment, FrameworkAssessment } from "../types/index.ts";

export class AssessmentViewComponent {
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
      this.render(state.currentAssessment, state.isLoading, state.errorMessage);
    });
  }

  private render(
    assessment: EthicalAssessment | null,
    isLoading: boolean,
    errorMessage: string | null,
  ): void {
    if (isLoading) {
      this.container.innerHTML = `
        <div class="assessment-loading-card">
          <div class="spinner"></div>
          <h3 class="loading-title">EN: Processing Algorithmic Audit | ES: Procesando Auditoria Algoritmica</h3>
          <p class="loading-desc">
            EN: Evaluating linguistic disparity coefficients and statutory compliance mandates...
            | ES: Evaluando coeficientes de disparidad linguistica y mandatos de cumplimiento estatutario...
          </p>
        </div>
      `;
      return;
    }

    if (errorMessage) {
      this.container.innerHTML = `
        <div class="alert-box error">
          <h4 class="alert-title">EN: Audit Simulation Error | ES: Error de Simulacion de Auditoria</h4>
          <p class="alert-body">${errorMessage}</p>
        </div>
      `;
      return;
    }

    if (!assessment) {
      this.container.innerHTML = `
        <div class="empty-state-card">
          <h3 class="empty-title">EN: Simulation Results Pending | ES: Resultados de Simulacion Pendientes</h3>
          <p class="empty-desc">
            EN: Select a computational linguistics scenario and execute the ethical audit to inspect statutory compliance.
            | ES: Seleccione un escenario de linguistica computacional y ejecute la auditoria etica para inspeccionar el cumplimiento legal.
          </p>
        </div>
      `;
      return;
    }

    this.container.innerHTML = `
      <div class="assessment-dashboard">
        <div class="summary-banner">
          <div class="banner-header">
            <div>
              <span class="banner-label">EN: Consolidated Assessment | ES: Evaluacion Consolidada</span>
              <h2 class="banner-title">Audit Report: ${assessment.scenario_id}</h2>
            </div>
            <div class="banner-badges">
              <span class="badge-risk tier-${assessment.overall_risk_tier.toLowerCase()}">
                ${assessment.overall_risk_tier.replace(/_/g, " ")}
              </span>
              <span class="badge-compliance status-${assessment.overall_compliance.toLowerCase()}">
                ${assessment.overall_compliance.replace(/_/g, " ")}
              </span>
            </div>
          </div>
          <p class="summary-text">${assessment.executive_summary}</p>
        </div>

        <div class="frameworks-grid">
          ${assessment.framework_assessments
            .map((fa) => this.renderFrameworkCard(fa))
            .join("")}
        </div>
      </div>
    `;
  }

  private renderFrameworkCard(fa: FrameworkAssessment): string {
    return `
      <div class="framework-card">
        <div class="framework-card-header">
          <div>
            <span class="framework-badge">${fa.framework}</span>
            <h3 class="framework-heading">${fa.framework.replace(/_/g, " ")}</h3>
          </div>
          <div class="framework-status-group">
            <span class="badge-risk-sm tier-${fa.risk_tier.toLowerCase()}">${fa.risk_tier}</span>
            <span class="badge-compliance-sm status-${fa.compliance_status.toLowerCase()}">${fa.compliance_status}</span>
          </div>
        </div>

        <div class="section-metrics">
          <h4 class="section-subtitle">EN: Evaluated Quantitative Metrics | ES: Metricas Cuantitativas Evaluadas</h4>
          <div class="metrics-grid">
            ${fa.metrics
              .map(
                (m) => `
              <div class="metric-box ${m.passed ? "metric-pass" : "metric-fail"}">
                <div class="metric-top">
                  <span class="metric-name">${m.name}</span>
                  <span class="metric-verdict">${m.passed ? "PASSED" : "FAILED"}</span>
                </div>
                <div class="metric-bar-bg">
                  <div 
                    class="metric-bar-fill ${m.passed ? "fill-pass" : "fill-fail"}" 
                    style="width: ${Math.min(100, Math.max(8, m.score * 100))}%"
                  ></div>
                </div>
                <div class="metric-values">
                  <span>Score: <strong>${m.score}</strong></span>
                  <span>Threshold: <strong>${m.threshold}</strong></span>
                </div>
                <p class="metric-explanation">${m.description}</p>
              </div>
            `
              )
              .join("")}
          </div>
        </div>

        <div class="section-findings">
          <h4 class="section-subtitle">EN: Statutory Findings & Deficiencies | ES: Hallazgos y Deficiencias Estatutarias</h4>
          ${
            fa.findings.length === 0
              ? `<p class="empty-findings">EN: Zero critical statutory defects identified. | ES: Cero defectos estatutarios criticos identificados.</p>`
              : `
            <div class="findings-list">
              ${fa.findings
                .map(
                  (f) => `
                <div class="finding-item severity-${f.severity.toLowerCase()}">
                  <div class="finding-header">
                    <span class="finding-category">${f.category}</span>
                    <span class="badge-severity sev-${f.severity.toLowerCase()}">${f.severity}</span>
                  </div>
                  <p class="finding-msg">${f.message}</p>
                  <p class="finding-rec"><strong>Remediation:</strong> ${f.recommendation}</p>
                </div>
              `
                )
                .join("")}
            </div>
          `
          }
        </div>

        <div class="section-recommendations">
          <h4 class="section-subtitle">EN: Statutory Recommendations | ES: Recomendaciones Estatutarias</h4>
          <ul class="recommendation-list">
            ${fa.recommendations.map((r) => `<li>${r}</li>`).join("")}
          </ul>
        </div>
      </div>
    `;
  }
}
