# Architectural Decisions and Formal Ethical Framework Evaluation for Natural Language Processing Systems: A Clean Architecture Approach

**Author**: Alejandro Peña (`alej-developer`)  
**Contact**: josealepm24@gmail.com  
**Publication Standard**: American Psychological Association (APA) 7th Edition  
**Date**: September 2026  

---

## Abstract
<!-- EN: Abstract synthesizing the architectural philosophy, ethical formalization, and engineering validation. | ES: Resumen que sintetiza la filosofia arquitectonica, la formalizacion etica y la validacion de ingenieria. -->
The increasing integration of Large Language Models (LLMs) and computational linguistics pipelines into high-stakes domains necessitates automated, auditable, and mathematically grounded ethical evaluation frameworks. This paper delineates the architectural design and theoretical formalization of the AI Ethics Interactive Simulator, an enterprise-grade evaluation platform constructed upon the tenets of Clean Architecture and SOLID object-oriented design principles. We bridge regulatory mandates from the European Union Artificial Intelligence Act (Regulation EU 2024/1689) and technical value-alignment guidelines from the Institute of Electrical and Electronics Engineers (IEEE Std 7000-2021 and IEEE Std 7001-2021). By decoupling core ethical domains from application workflows and infrastructure interfaces, our architecture achieves deterministic extensibility, strict static type safety, and verifiable compliance reporting across critical linguistic tasks, including clinical triage, dialectal toxicity moderation, and neural translation hallucination.

*Keywords*: Artificial Intelligence Ethics, Computational Linguistics, Clean Architecture, EU AI Act, IEEE 7000, Algorithmic Bias, Algorithmic Transparency.

---

## 1. Introduction and Theoretical Foundations
<!-- EN: Introduction contextualizing algorithmic harms and regulatory pressures in computational linguistics. | ES: Introduccion que contextualiza los perjuicios algoritmicos y las presiones regulatorias en linguistica computacional. -->
Natural Language Processing (NLP) systems do not operate within an axiological vacuum. As demonstrated by Blodgett et al. (2020) and Bender et al. (2021), machine-learned linguistic representations systematically reflect, amplify, and encode socioeconomic asymmetries present in training corpora. When these models are deployed in high-consequence operational spheres—such as emergency triage, asylum classification, judicial sentiment analysis, or automated content moderation—demographic disparities produce measurable allocative and dignitary harms (Crawford, 2017; Floridi et al., 2018).

Historically, software frameworks addressing algorithmic bias and safety have suffered from architectural conflation: evaluation rules, statistical metrics, database interactions, and user interface delivery mechanisms are intertwined into brittle monolithic scripts. This architectural coupling impedes regulatory adaptability when supranational standards evolve. To resolve this deficiency, this research formalizes an auditable ethical evaluation engine governed by Clean Architecture (Martin, 2017), establishing unambiguous boundaries between normative ethical invariants, orchestration use cases, and infrastructural delivery channels.

---

## 2. Architectural Formalization: Clean Architecture and SOLID Principles
<!-- EN: Formal description of architectural layers and adherence to SOLID engineering principles. | ES: Descripcion formal de las capas arquitectonicas y adhesion a los principios de ingenieria SOLID. -->

The AI Ethics Interactive Simulator is organized into concentric, decoupled rings conforming to the Dependency Inversion Principle. Dependencies point inward toward the enterprise business rules, guaranteeing that core ethical definitions remain agnostic to third-party frameworks, database drivers, or web protocols.

### 2.1 Domain Layer (`/backend/domain`)
The domain layer encapsulates enterprise business concepts, normative taxonomies, and abstract evaluation contracts:
1. **Entities & Value Objects**: `Scenario`, `LinguisticArtifact`, `EvaluationMetric`, `EthicalFinding`, and `EthicalAssessment`. These structures enforce domain invariants immutably.
2. **Evaluation Ports (`IEthicalEvaluator`)**: Defines the abstract contract through which normative frameworks inspect linguistic scenarios.
3. **Persistence Ports (`IScenarioRepository`, `IAssessmentRepository`)**: Pure abstract interfaces isolating data access mechanisms.

