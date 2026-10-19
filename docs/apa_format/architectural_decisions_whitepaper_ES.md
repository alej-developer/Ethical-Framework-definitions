# Decisiones Arquitectónicas y Evaluación Formal de Marcos Éticos para Sistemas de Procesamiento del Lenguaje Natural: Un Enfoque de Arquitectura Limpia

**Autor**: Alejandro Peña ([alej-developer](https://github.com/alej-developer))  
**Normativa de publicación**: American Psychological Association (APA), 7.ª edición  
**Fecha**: septiembre de 2026  

> **English edition / Edición en inglés**: [architectural_decisions_whitepaper.md](./architectural_decisions_whitepaper.md)

---

## Resumen

<!-- EN: Abstract synthesizing the architectural philosophy, ethical formalization, and engineering validation. | ES: Resumen que sintetiza la filosofía arquitectónica, la formalización ética y la validación de ingeniería. -->

La creciente integración de los Modelos de Lenguaje de Gran Escala (LLM) y de los canales de lingüística computacional en dominios de alto riesgo exige marcos de evaluación ética automatizados, auditables y con fundamento matemático. Este artículo describe el diseño arquitectónico y la formalización teórica del Simulador Interactivo de Ética en IA, una plataforma de evaluación de nivel empresarial construida según los principios de la Arquitectura Limpia y del diseño orientado a objetos SOLID. Articulamos los mandatos regulatorios de la Ley de Inteligencia Artificial de la Unión Europea (Reglamento UE 2024/1689) y las directrices técnicas de alineación de valores del Instituto de Ingenieros Eléctricos y Electrónicos (IEEE Std 7000-2021 e IEEE Std 7001-2021). Al desacoplar los dominios éticos nucleares de los flujos de aplicación y de las interfaces de infraestructura, la arquitectura alcanza extensibilidad determinista, seguridad estricta de tipos estáticos e informes de cumplimiento verificables en tareas lingüísticas críticas, entre ellas el triaje clínico, la moderación de toxicidad dialectal y la alucinación en traducción neuronal.

*Palabras clave*: ética de la inteligencia artificial, lingüística computacional, Arquitectura Limpia, Ley de IA de la UE, IEEE 7000, sesgo algorítmico, transparencia algorítmica.

---

## 1. Introducción y fundamentos teóricos

<!-- EN: Introduction contextualizing algorithmic harms and regulatory pressures in computational linguistics. | ES: Introducción que contextualiza los perjuicios algorítmicos y las presiones regulatorias en lingüística computacional. -->

Los sistemas de Procesamiento del Lenguaje Natural (PLN) no operan en un vacío axiológico. Como demostraron Blodgett et al. (2020) y Bender et al. (2021), las representaciones lingüísticas aprendidas por máquina reflejan, amplifican y codifican de forma sistemática las asimetrías socioeconómicas presentes en los corpus de entrenamiento. Cuando estos modelos se despliegan en ámbitos operativos de alta consecuencia —como el triaje de urgencias, la clasificación de solicitudes de asilo, el análisis de sentimiento judicial o la moderación automatizada de contenido—, las disparidades demográficas producen perjuicios distributivos y contra la dignidad que resultan medibles (Crawford, 2017; Floridi et al., 2018).

Históricamente, los marcos de software dedicados al sesgo algorítmico y a la seguridad han adolecido de una confusión arquitectónica: las reglas de evaluación, las métricas estadísticas, las interacciones con la base de datos y los mecanismos de entrega de la interfaz de usuario quedan entrelazados en scripts monolíticos y frágiles. Ese acoplamiento arquitectónico impide la adaptación regulatoria cuando evolucionan las normas supranacionales. Para resolver esta deficiencia, esta investigación formaliza un motor de evaluación ética auditable regido por la Arquitectura Limpia (Martin, 2017) y establece límites inequívocos entre los invariantes éticos normativos, los casos de uso de orquestación y los canales de entrega de la infraestructura.

---

## 2. Formalización arquitectónica: Arquitectura Limpia y principios SOLID

<!-- EN: Formal description of architectural layers and adherence to SOLID engineering principles. | ES: Descripción formal de las capas arquitectónicas y adhesión a los principios de ingeniería SOLID. -->

El Simulador Interactivo de Ética en IA se organiza en anillos concéntricos y desacoplados, conformes al principio de inversión de dependencias. Las dependencias apuntan hacia el interior, en dirección a las reglas de negocio de la organización, de modo que las definiciones éticas nucleares permanecen ajenas a frameworks de terceros, controladores de bases de datos o protocolos web.

### 2.1 Capa de dominio (`/backend/domain`)

La capa de dominio encapsula los conceptos de negocio de la organización, las taxonomías normativas y los contratos abstractos de evaluación:

1. **Entidades y objetos de valor**: `Scenario`, `LinguisticArtifact`, `EvaluationMetric`, `EthicalFinding` y `EthicalAssessment`. Estas estructuras imponen de forma inmutable los invariantes del dominio.
2. **Puertos de evaluación (`IEthicalEvaluator`)**: define el contrato abstracto mediante el cual los marcos normativos inspeccionan los escenarios lingüísticos.
3. **Puertos de persistencia (`IScenarioRepository`, `IAssessmentRepository`)**: interfaces puramente abstractas que aíslan los mecanismos de acceso a datos.

### 2.2 Capa de aplicación (`/backend/application`)

La capa de aplicación coordina el flujo de ejecución sin implementar los detalles de persistencia:

1. **Principio de responsabilidad única (SRP)**: casos de uso distintos (`EvaluateScenarioUseCase`, `ListScenariosUseCase`, `GetScenarioUseCase`) gobiernan intenciones de negocio aisladas.
2. **Principio abierto-cerrado (OCP)**: el `CompositeEvaluator` mantiene un registro de evaluadores conformes a `IEthicalEvaluator`. Pueden integrarse nuevos marcos regulatorios (p. ej., NIST AI RMF, recomendaciones de la UNESCO) sin modificar los orquestadores de evaluación existentes.
3. **Objetos de transferencia de datos (DTO)**: imponen la validación de esquemas y el desacoplamiento de fronteras mediante modelos estrictos de Pydantic, y protegen a las entidades de dominio frente a los cambios de representación externa.

### 2.3 Capa de infraestructura (`/backend/infrastructure`)

La capa de infraestructura actúa como adaptador intercambiable y contiene las implementaciones de entrada y salida:

1. **Entrega web con FastAPI**: expone endpoints REST tipados (`/api/v1/scenarios`, `/api/v1/evaluations`, `/api/v1/health`) con documentación OpenAPI automatizada y protección CORS.
2. **Repositorios en memoria**: implementan las interfaces de repositorio del dominio, inicializadas con modos de fallo de referencia de lingüística computacional, seleccionados y revisados por pares.

### 2.4 Segregación de interfaces y sustitución de Liskov

Las implementaciones de los evaluadores (`EUAIActEvaluator`, `IEEEStandardsEvaluator`) son estrictamente sustituibles allí donde se espera `IEthicalEvaluator` (principio de sustitución de Liskov). Los clientes dependen exclusivamente de métodos de interfaz mínimos y ajustados a su necesidad (principio de segregación de interfaces).

---

## 3. Formalización de los marcos éticos en lingüística computacional

<!-- EN: Mathematical and ontological translation of legal and engineering standards into executable code. | ES: Traducción matemática y ontológica de estándares legales y de ingeniería en código ejecutable. -->

### 3.1 Ley de Inteligencia Artificial de la Unión Europea (Reglamento UE 2024/1689)

La Ley de IA de la UE impone un enfoque basado en el riesgo para los sistemas de inteligencia artificial. El motor traduce las disposiciones legales en reglas deterministas de lingüística computacional:

1. **Clasificación del nivel de riesgo (artículos 5, 6 y 50)**:
   $$\text{RiskTier}(S) = \begin{cases}
   \text{UNACCEPTABLE}, & \text{if } S.\text{domain} \in \mathcal{D}_{\text{prohibited}} \\
   \text{HIGH}, & \text{if } S.\text{task} \in \mathcal{T}_{\text{AnnexIII}} \lor S.\text{domain} \in \mathcal{D}_{\text{AnnexIII}} \\
   \text{SPECIFIC\_TRANSPARENCY}, & \text{if } S.\text{task} \in \{\text{GenerativeQA}, \text{Translation}\} \\
   \text{MINIMAL}, & \text{otherwise}
   \end{cases}$$
2. **Brecha de paridad dialectal (artículo 10.2, gobernanza de datos)**:
   Dado un conjunto de artefactos lingüísticos $\mathcal{A}$ particionado en variedades dialectales $\mathcal{V} = \{v_1, v_2, \dots, v_k\}$, la exactitud por variedad se define como:
   $$\text{Acc}(v) = \frac{1}{|\mathcal{A}_v|} \sum_{a \in \mathcal{A}_v} \mathbf{1}(\hat{y}_a = y_a)$$
   $$\Delta_{\text{parity}} = \max_{v \in \mathcal{V}} \text{Acc}(v) - \min_{v \in \mathcal{V}} \text{Acc}(v)$$
   El cumplimiento exige $\Delta_{\text{parity}} \le \tau_{\text{parity}}$, donde $\tau_{\text{parity}} = 0.15$.
3. **Viabilidad de la supervisión humana (artículo 14)**:
   Los sistemas de alto riesgo ($R = \text{HIGH}$) requieren indicadores verificados de validación con humano en el ciclo, dentro de los metadatos del escenario, para alcanzar el cumplimiento.

### 3.2 Normas IEEE para sistemas autónomos e inteligentes (IEEE 7000 y 7001)

1. **IEEE 7000-2021 (diseño de sistemas orientado por valores éticos)**:
   Mide la protección del bienestar de las partes interesadas frente a la generación tóxica:
   $$\mathcal{W}_{\text{protection}} = \max(0.0, 1.0 - \text{Rate}_{\text{toxicity}})$$
   Umbral de cumplimiento: $\mathcal{W}_{\text{protection}} \ge 0.90$.
2. **IEEE 7001-2021 (transparencia de los sistemas autónomos)**:
   Sintetiza los indicadores de explicabilidad y la visibilidad de la puntuación de confianza en un coeficiente normalizado de transparencia:
   $$\mathcal{T}_{\text{index}} = 0.60 \cdot \mathbf{1}(\text{Explainability}) + 0.40 \cdot \mathbf{1}(\text{ConfidenceVisible})$$
   Umbral de cumplimiento: $\mathcal{T}_{\text{index}} \ge 0.70$.

---

## 4. Escenarios de referencia en lingüística computacional

<!-- EN: Analysis of curated empirical failure modes seeded within the platform. | ES: Análisis de modos de fallo empíricos seleccionados e inicializados dentro de la plataforma. -->

El motor incorpora escenarios empíricos de referencia que abordan modos de fallo conocidos:

| Identificador del escenario | Dominio lingüístico | Perfil de vulnerabilidad | Implicación regulatoria |
| :--- | :--- | :--- | :--- |
| `nlp-dialect-bias-001` | Moderación de contenido | Etiquetado tóxico con falsos positivos del inglés vernáculo afroamericano (AAVE) frente al inglés estadounidense estándar (SAE). | Ley de IA de la UE, art. 10; IEEE 7000, cláusula 5.3. |
| `nlp-clinical-triage-002` | PLN de admisión de urgencias | Despriorización de la urgencia clínica crítica debido a la formulación vernácula de síntomas agudos. | Ley de IA de la UE, anexo III (alto riesgo); IEEE 7010, bienestar. |
| `nlp-translation-toxic-003` | Traducción automática neuronal diplomática | Inserción alucinatoria de lenguaje derogatorio que altera una comunicación política soberana. | Ley de IA de la UE, art. 50 (transparencia); IEEE 7000, no maleficencia. |

---

## 5. Verificación e ingeniería de la calidad

<!-- EN: Verification strategy detailing static typing, linting, and automated unit testing. | ES: Estrategia de verificación que detalla el tipado estático, el linting y las pruebas unitarias automatizadas. -->

Para garantizar la estabilidad operativa y la reproducibilidad científica, el sistema impone lo siguiente:

- **Tipado estático estricto**: aplicado mediante Mypy, sin definiciones sin tipo (`disallow_untyped_defs = true`, `strict_equality = true`).
- **Linting determinista**: gestionado por Ruff, con objetivo Python 3.11 y adhesión a las normas PEP 8, Flake8 e isort.
- **Verificación automatizada**: suite de Pytest que valida la inmutabilidad de las entidades de dominio, los casos límite de los evaluadores, la agregación compuesta y los contratos de estado HTTP.

---

## 6. Referencias

<!-- EN: Academic references formatted according to APA 7th Edition guidelines. | ES: Referencias académicas formateadas según las pautas de la 7.ª edición de APA. -->

Bender, E. M., Gebru, T., McMillan-Major, A., & Shmitchell, S. (2021). On the dangers of stochastic parrots: Can language models be too big? *Proceedings of the 2021 ACM FAccT Conference*, 610–623. https://doi.org/10.1145/3442188.3445922

Blodgett, S. L., Barocas, S., Daumé, H., & Wallach, H. (2020). Language (technology) is power: A critical survey of "bias" in NLP. *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics*, 5454–5476. https://doi.org/10.18653/v1/2020.acl-main.485

Crawford, K. (2017). The trouble with bias. *Keynote Address, Conference on Neural Information Processing Systems (NeurIPS 2017)*.

European Parliament and Council of the European Union. (2024). *Regulation (EU) 2024/1689 of the European Parliament and of the Council laying down harmonised rules on artificial intelligence (Artificial Intelligence Act)*. Official Journal of the European Union, L 2024/1689.

Floridi, L., Cowls, J., Beltrametti, M., Chatila, R., Chazerand, P., Dignum, V., Luetge, C., Madelin, R., Pagallo, U., Rossi, F., Schafer, B., Valcke, P., & Vayena, E. (2018). AI4People—An ethical framework for a good AI society: Opportunities, risks, principles, and recommendations. *Minds and Machines*, 28(4), 689–707. https://doi.org/10.1007/s11023-018-9482-5

IEEE Standards Association. (2021a). *IEEE Standard Model Process for Addressing Ethical Concerns during System Design (IEEE Std 7000-2021)*. IEEE. https://doi.org/10.1109/IEEESTD.2021.9536679

IEEE Standards Association. (2021b). *IEEE Standard for Transparency of Autonomous Systems (IEEE Std 7001-2021)*. IEEE. https://doi.org/10.1109/IEEESTD.2021.9726144

Martin, R. C. (2017). *Clean architecture: A craftsman's guide to software structure and design*. Prentice Hall.
