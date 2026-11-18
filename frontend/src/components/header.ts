/** EN: Minimalist header component with dynamic language switcher and architecture status badge. | ES: Componente de cabecera minimalista con selector de idioma dinamico y distintivo de estado de arquitectura. */

import { getTranslation } from "../i18n/translations.ts";
import { actions, appStore } from "../state/store.ts";
import { Language } from "../types/index.ts";

export class HeaderComponent {
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
    // EN: Subscribe to state changes for dynamic language rendering | ES: Suscribirse a cambios de estado para renderizado dinamico del idioma
    appStore.subscribe((state) => {
      this.render(state.language);
    });
  }

  private render(language: Language): void {
    const title = getTranslation("appTitle", language);
    const subtitle = getTranslation("appSubtitle", language);
    const badge = getTranslation("architectureBadge", language);
    const toggleTarget: Language = language === "en" ? "es" : "en";
    const toggleLabel = language === "en" ? "ESPAÑOL" : "ENGLISH";

    this.container.innerHTML = `
      <header class="app-header" role="banner">
        <div class="header-container">
          <div class="brand-block">
            <h1 class="brand-heading">${title}</h1>
            <p class="brand-desc">${subtitle}</p>
          </div>
          <div class="header-actions">
            <span class="system-status" aria-label="Architecture Status">${badge}</span>
            <button 
              type="button" 
              id="btn-toggle-lang" 
              class="btn-lang-toggle" 
              aria-label="Switch Language to ${toggleLabel}"
            >
              ${toggleLabel}
            </button>
          </div>
        </div>
      </header>
    `;

    // EN: Attach event listener for language toggling | ES: Adjuntar escuchador de eventos para alternancia de idioma
    const toggleBtn = this.container.querySelector<HTMLButtonElement>("#btn-toggle-lang");
    if (toggleBtn) {
      toggleBtn.addEventListener("click", () => {
        actions.setLanguage(toggleTarget);
      });
    }
  }
}