### 2.2 Application Layer (`/backend/application`)
The application layer coordinates the execution flow without implementing persistence details:
1. **Single Responsibility Principle (SRP)**: Distinct use cases (`EvaluateScenarioUseCase`, `ListScenariosUseCase`, `GetScenarioUseCase`) govern isolated business intentions.
2. **Open-Closed Principle (OCP)**: The `CompositeEvaluator` maintains a registry of evaluators conforming to `IEthicalEvaluator`. New regulatory frameworks (e.g., NIST AI RMF, UNESCO Recommendations) can be integrated without modifying existing evaluation orchestrators.
3. **Data Transfer Objects (DTOs)**: Enforces schema validation and boundary decoupling using strict Pydantic models, shielding domain entities from external representation changes.

### 2.3 Infrastructure Layer (`/backend/infrastructure`)
The infrastructure layer acts as a pluggable adapter containing input/output implementations:
1. **FastAPI Web Delivery**: Exposes typed RESTful endpoints (`/api/v1/scenarios`, `/api/v1/evaluations`, `/api/v1/health`) with automated OpenAPI documentation and CORS protection.
2. **In-Memory Repositories**: Implements domain repository interfaces seeded with curated, peer-reviewed computational linguistics benchmark failure modes.

### 2.4 Interface Segregation and Liskov Substitution
Evaluator implementations (`EUAIActEvaluator`, `IEEEStandardsEvaluator`) are strictly substitutable wherever `IEthicalEvaluator` is expected (Liskov Substitution Principle). Clients depend exclusively on minimal, tailored interface methods (Interface Segregation Principle).

---

## 3. Formalization of Ethical Frameworks in Computational Linguistics
<!-- EN: Mathematical and ontological translation of legal and engineering standards into executable code. | ES: Traduccion matematica y ontologica de estandares legales y de ingenieria en codigo ejecutable. -->

### 3.1 European Union Artificial Intelligence Act (Regulation EU 2024/1689)
The EU AI Act mandates a risk-based approach to artificial intelligence systems. Our engine translates legal provisions into deterministic computational linguistics rules:

1. **Risk Tier Classification (Articles 5, 6, 50)**:
   $$\text{RiskTier}(S) = \begin{cases}
   \text{UNACCEPTABLE}, & \text{if } S.\text{domain} \in \mathcal{D}_{\text{prohibited}} \\
   \text{HIGH}, & \text{if } S.\text{task} \in \mathcal{T}_{\text{AnnexIII}} \lor S.\text{domain} \in \mathcal{D}_{\text{AnnexIII}} \\
   \text{SPECIFIC\_TRANSPARENCY}, & \text{if } S.\text{task} \in \{\text{GenerativeQA}, \text{Translation}\} \\
   \text{MINIMAL}, & \text{otherwise}
   \end{cases}$$
2. **Dialectal Parity Gap (Article 10.2 - Data Governance)**:
   Given a set of linguistic artifacts $\mathcal{A}$ partitioned into dialectal varieties $\mathcal{V} = \{v_1, v_2, \dots, v_k\}$, accuracy per variety is defined as:
   $$\text{Acc}(v) = \frac{1}{|\mathcal{A}_v|} \sum_{a \in \mathcal{A}_v} \mathbf{1}(\hat{y}_a = y_a)$$
   $$\Delta_{\text{parity}} = \max_{v \in \mathcal{V}} \text{Acc}(v) - \min_{v \in \mathcal{V}} \text{Acc}(v)$$
   Compliance requires $\Delta_{\text{parity}} \le \tau_{\text{parity}}$, where $\tau_{\text{parity}} = 0.15$.
3. **Human Oversight Viability (Article 14)**:
   High-risk systems ($R = \text{HIGH}$) require verified human-in-the-loop validation flags within scenario metadata to attain compliance.

### 3.2 IEEE Standards for Autonomous and Intelligent Systems (IEEE 7000 & 7001)
1. **IEEE 7000-2021 (Ethical Value-Driven System Design)**:
   Measures stakeholder well-being protection against toxic generation:
   $$\mathcal{W}_{\text{protection}} = \max(0.0, 1.0 - \text{Rate}_{\text{toxicity}})$$
   Compliance threshold: $\mathcal{W}_{\text{protection}} \ge 0.90$.
