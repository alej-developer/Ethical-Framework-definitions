/** EN: Frontend entrypoint initialising components and bootstrapping state. | ES: Punto de entrada del frontend que inicializa componentes y arranca el estado. */

import { HeaderComponent } from "./components/header.ts";
import { SplitPaneComponent } from "./components/split_pane.ts";
import { actions } from "./state/store.ts";

document.addEventListener("DOMContentLoaded", async () => {
  // EN: Instantiate presentation components bound to DOM roots | ES: Instanciar componentes de presentacion vinculados a raices del DOM
  new HeaderComponent("header-root");
  new SplitPaneComponent("split-pane-root");

  // EN: Bootstrap data from backend REST API | ES: Arrancar datos desde la API REST del backend
  await actions.loadInitialCases();
});
