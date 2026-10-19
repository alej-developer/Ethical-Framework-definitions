# AI Ethics Interactive Simulator

EN: Enterprise-grade simulation platform for auditing computational linguistics scenarios against international AI ethics regulations (EU AI Act, IEEE 7000 and 7001 standards), built upon Clean Architecture and SOLID principles. | ES: Plataforma de simulación empresarial para auditar escenarios de lingüística computacional frente a regulaciones internacionales de ética de IA (Ley de IA de la UE, normas IEEE 7000 y 7001), construida sobre Arquitectura Limpia y principios SOLID.

## Architectural Overview / Descripción Arquitectónica

```
Ethical Framework definitions/
|-- Makefile                               # Automation for install, lint, test, build
|-- backend/
|   |-- pyproject.toml                     # Poetry package management with strict Mypy and Ruff
|   |-- domain/                            # Core entities, contracts, and ethical frameworks
|   |   |-- entities.py                    # RiskTier, Scenario, EvaluationMetric, EthicalAssessment
|   |   |-- interfaces.py                  # IEthicalEvaluator, IScenarioRepository, IAssessmentRepository
|   |   |-- frameworks/
|   |       |-- eu_ai_act.py              # EU AI Act risk categorization & parity audit
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

## Quick Start / Inicio Rápido

### Prerequisites / Requisitos
- Python 3.11+
- Poetry (version 2.0+)
- Node.js (v20+) and npm

### 1. Installation / Instalación
```bash
make install
```
Or manually / O manualmente:
```bash
cd backend && poetry install
cd ../frontend && npm install
```

### 2. Linting and Static Type Checking / Linting y Tipado Estático
```bash
make lint
```
Executes / Ejecuta:
- `ruff check .`
- `mypy domain application infrastructure tests` (with strict static typing enforcement / con aplicación estricta del tipado estático)

### 3. Automated Testing / Pruebas Automatizadas
```bash
make test
```
Executes full Pytest test suite covering domain entities, evaluators, use cases, and HTTP endpoints. / Ejecuta la suite completa de pruebas Pytest que cubre entidades de dominio, evaluadores, casos de uso y endpoints HTTP.

### 4. Running the Development Environment / Ejecución en Entorno de Desarrollo
Terminal 1 (Backend) / Terminal 1 (backend):
```bash
make dev-backend
```
Terminal 2 (Frontend) / Terminal 2 (frontend):
```bash
make dev-frontend
```

## Documentation / Documentación
- Canonical APA 7th Whitepaper / Libro blanco canónico APA 7.ª edición: `docs/ethical_framework_design.md`
- Spanish Edition / Edición en español: `docs/ethical_framework_design_ES.md`
- English Edition / Edición en inglés: `docs/ethical_framework_design_EN.md`
- Architectural Whitepaper / Libro blanco arquitectónico: `docs/apa_format/architectural_decisions_whitepaper.md`
- Developer Guide (Clean Architecture) / Guía para desarrolladores (Arquitectura Limpia): `docs/developer_guide.md`

## Author / Autoría
- **Alejandro Peña** ([alej-developer](https://github.com/alej-developer))
