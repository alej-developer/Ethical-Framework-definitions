# AI Ethics Interactive Simulator - Backend Service

EN: Backend service designed according to Clean Architecture and SOLID principles for evaluating computational linguistics scenarios against international AI ethics frameworks. | ES: Servicio de backend disenado segun Arquitectura Limpia y principios SOLID para evaluar escenarios de linguistica computacional frente a marcos internacionales de etica de IA.

## Architectural Layers / Capas Arquitectonicas

- **domain**: EN: Core business entities, value objects, and evaluation contracts. | ES: Entidades de negocio centrales, objetos de valor y contratos de evaluacion.
- **application**: EN: Use cases and composite ethical evaluation logic. | ES: Casos de uso y logica de evaluacion etica compuesta.
- **infrastructure**: EN: FastAPI web server, in-memory repository adapters, and external integrations. | ES: Servidor web FastAPI, adaptadores de repositorio en memoria e integraciones externas.
- **tests**: EN: Automated unit, use case, and API integration test suites. | ES: Suites de pruebas automatizadas unitarias, de casos de uso y de integracion de API.
