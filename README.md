# AI Ethics Interactive Simulator

EN: Enterprise-grade simulation platform for auditing computational linguistics scenarios against international AI ethics regulations (EU AI Act, IEEE 7000 and 7001 standards), built upon Clean Architecture and SOLID principles.
| ES: Plataforma de simulacion empresarial para auditar escenarios de linguistica computacional frente a regulaciones internacionales de etica de IA (Ley de IA de la UE, normas IEEE 7000 y 7001), construida sobre Arquitectura Limpia y principios SOLID.

## Architectural Overview / Descripcion Arquitectonica

```
Ethical Framework definitions/
|-- Makefile                               # Automation for install, lint, test, build
|-- backend/
|   |-- pyproject.toml                     # Poetry package management with strict Mypy and Ruff
|   |-- domain/                            # Core entities, contracts, and ethical frameworks
|   |   |-- entities.py                    # RiskTier, Scenario, EvaluationMetric, EthicalAssessment
|   |   |-- interfaces.py                  # IEthicalEvaluator, IScenarioRepository, IAssessmentRepository
|   |   |-- frameworks/
|   |       |-- eu_ai_act.py              # EU AI Act risk categorisation & parity audit
|   |       |-- ieee_standards.py         # IEEE 7000/7001 transparency and well-being audit
|   |-- application/                       # Use cases and evaluation orchestrators
|   |   |-- dtos.py                        # Pydantic schemas decoupling boundaries
|   |   |-- use_cases.py                   # EvaluateScenarioUseCase, ListScenariosUseCase
|   |   |-- evaluators/
|   |       |-- composite_evaluator.py     # Open-Closed multi-framework aggregator
|   |-- infrastructure/                    # Pluggable framework adapters
|   |   |-- main.py                        # FastAPI application entrypoint
|   |   |-- api/routes.py                  # Typed REST API endpoints
|   |   |-- repositories/                  # In-memory benchmark scenario repository
|   |-- tests/                             # Automated test suite (Pytest)
|-- frontend/
|   |-- package.json                       # Vite and TypeScript tooling
|   |-- src/
|       |-- state/store.ts                 # Reactive Observer state management (no heavy frameworks)
|       |-- services/api.ts                # Typed HTTP API client
|       |-- components/                    # Modular UI components
|       |-- styles/main.css                # Modern dark-mode styling
|-- docs/
    |-- apa_format/
        |-- architectural_decisions_whitepaper.md # APA 7th edition whitepaper
```

## Quick Start / Inicio Rapido

### Prerequisites / Requisitos
- Python 3.11+
- Poetry (version 2.0+)
- Node.js (v20+) and npm

### 1. Installation / Instalacion
```bash
make install
```
Or manually:
```bash
cd backend && poetry install
cd ../frontend && npm install
```

### 2. Linting and Static Type Checking / Linting y Tipado Estatico
```bash
make lint
```
Executes:
- `ruff check .`
- `mypy domain application infrastructure tests` (with strict static typing enforcement)

### 3. Automated Testing / Pruebas Automatizadas
```bash
make test
```
Executes full Pytest test suite covering domain entities, evaluators, use cases, and HTTP endpoints.

### 4. Running the Development Environment / Ejecucion en Entorno de Desarrollo
Terminal 1 (Backend):
```bash
make dev-backend
```
Terminal 2 (Frontend):
```bash
make dev-frontend
```

## Documentation / Documentacion
- Canonical APA 7th Whitepaper: `docs/ethical_framework_design.md`
- Spanish Edition: `docs/ethical_framework_design_ES.md`
- English Edition: `docs/ethical_framework_design_EN.md`
- Architectural Whitepaper: `docs/apa_format/architectural_decisions_whitepaper.md`
- Developer Guide (Clean Architecture): `docs/developer_guide.md`

## Author / Autoria
- **Alejandro Peña** (`alej-developer`) - [josealepm24@gmail.com](mailto:josealepm24@gmail.com)

