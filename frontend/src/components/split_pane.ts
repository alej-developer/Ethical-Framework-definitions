/** EN: Split-pane container component orchestrating Left (Case Study) and Right (Decision & Metrics) panes. | ES: Componente contenedor de panel dividido que orquesta los paneles Izquierdo (Caso de Estudio) y Derecho (Decision y Metricas). */

import { CasePaneComponent } from "./case_pane.ts";
import { DecisionPaneComponent } from "./decision_pane.ts";

export class SplitPaneComponent {
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
    // EN: Create semantic split-pane layout containers | ES: Crear contenedores de diseno semanticos para el panel dividido
    this.container.innerHTML = `
      <div class="split-layout" role="main">
        <div id="left-case-pane-root"></div>
        <div id="right-decision-pane-root"></div>
      </div>
    `;

    // EN: Initialize sub-components inside their respective pane roots | ES: Inicializar subcomponentes dentro de sus respectivas raices de panel
    new CasePaneComponent("left-case-pane-root");
    new DecisionPaneComponent("right-decision-pane-root");
  }
}
