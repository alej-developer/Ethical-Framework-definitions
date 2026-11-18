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
    // EN: Subscribe to language and loading changes for dynamic header rendering | ES: Suscribirse a cambios de idioma y carga para renderizado dinamico de cabecera
    appStore.subscribeSelector(
      (state) => ({ language: state.language, isLoading: state.isLoading }),
      ({ language, isLoading }) => {
        this.render(language, isLoading);
      },
    );
  }

  private render(language: Language, isLoading = false): void {
    document.documentElement.lang = language;
    const skipLink = document.querySelector<HTMLAnchorElement>(".skip-link");
    if (skipLink) {
      skipLink.textContent = getTranslation("skipToContent", language);
    }

    const title = getTranslation("appTitle", language);
    const subtitle = getTranslation("appSubtitle", language);
    const badge = getTranslation("architectureBadge", language);
    const loadingLabel = getTranslation("loadingStatusText", language);
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
            ${
              isLoading
                ? `<span class="loading-status-badge" role="status" aria-live="polite">${loadingLabel}</span>`
                : ""
            }
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
