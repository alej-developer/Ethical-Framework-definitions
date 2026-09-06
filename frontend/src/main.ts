/** EN: Frontend entrypoint initialising components and bootstrapping state. | ES: Punto de entrada del frontend que inicializa componentes y arranca el estado. */

import { HeaderComponent } from "./components/header.ts";
import { SplitPaneComponent } from "./components/split_pane.ts";
import { ApiService } from "./services/api.ts";
import { actions } from "./state/store.ts";

document.addEventListener("DOMContentLoaded", async () => {
  // EN: Instantiate presentation components bound to DOM roots | ES: Instanciar componentes de presentacion vinculados a raices del DOM
  new HeaderComponent("header-root");
  new SplitPaneComponent("split-pane-root");

  // EN: Bootstrap data from backend REST API | ES: Arrancar datos desde la API REST del backend
  try {
    actions.setLoading(true);
    const caseSummaries = await ApiService.fetchCaseStudies();
    actions.setCaseList(caseSummaries);

    if (caseSummaries.length > 0) {
      const initialCase = await ApiService.fetchCaseStudy(caseSummaries[0].id);
      actions.setCurrentCase(initialCase);
    }
  } catch (err: unknown) {
    const errorMsg =
      err instanceof Error
        ? err.message
        : "Failed to connect to AI Ethics Simulator backend.";
    actions.setError(
      `Connection error: ${errorMsg}. Please ensure the FastAPI backend service is running on port 8000.`
    );
  } finally {
    actions.setLoading(false);
  }
});
