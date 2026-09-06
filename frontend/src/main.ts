/** EN: Frontend entrypoint initialising components and bootstrapping state. | ES: Punto de entrada del frontend que inicializa componentes y arranca el estado. */

import { AssessmentViewComponent } from "./components/assessment_view.ts";
import { FrameworkSelectorComponent } from "./components/framework_selector.ts";
import { ScenarioSelectorComponent } from "./components/scenario_selector.ts";
import { ApiService } from "./services/api.ts";
import { actions } from "./state/store.ts";

document.addEventListener("DOMContentLoaded", async () => {
  // EN: Instantiate presentation components bound to DOM roots | ES: Instanciar componentes de presentacion vinculados a raices del DOM
  new ScenarioSelectorComponent("scenario-selector-root");
  new FrameworkSelectorComponent("framework-selector-root");
  new AssessmentViewComponent("assessment-view-root");

  // EN: Bootstrap data from backend REST API | ES: Arrancar datos desde la API REST del backend
  try {
    actions.setLoading(true);
    const scenarios = await ApiService.fetchScenarios();
    actions.setScenarios(scenarios);
  } catch (err: unknown) {
    const errorMsg =
      err instanceof Error
        ? err.message
        : "Failed to connect to AI Ethics Simulator backend.";
    actions.setError(
      `Connection error: ${errorMsg}. Please ensure the backend service is running on port 8000.`
    );
  } finally {
    actions.setLoading(false);
  }
});