2. **IEEE 7001-2021 (Transparency of Autonomous Systems)**:
   Synthesizes explicability indicators and confidence score visibility into a normalized transparency coefficient:
   $$\mathcal{T}_{\text{index}} = 0.60 \cdot \mathbf{1}(\text{Explainability}) + 0.40 \cdot \mathbf{1}(\text{ConfidenceVisible})$$
   Compliance threshold: $\mathcal{T}_{\text{index}} \ge 0.70$.

---

## 4. Benchmark Scenarios in Computational Linguistics
<!-- EN: Analysis of curated empirical failure modes seeded within the platform. | ES: Analisis de modos de fallo empiricos seleccionados inicializados dentro de la plataforma. -->

The engine incorporates empirical benchmark scenarios addressing known failure modes:

| Scenario Identifier | Linguistic Domain | Vulnerability Profile | Regulatory Implication |
| :--- | :--- | :--- | :--- |
| `nlp-dialect-bias-001` | Content Moderation | False-positive toxic labeling of African American Vernacular English (AAVE) vs Standard American English (SAE). | EU AI Act Art. 10; IEEE 7000 Clause 5.3. |
| `nlp-clinical-triage-002` | Emergency Intake NLP | Deprioritization of critical clinical urgency due to vernacular phrasing of acute symptoms. | EU AI Act Annex III (High Risk); IEEE 7010 Well-being. |
| `nlp-translation-toxic-003` | Diplomatic NMT | Hallucinatory insertion of derogatory language altering sovereign political communication. | EU AI Act Art. 50 (Transparency); IEEE 7000 Non-Maleficence. |

---

## 5. Verification and Quality Engineering
<!-- EN: Verification strategy detailing static typing, linting, and automated unit testing. | ES: Estrategia de verificacion que detalla tipado estatico, linting y pruebas unitarias automatizadas. -->
To ensure operational stability and scientific reproducibility, the system enforces:
- **Strict Static Typing**: Enforced via Mypy with zero untyped definitions (`disallow_untyped_defs = true`, `strict_equality = true`).
- **Deterministic Linting**: Managed by Ruff targeting Python 3.11 with adherence to PEP 8, Flake8, and isort standards.
- **Automated Verification**: Pytest suite validating domain entity immutability, evaluator edge cases, composite aggregation, and HTTP status contracts.

---

## 6. References
<!-- EN: Academic references formatted according to APA 7th Edition guidelines. | ES: Referencias academicas formateadas segun las pautas de la 7ma edicion de APA. -->

Bender, E. M., Gebru, T., McMillan-Major, A., & Shmitchell, S. (2021). On the dangers of stochastic parrots: Can language models be too big? *Proceedings of the 2021 ACM FAccT Conference*, 610–623. https://doi.org/10.1145/3442188.3445922

Blodgett, S. L., Barocas, S., Daumé, H., & Wallach, H. (2020). Language (technology) is power: A critical survey of "bias" in NLP. *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics*, 5454–5476. https://doi.org/10.18653/v1/2020.acl-main.485

Crawford, K. (2017). The trouble with bias. *Keynote Address, Conference on Neural Information Processing Systems (NeurIPS 2017)*.

European Parliament and Council of the European Union. (2024). *Regulation (EU) 2024/1689 of the European Parliament and of the Council laying down harmonised rules on artificial intelligence (Artificial Intelligence Act)*. Official Journal of the European Union, L 2024/1689.

Floridi, L., Cowls, J., Beltrametti, M., Chatila, R., Chazerand, P., Dignum, V., Luetge, C., Madelin, R., Pagallo, U., Rossi, F., Schafer, B., Valcke, P., & Vayena, E. (2018). AI4People—An ethical framework for a good AI society: Opportunities, risks, principles, and recommendations. *Minds and Machines*, 28(4), 689–707. https://doi.org/10.1007/s11023-018-9482-5

IEEE Standards Association. (2021a). *IEEE Standard Model Process for Addressing Ethical Concerns during System Design (IEEE Std 7000-2021)*. IEEE. https://doi.org/10.1109/IEEESTD.2021.9536679

IEEE Standards Association. (2021b). *IEEE Standard for Transparency of Autonomous Systems (IEEE Std 7001-2021)*. IEEE. https://doi.org/10.1109/IEEESTD.2021.9726144

Martin, R. C. (2017). *Clean architecture: A craftsman's guide to software structure and design*. Prentice Hall.
