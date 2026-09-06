# Developer Guide: Clean Architecture & Modular Engineering

<!-- EN: Technical developer guide detailing Clean Architecture implementation, SOLID principles, backend layers, frontend design, and extension workflows. | ES: Guia tecnica para desarrolladores que detalla la implementacion de Arquitectura Limpia, principios SOLID, capas del backend, diseno del frontend y flujos de extension. -->

**Project**: AI Ethics Interactive Simulator  
**Author**: Alejandro Peña (`alej-developer`) - josealepm24@gmail.com  
**Architecture Paradigm**: Clean Architecture (Hexagonal / Ports & Adapters)  
**Backend Stack**: Python 3.11+, FastAPI, Pydantic V2, Poetry, Mypy, Ruff, Pytest  
**Frontend Stack**: Vanilla TypeScript, Vite, Raw CSS Variables (CSS Modules), WCAG AA  
**Publication Date**: September 2026  

---

## 1. Architectural Overview

The AI Ethics Interactive Simulator is engineered following the tenets of **Clean Architecture** (Martin, 2017). The core business logic and normative ethical definitions remain strictly decoupled from database drivers, web frameworks, and presentation interfaces.

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

### 1.1 The Dependency Inversion Principle (DIP)
All source code dependencies point strictly inward toward the domain layer:
- The **Domain Layer** has zero dependencies on third-party frameworks or external protocols.
- The **Application Layer** depends exclusively on Domain entities and abstract interfaces.
- The **Infrastructure Layer** implements the ports defined in the Domain and Application layers.

---

## 2. SOLID Engineering Principles

The codebase enforces the five SOLID principles systematically:

1. **Single Responsibility Principle (SRP)**:
   - Each use case class (e.g., `EvaluateDecisionUseCase`, `ListCaseStudiesUseCase`) orchestrates a single business action.
   - Evaluators handle distinct normative spaces: `MatrixEvaluator` computes quantitative deltas, while `EUAIActEvaluator` and `IEEEStandardsEvaluator` evaluate legal and technical standards.
2. **Open-Closed Principle (OCP)**:
   - The `CompositeEvaluator` maintains a registry of evaluators conforming to `IEthicalEvaluator`. New regulatory frameworks (e.g., NIST AI RMF, UNESCO AI Ethics) can be added without modifying existing orchestrator code.
3. **Liskov Substitution Principle (LSP)**:
   - All evaluators implementing `IEthicalEvaluator` can be substituted interchangeably without altering the correctness of the evaluation pipeline.
4. **Interface Segregation Principle (ISP)**:
   - Repository interfaces (`ICaseStudyRepository`, `IDecisionImpactRepository`, `IScenarioRepository`, `IAssessmentRepository`) define focused, cohesive method contracts rather than monolithic database interfaces.
5. **Dependency Inversion Principle (DIP)**:
   - Application use cases depend upon domain abstractions (`ICaseStudyRepository`), which are injected via FastAPI dependencies (`Annotated[..., Depends(...)]`) at runtime.

---

## 3. Directory Structure

```
.
+-- backend/
|   +-- application/
|   |   +-- dtos.py                     # Pydantic V2 input/output schemas
|   |   +-- use_cases.py                # Core orchestration use cases
|   |   +-- evaluators/
|   |       +-- composite_evaluator.py  # Poly-framework dispatch engine
|   |       +-- matrix_evaluator.py     # Multidimensional Matrix delta engine
|   +-- domain/
|   |   +-- entities.py                 # Immutable domain models & value objects
|   |   +-- interfaces.py               # Abstract repository and evaluator ports
|   |   +-- frameworks/
|   |       +-- eu_ai_act.py            # EU AI Act (Regulation EU 2024/1689) rules
|   |       +-- ieee_standards.py       # IEEE 7000 & 7001 evaluation logic
|   +-- infrastructure/
|   |   +-- api/
|   |   |   +-- routes.py               # FastAPI REST endpoints & dependency injection
|   |   +-- middleware/
|   |   |   +-- error_handler.py        # Centralized exception handling middleware
|   |   +-- repositories/
|   |   |   +-- in_memory_repository.py # In-memory storage & benchmark seed data
|   |   +-- main.py                     # FastAPI application factory
|   +-- tests/                          # Automated Pytest suite (95% coverage)
+-- frontend/
|   +-- src/
|   |   +-- components/
|   |   |   +-- case_pane.ts            # Left pane: scenario text, artifacts, baseline
|   |   |   +-- decision_pane.ts        # Right pane: decision tree, live impact cards
|   |   |   +-- header.ts               # Header with dynamic language switcher
|   |   |   +-- split_pane.ts           # Split-pane layout coordinator
|   |   +-- i18n/
|   |   |   +-- translations.ts         # Bilingual JSON dictionary (EN / ES)
|   |   +-- services/
|   |   |   +-- api.ts                  # Typed HTTP client for backend endpoints
|   |   +-- state/
|   |   |   +-- store.ts                # Custom Observer-pattern reactive state store
|   |   +-- styles/
|   |   |   +-- main.css                # Raw CSS variables, brutalist minimalism, WCAG AA
|   |   +-- types/
|   |   |   +-- index.ts                # TypeScript interfaces matching backend DTOs
|   |   +-- main.ts                     # Application bootstrap
|   +-- index.html                      # Semantic HTML5 container with skip link
|   +-- package.json
|   +-- vite.config.ts
+-- docs/
|   +-- apa_format/
|   |   +-- architectural_decisions_whitepaper.md
|   +-- ethical_framework_design.md    # Primary APA 7th academic document
|   +-- ethical_framework_design_EN.md # English APA 7th academic document
|   +-- ethical_framework_design_ES.md # Spanish APA 7th academic document
|   +-- developer_guide.md              # Technical Clean Architecture guide
+-- pyproject.toml
```

