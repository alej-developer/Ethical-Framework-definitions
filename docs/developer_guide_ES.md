# Guía para desarrolladores: Arquitectura Limpia e ingeniería modular

<!-- EN: Technical developer guide detailing Clean Architecture implementation, SOLID principles, backend layers, frontend design, and extension workflows. | ES: Guía técnica para desarrolladores que detalla la implementación de Arquitectura Limpia, principios SOLID, capas del backend, diseño del frontend y flujos de extensión. -->

**Proyecto**: AI Ethics Interactive Simulator  
**Autor**: Alejandro Peña ([alej-developer](https://github.com/alej-developer))  
**Paradigma de arquitectura**: Arquitectura Limpia (hexagonal / puertos y adaptadores)  
**Pila del backend**: Python 3.11+, FastAPI, Pydantic V2, Poetry, Mypy, Ruff, Pytest  
**Pila del frontend**: TypeScript puro, Vite, variables CSS en bruto (módulos CSS), WCAG AA  
**Fecha de publicación**: septiembre de 2026  

> **English edition / Edición en inglés**: [developer_guide.md](./developer_guide.md)

---

## 1. Visión general de la arquitectura

El Simulador Interactivo de Ética en IA está construido según los principios de la **Arquitectura Limpia** (Martin, 2017). La lógica de negocio central y las definiciones éticas normativas permanecen estrictamente desacopladas de los controladores de bases de datos, los frameworks web y las interfaces de presentación.

```
+-------------------------------------------------------------------------+
|                           Clean Architecture                            |
|                                                                         |
|   +-----------------------------------------------------------------+   |
|   |                   Infrastructure Layer                          |   |
|   |   - FastAPI Routes & Dependency Injection                       |   |
|   |   - In-Memory / SQL Repositories                                |   |
|   |   - Centralized Error Handling Middleware                       |   |
|   |   - Vite Frontend Delivery                                      |   |
|   |                                                                 |   |
|   |   +---------------------------------------------------------+   |   |
|   |   |               Application Layer                         |   |   |
|   |   |   - Use Cases (Evaluate, List, Get)                     |   |   |
|   |   |   - Multidimensional Matrix Evaluator                   |   |   |
|   |   |   - Composite Evaluator (Poly-framework dispatch)       |   |   |
|   |   |   - Pydantic V2 DTOs & Validation Schemas               |   |   |
|   |   |                                                         |   |   |
|   |   |   +-------------------------------------------------+   |   |   |
|   |   |   |               Domain Layer                      |   |   |   |
|   |   |   |   - Pure Entities (CaseStudy, DecisionOption)   |   |   |   |
|   |   |   |   - Value Objects (EthicalDimension, RiskTier)  |   |   |   |
|   |   |   |   - Repository Ports (ICaseStudyRepository)     |   |   |   |
|   |   |   |   - Evaluator Ports (IEthicalEvaluator)         |   |   |   |
|   |   |   +-------------------------------------------------+   |   |   |
|   |   +---------------------------------------------------------+   |   |
|   +-----------------------------------------------------------------+   |
+-------------------------------------------------------------------------+
```

### 1.1 El principio de inversión de dependencias (DIP)

Todas las dependencias del código fuente apuntan estrictamente hacia el interior, en dirección a la capa de dominio:

- La **capa de dominio** no tiene dependencias de frameworks de terceros ni de protocolos externos.
- La **capa de aplicación** depende exclusivamente de las entidades de dominio y de las interfaces abstractas.
- La **capa de infraestructura** implementa los puertos definidos en las capas de dominio y de aplicación.

---

## 2. Principios de ingeniería SOLID

El código aplica de forma sistemática los cinco principios SOLID:

1. **Principio de responsabilidad única (SRP)**:
   - Cada clase de caso de uso (p. ej., `EvaluateDecisionUseCase`, `ListCaseStudiesUseCase`) orquesta una sola acción de negocio.
   - Los evaluadores atienden espacios normativos distintos: `MatrixEvaluator` calcula los deltas cuantitativos, mientras que `EUAIActEvaluator` e `IEEEStandardsEvaluator` evalúan las normas legales y técnicas.
2. **Principio abierto-cerrado (OCP)**:
   - El `CompositeEvaluator` mantiene un registro de evaluadores conformes a `IEthicalEvaluator`. Pueden añadirse nuevos marcos regulatorios (p. ej., NIST AI RMF, ética de la IA de la UNESCO) sin modificar el código del orquestador existente.
3. **Principio de sustitución de Liskov (LSP)**:
   - Todos los evaluadores que implementan `IEthicalEvaluator` pueden sustituirse entre sí sin alterar la corrección del canal de evaluación.
4. **Principio de segregación de interfaces (ISP)**:
   - Las interfaces de repositorio (`ICaseStudyRepository`, `IDecisionImpactRepository`, `IScenarioRepository`, `IAssessmentRepository`) definen contratos de métodos acotados y cohesivos, en lugar de interfaces monolíticas de base de datos.
5. **Principio de inversión de dependencias (DIP)**:
   - Los casos de uso de la aplicación dependen de abstracciones del dominio (`ICaseStudyRepository`), que se inyectan en tiempo de ejecución mediante dependencias de FastAPI (`Annotated[..., Depends(...)]`).

---

## 3. Estructura de directorios

```
.
+-- backend/
|   +-- application/
|   |   +-- dtos.py                     # Esquemas de entrada y salida de Pydantic V2
|   |   +-- use_cases.py                # Casos de uso de la orquestación central
|   |   +-- evaluators/
|   |       +-- composite_evaluator.py  # Motor de despacho entre varios marcos
|   |       +-- matrix_evaluator.py     # Motor de deltas de la matriz multidimensional
|   +-- domain/
|   |   +-- entities.py                 # Modelos de dominio inmutables y objetos de valor
|   |   +-- interfaces.py               # Puertos abstractos de repositorio y de evaluador
|   |   +-- frameworks/
|   |       +-- eu_ai_act.py            # Reglas de la Ley de IA de la UE (Reglamento UE 2024/1689)
|   |       +-- ieee_standards.py       # Lógica de evaluación IEEE 7000 y 7001
|   +-- infrastructure/
|   |   +-- api/
|   |   |   +-- routes.py               # Endpoints REST de FastAPI e inyección de dependencias
|   |   +-- middleware/
|   |   |   +-- error_handler.py        # Middleware centralizado de manejo de excepciones
|   |   +-- repositories/
|   |   |   +-- in_memory_repository.py # Almacenamiento en memoria y datos semilla de referencia
|   |   +-- main.py                     # Fábrica de la aplicación FastAPI
|   +-- tests/                          # Suite automatizada de Pytest (cobertura del 95%)
+-- frontend/
|   +-- src/
|   |   +-- components/
|   |   |   +-- case_pane.ts            # Panel izquierdo: texto del escenario, artefactos y línea base
|   |   |   +-- decision_pane.ts        # Panel derecho: árbol de decisiones y tarjetas de impacto en vivo
|   |   |   +-- header.ts               # Encabezado con selector dinámico de idioma
|   |   |   +-- split_pane.ts           # Coordinador del diseño de panel dividido
|   |   +-- i18n/
|   |   |   +-- translations.ts         # Diccionario bilingüe (EN / ES)
|   |   +-- services/
|   |   |   +-- api.ts                  # Cliente HTTP tipado para los endpoints del backend
|   |   +-- state/
|   |   |   +-- store.ts                # Almacén de estado reactivo con el patrón Observer
|   |   +-- styles/
|   |   |   +-- main.css                # Variables CSS en bruto, minimalismo brutalista, WCAG AA
|   |   +-- types/
|   |   |   +-- index.ts                # Interfaces de TypeScript alineadas con los DTO del backend
|   |   +-- main.ts                     # Arranque de la aplicación
|   +-- index.html                      # Contenedor HTML5 semántico con enlace de salto
|   +-- package.json
|   +-- vite.config.ts
+-- docs/
|   +-- apa_format/
|   |   +-- architectural_decisions_whitepaper.md
|   |   +-- architectural_decisions_whitepaper_ES.md # Edición en español del libro blanco
|   +-- ethical_framework_design.md    # Documento académico principal, APA 7.ª edición
|   +-- ethical_framework_design_EN.md # Documento académico en inglés, APA 7.ª edición
|   +-- ethical_framework_design_ES.md # Documento académico en español, APA 7.ª edición
|   +-- developer_guide.md              # Guía técnica de Arquitectura Limpia
|   +-- developer_guide_ES.md           # Edición en español de esta guía
+-- pyproject.toml
```

---

## 4. Detalles de implementación del backend

### 4.1 Capa de dominio (`backend/domain`)

La capa de dominio encapsula los modelos de la organización sin dependencias de bibliotecas externas:

- **`CaseStudy`**: representa un dilema de lingüística computacional y contiene el contexto narrativo, las puntuaciones éticas de línea base, las opciones de decisión, los artefactos lingüísticos y los mapeos regulatorios.
- **`DecisionOption`**: define una estrategia de intervención accionable, con los modificadores de puntuación por dimensión asociados ($\mathbf{M}$) y una justificación cualitativa.
- **`MultidimensionalMatrix`**: almacena las puntuaciones calculadas por dimensión ($S_T, S_A, S_F$), las puntuaciones de línea base, los deltas ($\Delta$) y la puntuación compuesta de alineación ponderada.
- **`EthicalDimension` (enumeración)**: `TRANSPARENCY`, `ACCOUNTABILITY`, `FAIRNESS`.
- **`RiskTier` (enumeración)**: `UNACCEPTABLE`, `HIGH`, `SPECIFIC_TRANSPARENCY`, `MINIMAL`.

### 4.2 Capa de aplicación (`backend/application`)

- **`MatrixEvaluator`** ([matrix_evaluator.py](../backend/application/evaluators/matrix_evaluator.py)):
  - Evalúa las opciones frente a la línea base del caso:
    $$S_d = \max(0.0, \min(1.0, B_d + M_d))$$
    $$\Delta_d = S_d - B_d$$
  - Resuelve las ponderaciones por dimensión (por defecto, $\frac{1}{3}$ cada una) y calcula el índice global de alineación:
    $$I_{\text{align}} = \sum w_d \cdot S_d$$
  - Formula análisis cualitativos de compensaciones que identifican las dimensiones reforzadas, degradadas y neutras.
- **`CompositeEvaluator`** ([composite_evaluator.py](../backend/application/evaluators/composite_evaluator.py)):
  - Distribuye la evaluación entre las implementaciones de marcos registradas (`EUAIActEvaluator`, `IEEEStandardsEvaluator`).
- **`EvaluateDecisionUseCase`** ([use_cases.py](../backend/application/use_cases.py)):
  - Comprueba que el caso de estudio existe, resuelve la opción seleccionada, invoca `MatrixEvaluator` y `CompositeEvaluator`, persiste el resultado de la evaluación y devuelve un `DecisionImpactResponseDTO` unificado.

### 4.3 Capa de infraestructura (`backend/infrastructure`)

- **Inyección de dependencias** ([routes.py](../backend/infrastructure/api/routes.py)):
  ```python
  @router.post("/decisions", response_model=DecisionImpactResponseDTO)
  async def submit_decision(
      request: SubmitDecisionRequestDTO,
      use_case: Annotated[EvaluateDecisionUseCase, Depends(get_evaluate_decision_use_case)],
  ) -> DecisionImpactResponseDTO:
      return use_case.execute(...)
  ```
- **Manejo centralizado de errores** ([error_handler.py](../backend/infrastructure/middleware/error_handler.py)):
  Normaliza los errores de la API en sobres JSON coherentes:
  ```json
  {
    "error": {
      "code": "CASE_STUDY_NOT_FOUND",
      "message": "Case study with id 'xyz' was not found.",
      "status_code": 404,
      "details": { "case_id": "xyz" },
      "timestamp": "2026-09-06T11:03:00.000000Z"
    }
  }
  ```

---

## 5. Detalles de implementación del frontend

### 5.1 TypeScript modular puro y arquitectura sin frameworks

El frontend prescinde de forma estricta de React, Vue y de bibliotecas de componentes. Todos los componentes de la interfaz son clases y funciones de TypeScript puro que manipulan las API estándar del DOM.

### 5.2 Gestor de estado reactivo propio (`frontend/src/state/store.ts`)

El estado se rige por una implementación ligera del patrón Observer:

```typescript
export class Store<T> {
  private state: T;
  private listeners: Set<(state: T) => void> = new Set();

  constructor(initialState: T) {
    this.state = initialState;
  }

  public getState(): T {
    return this.state;
  }

  public setState(partial: Partial<T>): void {
    this.state = { ...this.state, ...partial };
    this.notify();
  }

  public subscribe(listener: (state: T) => void): () => void {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  private notify(): void {
    this.listeners.forEach((listener) => listener(this.state));
  }
}
```

### 5.3 Diseño interactivo de panel dividido

La interfaz se divide en dos paneles principales y complementarios:

- **Panel izquierdo (`case_pane.ts`)**: pestañas de selección del caso de estudio, contexto narrativo, llamada de atención del dilema, tabla comparativa de artefactos lingüísticos (p. ej., análisis sintáctico de AAVE frente a SAE), puntuaciones de la matriz de línea base e implicaciones regulatorias.
- **Panel derecho (`decision_pane.ts`)**: árbol de decisión con botones de opción, área de justificación con contador de caracteres, conmutadores de marcos regulatorios (Ley de IA de la UE e IEEE), botón de envío y tarjetas de impacto de la decisión en vivo (muestran deltas de puntuación, niveles de riesgo y síntesis de compensaciones).

### 5.4 Localización bilingüe centralizada (`frontend/src/i18n/translations.ts`)

Todo el texto de la interfaz de usuario puede intercambiarse de forma dinámica entre inglés y español mediante `getTranslation(lang, key)`. Cambiar el idioma actualiza el almacén de estado reactivo y vuelve a dibujar las etiquetas sin recargar la página ni perder las selecciones actuales del formulario.

### 5.5 Cumplimiento de accesibilidad WCAG AA

- Paleta monocromática de alto contraste (relación de contraste superior a 7:1 frente a `#0A0A0A`).
- Contorno de foco visible (`:focus-visible` con 2 px en blanco sólido y 2 px de desplazamiento).
- Regiones semánticas (`<header>`, `<main>`, `<section>`, `<aside>`).
- Navegación por teclado: tabulación completa entre pestañas, opciones de radio, botones y áreas de texto.
- Semántica ARIA: `role="radiogroup"`, `role="radio"`, `aria-checked`, `aria-live="polite"`.
- Enlace de salto: enlace de teclado accesible hacia el contenido principal (`#main-content`).

---

## 6. Directrices de desarrollo y normas de codificación

### 6.1 Norma de documentación bilingüe

Todos los comentarios, las docstrings y las descripciones de endpoints deben ajustarse de forma estricta al formato bilingüe:

```python
"""EN: [English descriptive text] | ES: [Texto descriptivo en español]"""

# EN: Calculate weighted overall score | ES: Calcular puntuación general ponderada
```

### 6.2 Política estricta de cero emojis

Para mantener el máximo profesionalismo académico y empresarial, se permiten **cero emojis** en el código, los comentarios, CSS, HTML y la documentación. La verificación automatizada se ejecuta mediante un barrido de rangos de caracteres en Python:

```python
EMOJI_RANGES = [
    (0x1F600, 0x1F64F), (0x1F300, 0x1F5FF), (0x1F680, 0x1F6FF),
    (0x1F700, 0x1F77F), (0x1F780, 0x1F7FF), (0x1F800, 0x1F8FF),
    (0x1F900, 0x1F9FF), (0x1FA00, 0x1FA6F), (0x1FA70, 0x1FAFF),
    (0x2600, 0x26FF), (0x2700, 0x27BF)
]
```

### 6.3 Tipado estático, linting y aseguramiento de la calidad

1. **Backend en Python**:
   - Gestión de paquetes: `poetry install`
   - Comprobación estática de tipos: `poetry run mypy domain application infrastructure tests --strict`
   - Linting y formato: `poetry run ruff check .`
   - Suite de pruebas: `poetry run pytest --cov=domain --cov=application --cov=infrastructure -v` (mínimo exigido: 90%; valor actual: 95%).
2. **Frontend en TypeScript**:
   - Comprobación de tipos y compilación: `npm run build` (`tsc && vite build`)
   - Servidor de desarrollo: `npm run dev`

---

## 7. Guías prácticas de extensión

### 7.1 Añadir un caso de estudio nuevo

1. En [in_memory_repository.py](../backend/infrastructure/repositories/in_memory_repository.py), definir el nuevo `CaseStudy` dentro de `_seed_case_studies()`:
   - Aportar `id`, `title`, `nlp_domain`, `dilemma`, `context_description`, `task_type` y `domain_category`.
   - Especificar `baseline_matrix` con puntuaciones de coma flotante para `TRANSPARENCY`, `ACCOUNTABILITY` y `FAIRNESS`.
   - Añadir tres objetos `DecisionOption` con modificadores de dimensión ($\mathbf{M}$) y justificaciones operativas.
   - Adjuntar instancias de ejemplo de `LinguisticArtifact` que ilustren discrepancias dialectales o sociolingüísticas.
   - Definir el diccionario `regulatory_implications`.
2. En [translations.ts](../frontend/src/i18n/translations.ts), añadir las traducciones correspondientes de los títulos y las descripciones de los casos si se desean sustituciones localizadas.

### 7.2 Añadir un marco ético nuevo

1. En `backend/domain/interfaces.py`, comprobar la compatibilidad con `IEthicalEvaluator`:
   ```python
   class IEthicalEvaluator(ABC):
       @abstractmethod
       def evaluate(self, scenario: Scenario) -> EthicalAssessment:
           pass
   ```
2. En `backend/domain/frameworks/`, crear el módulo del marco nuevo (p. ej., `nist_ai_rmf.py`).
3. Implementar la lógica de evaluación de acuerdo con los criterios legales o técnicos del marco.
4. En `backend/application/evaluators/composite_evaluator.py`, registrar el evaluador nuevo en el registro compuesto.
5. En `frontend/src/types/index.ts` y `frontend/src/components/decision_pane.ts`, añadir el conmutador del marco a la interfaz de usuario.

---

## 8. Verificación y despliegue

```bash
# Verificación del backend
poetry run ruff check .
poetry run mypy domain application infrastructure tests
poetry run pytest -v

# Verificación del frontend
cd frontend
npm run build

# Ejecución local
poetry run uvicorn infrastructure.main:app --host 127.0.0.1 --port 8000 &
cd frontend && npm run dev -- --host 127.0.0.1 --port 5173
```