---

## 4. Backend Implementation Details

### 4.1 Domain Layer (`backend/domain`)
The domain layer encapsulates enterprise models without external library dependencies:
- **`CaseStudy`**: Represents a computational linguistics dilemma, containing narrative context, baseline ethical scores, decision options, linguistic artifacts, and regulatory mappings.
- **`DecisionOption`**: Defines an actionable intervention strategy with associated dimension score modifiers ($\mathbf{M}$) and qualitative rationale.
- **`MultidimensionalMatrix`**: Stores calculated dimension scores ($S_T, S_A, S_F$), baseline scores, deltas ($\Delta$), and the composite weighted alignment score.
- **`EthicalDimension` (Enum)**: `TRANSPARENCY`, `ACCOUNTABILITY`, `FAIRNESS`.
- **`RiskTier` (Enum)**: `UNACCEPTABLE`, `HIGH`, `SPECIFIC_TRANSPARENCY`, `MINIMAL`.

### 4.2 Application Layer (`backend/application`)
- **`MatrixEvaluator`** ([matrix_evaluator.py](file:///backend/application/evaluators/matrix_evaluator.py)):
  - Evaluates options against the case baseline:
    $$S_d = \max(0.0, \min(1.0, B_d + M_d))$$
    $$\Delta_d = S_d - B_d$$
  - Resolves dimension weightings (defaulting to $\frac{1}{3}$ each) and calculates the overall alignment index:
    $$I_{\text{align}} = \sum w_d \cdot S_d$$
  - Formulates qualitative trade-off analyses identifying strengthened, degraded, and neutral dimensions.
- **`CompositeEvaluator`** ([composite_evaluator.py](file:///backend/application/evaluators/composite_evaluator.py)):
  - Dispatches evaluation across registered framework implementations (`EUAIActEvaluator`, `IEEEStandardsEvaluator`).
- **`EvaluateDecisionUseCase`** ([use_cases.py](file:///backend/application/use_cases.py)):
  - Validates case study existence, resolves selected option, triggers `MatrixEvaluator` and `CompositeEvaluator`, persists the evaluation result, and returns a unified `DecisionImpactResponseDTO`.

### 4.3 Infrastructure Layer (`backend/infrastructure`)
- **Dependency Injection** ([routes.py](file:///backend/infrastructure/api/routes.py)):
  ```python
  @router.post("/decisions", response_model=DecisionImpactResponseDTO)
  async def submit_decision(
      request: SubmitDecisionRequestDTO,
      use_case: Annotated[EvaluateDecisionUseCase, Depends(get_evaluate_decision_use_case)],
  ) -> DecisionImpactResponseDTO:
      return use_case.execute(...)
  ```
- **Centralized Error Handling** ([error_handler.py](file:///backend/infrastructure/middleware/error_handler.py)):
  Standardizes API errors into consistent JSON envelopes:
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

## 5. Frontend Implementation Details

### 5.1 Modular Vanilla TypeScript & Zero-Framework Architecture
The frontend strictly eschews React, Vue, or component libraries. All UI components are vanilla TypeScript classes and functions manipulating standard DOM APIs.

### 5.2 Custom Reactive State Manager (`frontend/src/state/store.ts`)
State is governed by a lightweight implementation of the Observer pattern:
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

### 5.3 Interactive Split-Pane Layout
The UI is divided into two primary complementary panes:
- **Left Pane (`case_pane.ts`)**: Case study selector tabs, narrative context, dilemma callout, comparative linguistic artifacts table (e.g., AAVE vs. SAE syntactic parsing), baseline matrix scores, and regulatory implications.
- **Right Pane (`decision_pane.ts`)**: Interactive radio decision tree, rationale input area with character counter, regulatory framework toggles (EU AI Act & IEEE), submit button, and live decision impact cards (displaying score deltas, risk tiers, and trade-off synthesis).

### 5.4 Centralized Bilingual Localization (`frontend/src/i18n/translations.ts`)
The entire user interface text is dynamically swappable between English and Spanish via `getTranslation(lang, key)`. Changing the language updates the reactive state store, triggering re-render of labels without reloading the page or losing current form selections.

### 5.5 WCAG AA Accessibility Compliance
- High-contrast monochromatic color palette (contrast ratio > 7:1 against `#0A0A0A`).
- Visible focus outline (`:focus-visible` with 2px solid white and 2px offset).
- Semantic landmarks (`<header>`, `<main>`, `<section>`, `<aside>`).
- Keyboard navigation: Full tab navigation across tabs, radio options, buttons, and textareas.
- ARIA semantics: `role="radiogroup"`, `role="radio"`, `aria-checked`, `aria-live="polite"`.
- Skip link: Accessible keyboard jump link (`#main-content`).

---

## 6. Development Directives & Coding Standards

### 6.1 Bilingual Documentation Standard
All comments, docstrings, and endpoint descriptions must adhere strictly to the bilingual format:
```python
"""EN: [English descriptive text] | ES: [Texto descriptivo en espanol]"""

# EN: Calculate weighted overall score | ES: Calcular puntuacion general ponderada
```

### 6.2 Strict Zero-Emoji Policy
To maintain maximum academic and enterprise professionalism, **zero emojis** are permitted across code, comments, CSS, HTML, and documentation. Automated verification is executed via Python character range scanning:
```python
EMOJI_RANGES = [
    (0x1F600, 0x1F64F), (0x1F300, 0x1F5FF), (0x1F680, 0x1F6FF),
    (0x1F700, 0x1F77F), (0x1F780, 0x1F7FF), (0x1F800, 0x1F8FF),
    (0x1F900, 0x1F9FF), (0x1FA00, 0x1FA6F), (0x1FA70, 0x1FAFF),
    (0x2600, 0x26FF), (0x2700, 0x27BF)
]
```

### 6.3 Static Typing, Linting, and Quality Assurance
1. **Python Backend**:
   - Package Management: `poetry install`
   - Static Type Checking: `poetry run mypy domain application infrastructure tests --strict`
   - Code Linting & Formatting: `poetry run ruff check .`
   - Test Suite: `poetry run pytest --cov=domain --cov=application --cov=infrastructure -v` (Minimum 90% required; current: 95%).
2. **TypeScript Frontend**:
   - Type Checking & Build: `npm run build` (`tsc && vite build`)
   - Development Server: `npm run dev`

---

## 7. How-To Extension Guides

### 7.1 Adding a New Case Study
1. In [in_memory_repository.py](file:///backend/infrastructure/repositories/in_memory_repository.py), define the new `CaseStudy` within `_seed_case_studies()`:
   - Provide `id`, `title`, `nlp_domain`, `dilemma`, `context_description`, `task_type`, and `domain_category`.
   - Specify `baseline_matrix` containing float scores for `TRANSPARENCY`, `ACCOUNTABILITY`, and `FAIRNESS`.
   - Add three `DecisionOption` objects with dimension modifiers ($\mathbf{M}$) and operational rationales.
   - Attach sample `LinguisticArtifact` instances illustrating dialectal or sociolinguistic discrepancies.
   - Define `regulatory_implications` dictionary.
2. In [translations.ts](file:///frontend/src/i18n/translations.ts), add corresponding translations for case titles and descriptions if localized overrides are desired.

### 7.2 Adding a New Ethical Framework
1. In `backend/domain/interfaces.py`, verify compatibility with `IEthicalEvaluator`:
   ```python
   class IEthicalEvaluator(ABC):
       @abstractmethod
       def evaluate(self, scenario: Scenario) -> EthicalAssessment:
           pass
   ```
2. In `backend/domain/frameworks/`, create the new framework module (e.g., `nist_ai_rmf.py`).
3. Implement evaluation logic adhering to the framework's statutory or technical criteria.
4. In `backend/application/evaluators/composite_evaluator.py`, register the new evaluator within the composite registry.
5. In `frontend/src/types/index.ts` and `frontend/src/components/decision_pane.ts`, add the framework toggle to the user interface.

---

## 8. Verification & Deployment

```bash
# Backend Verification
poetry run ruff check .
poetry run mypy domain application infrastructure tests
poetry run pytest -v

# Frontend Verification
cd frontend
npm run build

# Run Locally
poetry run uvicorn infrastructure.main:app --host 127.0.0.1 --port 8000 &
cd frontend && npm run dev -- --host 127.0.0.1 --port 5173
```
