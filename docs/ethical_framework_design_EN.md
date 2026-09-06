# Pedagogical Framework and Computational Linguistics Evaluation Metrics for Interactive AI Ethics Simulation: A Multidimensional Decision-Modeling Approach

**Author**: Alejandro Peña (`alej-developer`)  
**Contact**: josealepm24@gmail.com  
**Project**: AI Ethics Interactive Simulator  
**Publication Standard**: American Psychological Association (APA) 7th Edition  
**Date**: September 2026  

---

## Abstract

<!-- EN: Structured academic abstract delineating the research problem, pedagogical methodology, computational metrics, and simulation results. | ES: Resumen academico estructurado que delinea el problema de investigacion, la metodologia pedagogica, las metricas computacionales y los resultados de la simulacion. -->

The rapid integration of Large Language Models (LLMs) and automated text processing pipelines into high-stakes institutional domains has exposed critical deficiencies in conventional AI ethics pedagogy. Traditional pedagogical modalities rely predominantly on abstract normative theory or post-hoc post-mortem analyses, failing to cultivate operational decision-making competencies under competing engineering and ethical constraints. This paper presents the pedagogical architecture and computational linguistics metrics underlying the AI Ethics Interactive Simulator, an open-source educational and evaluation platform engineered under Clean Architecture and SOLID design principles. Grounded in Kolb's Experiential Learning Cycle and Case-Based Reasoning, the simulator immerses learners in realistic computational linguistics dilemmas: dialectal bias in automated recruitment parsing (African American Vernacular English vs. Standard American English), stylistic profiling in forensic authorship attribution, and pre-training dataset provenance gaps. We formalize a Multidimensional Ethical Matrix that dynamically quantifies decisions across Transparency ($S_T$), Accountability ($S_A$), and Fairness ($S_F$) within bounded limits $[0.0, 1.0]$, calculating score deltas ($\Delta$) and composite alignment against the European Union Artificial Intelligence Act (Regulation EU 2024/1689) and IEEE Standards 7000-2021 and 7001-2021. By requiring learners to actively balance processing velocity against systemic discrimination, the simulator fosters reflective equilibrium, dismantles naive techno-solutionism, and bridges the pedagogical gap between regulatory compliance and production Natural Language Processing (NLP) engineering.

*Keywords*: AI ethics pedagogy, computational linguistics, experiential learning, algorithmic bias, EU AI Act, IEEE 7000, Clean Architecture, sociotechnical systems.

---

## 1. Introduction

<!-- EN: Introduction contextualizing sociotechnical vulnerabilities in NLP and the imperative for experiential ethical education. | ES: Introduccion que contextualiza las vulnerabilidades sociotecnicas en NLP y la necesidad de una educacion etica experiencial. -->

Natural Language Processing (NLP) technologies have transitioned from academic experimentation to systemic deployment across societally consequential infrastructures, including employment screening, judicial risk scoring, medical triage, and foundational information retrieval (Bender et al., 2021; Bommasani et al., 2021). However, machine learning algorithms trained on human-generated text corpora do not merely ingest semantic structures; they reproduce, encode, and amplify historic sociolinguistic hierarchies and structural inequities (Blodgett et al., 2020; Crawford, 2017). When computational pipelines process vernacular language varieties, non-standard dialects, or sociodemographic proxies, marginalized populations experience disproportionate allocative and representational harms (Barocas et al., 2023; Buolamwini & Gebru, 2018).

Concurrently, international governance bodies have enacted stringent regulatory frameworks to govern high-risk algorithmic systems. Most notably, the European Union Artificial Intelligence Act (Regulation EU 2024/1689) imposes strict legal obligations regarding data governance (Article 10), technical documentation (Article 11), record-keeping (Article 12), transparency (Article 13), and human oversight (Article 14) for high-risk AI deployments listed under Annex III, including employment screening and law enforcement tools. Similarly, the Institute of Electrical and Electronics Engineers has established formal methodologies for addressing ethical concerns during system conception (IEEE Std 7000-2021) and measuring autonomous system transparency (IEEE Std 7001-2021).

Despite these robust standards, computer science and computational linguistics curricula exhibit a persistent pedagogical disconnect (Saltz et al., 2019; Fiesler et al., 2020). Traditional ethical education in engineering disciplines often suffers from three structural pathologies:
1. **Abstract Decontextualization**: Ethics is taught through high-level moral philosophy (e.g., deontology, utilitarianism, virtue ethics) without practical integration into technical artifacts, codebases, or loss functions.
2. **Post-Hoc Disconnect**: Ethics is presented as an afterthought or an external compliance checklist rather than an intrinsic engineering trade-off negotiated throughout the development lifecycle.
3. **Passive Didacticism**: Students analyze static case studies where the "correct" answer is transparent, shielding them from the genuine cognitive dissonance and commercial pressures inherent in real-world machine learning deployment.

To resolve these deficiencies, this paper formalizes the pedagogical methodology and mathematical evaluation metrics of the AI Ethics Interactive Simulator. By situating learners in the role of lead NLP architects confronted with multifaceted algorithmic dilemmas, the simulator transforms ethical reasoning from a passive academic exercise into a dynamic, quantifiable, and experiential decision-making process.

---

## 2. Pedagogical Methodology

<!-- EN: Detailed theoretical formulation of the simulator's pedagogical architecture and learning theory alignment. | ES: Formulacion teorica detallada de la arquitectura pedagogica del simulador y alineacion con la teoria del aprendizaje. -->

The pedagogical foundation of the AI Ethics Interactive Simulator is synthesized from adult learning theory, cognitive dissonance theory, and scenario-based decision modeling.

```
+-------------------------------------------------------------------+
|               Kolb's Experiential Learning Cycle                  |
|                                                                   |
|   1. Concrete Experience (CE)                                     |
|      - Review linguistic artifacts & empirical baseline matrix    |
|      - Experience operational pressure (velocity vs. safety)      |
|                           |                                       |
|                           v                                       |
|   2. Reflective Observation (RO)                                  |
|      - Inspect dialectal error disparities (AAVE vs. SAE)         |
|      - Analyze regulatory non-compliance exposure                 |
|                           |                                       |
|                           v                                       |
|   3. Abstract Conceptualization (AC)                              |
|      - Formulate trade-off hypotheses                             |
|      - Reconcile EU AI Act & IEEE 7000 normative constraints      |
|                           |                                       |
|                           v                                       |
|   4. Active Experimentation (AE)                                  |
|      - Select mitigation strategy & submit written rationale      |
|      - Evaluate multidimensional delta shifts and risk tier       |
+-------------------------------------------------------------------+
```

### 2.1 Experiential Learning Cycle and Constructive Alignment

The simulator implements Kolb's (1984) Experiential Learning Cycle across four continuous phases:
1. **Concrete Experience (CE)**: The learner is presented with an authentic industrial NLP deployment scenario containing concrete text artifacts, baseline performance data, and competing organizational objectives (e.g., reducing candidate processing backlog vs. preventing disparate impact).
2. **Reflective Observation (RO)**: The learner reviews qualitative and quantitative discrepancies in model behavior, such as differences in classification confidence between Standard American English (SAE) and African American Vernacular English (AAVE), observing the human consequences of algorithmic failure.
3. **Abstract Conceptualization (AC)**: The learner evaluates competing ethical theories and regulatory mandates (e.g., EU AI Act Annex III vs. Title VII vs. IEEE 7000), conceptualizing how engineering decisions affect systemic transparency, accountability, and fairness.
4. **Active Experimentation (AE)**: The learner selects an intervention pathway, writes an evidence-based justification, and submits the decision to the evaluation engine, immediately observing the recalculated ethical deltas and regulatory risk posture.

This structure satisfies Biggs' (1996) principle of *constructive alignment*, ensuring that learning objectives, student activities, and assessment mechanisms are intrinsically integrated.

### 2.2 Pedagogical Provocation and Cognitive Dissonance

A central premise of moral psychology is that moral development occurs when individuals encounter cognitive dissonance—situations where existing cognitive schema cannot resolve competing ethical obligations (Festinger, 1957; Kohlberg, 1984). The simulator systematically rejects "trivially correct" or "cost-free" options. Every available intervention enforces tangible trade-offs:
- **Throughput Maximization (Status Quo)** yields maximal processing velocity and business throughput, but severely degrades fairness ($S_F$) and creates catastrophic legal exposure under EU AI Act Article 5 and Annex III.
- **Surface Heuristic Redaction (Regex/Entity Masking)** offers moderate engineering speed and minimal pipeline disruption, but leaves deep latent semantic representations unaddressed, illustrating the fallacy of superficial fairness.
- **Comprehensive Value-Aligned Oversight (Counterfactual Fine-Tuning and Dual Review)** achieves high ethical alignment across all dimensions, but imposes substantial inference latency, ongoing operational expenditure, and human reviewer overhead.

By exposing learners to these tensions, the simulator dismantles naive techno-solutionism (Green, 2020), forcing engineering students to recognize that algorithm design is an inherently political and moral act.

---

## 3. Computational Linguistics Metrics in Empirical Case Studies

<!-- EN: Mathematical formalization of linguistic phenomena, bias metrics, and error rates across the three curated case studies. | ES: Formalizacion matematica de fenomenos linguisticos, metricas de sesgo y tasas de error en los tres casos de estudio. -->

The simulator incorporates three complex NLP case studies reflecting urgent contemporary dilemmas in applied computational linguistics.

### 3.1 Case Study 1: LLM Demographic Bias in Automated Recruitment Parsing (`cs-recruitment-llm-001`)

#### 3.1.1 Problem Formulation and Linguistic Mechanics
In automated resume information extraction, zero-shot Large Language Models are frequently deployed to parse unstructured curriculum vitae into structured competency vectors and rank candidate suitability. However, pre-trained transformer embeddings capture sociolinguistic patterns where African American Vernacular English (AAVE) syntax—such as habitual *be* ("They be having zero downtime") or copula absence—is embedded proximal to lower qualification clusters compared to isomorphic Standard American English (SAE) phrasing ("Ensured continuous zero downtime") (Blodgett & O'Connor, 2017; Harris et al., 2022). Furthermore, mentions of historically marginalized affinity groups (e.g., "Society of Women Engineers") trigger latent downgrading.

#### 3.1.2 Quantitative Formulation
Let $\mathcal{D} = \{(x_i, y_i, d_i)\}_{i=1}^N$ represent a resume dataset, where $x_i \in \mathcal{X}$ is the textual resume, $y_i \in \{0, 1\}$ denotes true candidate qualification ($1 = \text{Qualified}$), and $d_i \in \{v_{\text{AAVE}}, v_{\text{SAE}}\}$ denotes the dialectal variety. The classifier outputs a qualification probability $\hat{p}_i = f_\theta(x_i)$ and binary decision $\hat{y}_i = \mathbf{1}(\hat{p}_i \ge \tau)$.

1. **Disparate Impact Ratio ($DI$)**:
   Governed by the EEOC Uniform Guidelines four-fifths rule and EU AI Act Article 10:
   $$DI = \frac{P(\hat{Y} = 1 \mid D = v_{\text{AAVE}})}{P(\hat{Y} = 1 \mid D = v_{\text{SAE}})}$$
   An unmitigated baseline deployment produces $DI = 0.58$, severely violating the statutory threshold of $DI \ge 0.80$.

2. **False Negative Disparity ($\Delta_{\text{FNR}}$)**:
   Measures the difference in error rates where qualified candidates are incorrectly rejected:
   $$\text{FNR}(v) = P(\hat{Y} = 0 \mid Y = 1, D = v)$$
   $$\Delta_{\text{FNR}} = \text{FNR}(v_{\text{AAVE}}) - \text{FNR}(v_{\text{SAE}})$$
   In baseline testing, $\Delta_{\text{FNR}} = 0.24$, reflecting systematic dialectal penalization.

3. **Semantic Embedding Cosine Distance**:
   For semantically identical resume segments $x_{\text{AAVE}}$ and $x_{\text{SAE}}$:
   $$\text{Dist}_{\text{cosine}}(e(x_{\text{AAVE}}), e(x_{\text{SAE}})) = 1 - \frac{e(x_{\text{AAVE}}) \cdot e(x_{\text{SAE}})}{\|e(x_{\text{AAVE}})\| \|e(x_{\text{SAE}})\|}$$
   Where $e(\cdot)$ is the encoder representation. In uncalibrated models, distance exceeds 0.38, demonstrating semantic drift driven exclusively by dialectal syntax.

---

### 3.2 Case Study 2: Stylistic Profiling in Forensic Linguistics (`cs-forensic-stylometry-002`)

#### 3.2.1 Problem Formulation and Linguistic Mechanics
Forensic authorship attribution utilizes computational stylometry—analyzing function word frequencies, syntactic n-grams, and hapax legomena—to determine the probability that an anonymous text originated from a specific suspect (Chaski, 2005; Juola, 2008). When applied to multilingual speakers, code-switching individuals, or regional English varieties (e.g., Nigerian English, Indian English), stylometric classifiers exhibit severe error asymmetry. Idiosyncratic feature distributions are misattributed to target suspects with artificially inflated confidence, risking false arrest warrants and violating the European Convention on Human Rights (Article 6 - Right to a Fair Trial).

#### 3.2.2 Quantitative Formulation
Let $\mathcal{S} = \{s_1, s_2, \dots, s_K\}$ represent the candidate suspect pool, and let $q$ denote the questioned anonymous communiqué.

1. **Authorship Posterior Probability and Cross-Entropy Calibration**:
   $$P(\text{Author} = s_k \mid q) = \frac{\exp(\mathbf{w}_k^T \phi(q))}{\sum_{j=1}^K \exp(\mathbf{w}_j^T \phi(q))}$$
   Where $\phi(q)$ is the stylometric feature vector. The uncalibrated baseline model yields posterior certainty $P(s_4 \mid q) = 0.88$ for a Nigerian English speaker, driven by syntactic transfer artifacts rather than unique individual idiolect.

2. **False Positive Attribution Rate for Minority Sociolects ($FPAR_{\text{minority}}$)**:
   Given non-author texts $q \notin \mathcal{Q}_{s_k}$ originating from dialectal background $v$:
   $$FPAR(v) = P(\hat{s} = s_k \mid s \ne s_k, D = v)$$
   The baseline demonstrates $FPAR(v_{\text{Nigerian}}) = 0.31$ compared to $FPAR(v_{\text{British Standard}}) = 0.04$, representing a nearly eightfold disparity in wrongful accusation risk.

3. **Daubert Standard Evidentiary Admissibility Index ($\mathcal{E}_{\text{Daubert}}$)**:
   Derived from the US Supreme Court *Daubert v. Merrell Dow Pharmaceuticals* (1993) criteria (empirical testing, peer review, known error rate, standard maintenance, and scientific consensus):
   $$\mathcal{E}_{\text{Daubert}} = \frac{1}{5} \sum_{m=1}^5 \mathbf{1}(\text{Criterion}_m \text{ Satisfied})$$
   The baseline achieves $\mathcal{E}_{\text{Daubert}} = 0.20$ due to black-box proprietary code and unknown dialectal error bounds.

---

### 3.3 Case Study 3: Dataset Provenance Gaps in Foundation Models (`cs-dataset-provenance-003`)

#### 3.3.1 Problem Formulation and Linguistic Mechanics
Modern foundation models require web-scale pre-training corpora exceeding hundreds of billions of tokens (Brown et al., 2020; Touvron et al., 2023). Under commercial competitive pressure, scraping pipelines ingest data indiscriminately from digital spaces: clinical self-help communities, private discussion forums, serialized creative writing, and proprietary code repositories. This practice generates critical risks of verbatim extraction of Personally Identifiable Information (PII), medical disclosure, and mass copyright infringement, directly conflicting with EU AI Act Article 10 and Article 53, and GDPR Article 6 and 9.

#### 3.3.2 Quantitative Formulation
1. **Consent Coverage Ratio ($CCR$)**:
   Let $\mathcal{C}$ denote the corpus partitioned into source domains $\mathcal{D}_1, \dots, \mathcal{D}_M$, with token volume $V(\mathcal{D}_m)$:
   $$CCR = \frac{\sum_{m=1}^M V(\mathcal{D}_m) \cdot \mathbf{1}(\text{Consent}(\mathcal{D}_m) = \text{Verified})}{\sum_{m=1}^M V(\mathcal{D}_m)}$$
   The unvetted 700B token web scrape yields $CCR = 0.08$.

2. **Verbatim Memorization Exposure Rate ($\mathcal{M}_{\text{verbatim}}$)**:
   Following Carlini et al. (2021), memorization is quantified by prompting the model with prefix $p$ of length $k$ and observing exact token match of continuation $s$:
   $$\mathcal{M}_{\text{verbatim}}(s) = \mathbf{1}(\arg\max_{\hat{s}} P(\hat{s} \mid p; \theta) = s)$$
   Without deduplication and differential privacy filtering, verbatim memorization of sensitive clinical text reaches unacceptable levels, resulting in a low baseline transparency score ($S_T = 0.20$).

---

## 4. Simulation Mechanics and the Multidimensional Ethical Matrix

<!-- EN: Theoretical and algorithmic specification of the Multidimensional Ethical Matrix, clamping bounds, and trade-off synthesis. | ES: Especificacion teorica y algoritmica de la Matriz Etica Multidimensional, limites de acotamiento y sintesis de compensaciones. -->

To compute real-time feedback without full-page reloads, the simulator implements a deterministic Multidimensional Ethical Matrix governed by three orthogonal normative pillars.

```
+-------------------------------------------------------------------------+
|                  Multidimensional Ethical Evaluation                    |
|                                                                         |
|      Transparency (S_T)        Accountability (S_A)     Fairness (S_F)  |
|      [ Baseline + Mod_T ]      [ Baseline + Mod_A ]  [ Baseline + Mod_F]|
|               |                         |                    |          |
|               +-------------------------+--------------------+          |
|                                         |                               |
|                                         v                               |
|                         Clamping Boundaries [0.0, 1.0]                  |
|                         Calculate Deltas: Delta = S - Baseline          |
|                                         |                               |
|                                         v                               |
|                       Weighted Overall Alignment Index:                 |
|                       I_align = w_T*S_T + w_A*S_A + w_F*S_F             |
|                                         |                               |
|                                         v                               |
|                     EU AI Act & IEEE Regulatory Mapping                 |
|                     Qualitative Trade-Off Narrative Synthesis           |
+-------------------------------------------------------------------------+
```

### 4.1 Ethical Dimensions

1. **Transparency ($S_T \in [0.0, 1.0]$)**:
   Measures system explainability, algorithmic auditability, disclosure of training provenance, and visibility of confidence intervals to end-users (aligned with IEEE 7001-2021 and EU AI Act Article 13).
2. **Accountability ($S_A \in [0.0, 1.0]$)**:
   Measures the presence of verified human oversight (Human-in-the-Loop / Human-on-the-Loop), defined lines of legal and operational responsibility, appeal mechanisms, and audit logging (aligned with EU AI Act Article 14 and GDPR Article 22).
3. **Fairness ($S_F \in [0.0, 1.0]$)**:
   Measures statistical demographic parity, mitigation of dialectal performance gaps, protection of vulnerable demographic groups, and equitable distribution of classification errors (aligned with EU AI Act Article 10 and IEEE 7000-2021).

### 4.2 Score Calculation and Boundary Clamping

For each case study $C$ with baseline matrix $\mathbf{B} = (B_T, B_A, B_F)$ and selected decision option $O$ with modifiers $\mathbf{M} = (M_T, M_A, M_F)$:

$$S_d = \max\left(0.0, \min\left(1.0, \text{round}(B_d + M_d, 3)\right)\right), \quad \forall d \in \{T, A, F\}$$

Score deltas represent the precise directional impact of the learner's intervention:

$$\Delta_d = \text{round}(S_d - B_d, 3), \quad \forall d \in \{T, A, F\}$$

### 4.3 Composite Alignment Index

The overall alignment score $I_{\text{align}}$ is calculated as a convex combination of the dimension scores:

$$I_{\text{align}} = \sum_{d \in \{T, A, F\}} w_d \cdot S_d, \quad \text{subject to } \sum_{d} w_d = 1.0 \text{ and } w_d \ge 0$$

By default, weights are uniform ($w_T = w_A = w_F = \frac{1}{3}$). Custom weighting configurations allow instructors to emphasize specific institutional priorities during simulation runs.

### 4.4 Regulatory Mapping Engine

The engine maps simulation state vectors to statutory risk categories:
- **EU AI Act Risk Classification**:
  - *Unacceptable Risk (Article 5)*: Systems deploying cognitive behavioral manipulation, social scoring, or biometric predictive policing.
  - *High Risk (Annex III)*: Automated employment screening, worker management, judicial support, and law enforcement forensics. Mandates conformity assessment and human oversight.
  - *Specific Transparency Risk (Article 50)*: General-purpose generative conversational systems requiring explicit synthetic disclosure.
  - *Minimal Risk*: Operational systems with no significant fundamental rights impact.
- **IEEE 7000 / 7001 Compliance**:
  - Requires $S_T \ge 0.70$ and $S_F \ge 0.75$ to certify ethical value alignment.

---

## 5. Simulation Mechanics and Empirical Decision Pathways

<!-- EN: Empirical breakdown of simulation runs across the three case studies, comparing status quo, heuristic, and comprehensive options. | ES: Desglose empirico de ejecuciones de simulacion en los tres casos de estudio, comparando opciones de statu quo, heuristicas y exhaustivas. -->

Table 1 summarizes the mathematical trajectories across all seeded case studies and decision options within the platform.

### Table 1
*Simulation Decision Matrix: Baseline Scores, Modifiers, Final Scores, Deltas, and Overall Alignment*

| Case Study | Decision Option Strategy | Dimension | Baseline | Modifier | Final Score | Delta ($\Delta$) | Overall Alignment ($I$) |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Case 1: Recruitment Parsing** | 1. Throughput Maximization | Transparency ($S_T$) | 0.35 | -0.10 | 0.25 | -0.10 | **0.250** |
| | | Accountability ($S_A$) | 0.40 | -0.15 | 0.25 | -0.15 | |
| | | Fairness ($S_F$) | 0.30 | -0.15 | 0.15 | -0.15 | |
| | 2. Surface Heuristic Masking | Transparency ($S_T$) | 0.35 | +0.15 | 0.50 | +0.15 | **0.500** |
| | | Accountability ($S_A$) | 0.40 | +0.10 | 0.50 | +0.10 | |
| | | Fairness ($S_F$) | 0.30 | +0.20 | 0.50 | +0.20 | |
| | 3. Value-Aligned Oversight | Transparency ($S_T$) | 0.35 | +0.45 | 0.80 | +0.45 | **0.833** |
| | | Accountability ($S_A$) | 0.40 | +0.45 | 0.85 | +0.45 | |
| | | Fairness ($S_F$) | 0.30 | +0.55 | 0.85 | +0.55 | |
| **Case 2: Forensic Stylometry** | 1. Automated Probable Cause | Transparency ($S_T$) | 0.25 | -0.15 | 0.10 | -0.15 | **0.083** |
| | | Accountability ($S_A$) | 0.30 | -0.25 | 0.05 | -0.25 | |
| | | Fairness ($S_F$) | 0.35 | -0.25 | 0.10 | -0.25 | |
| | 2. Proprietary Expert Testimony | Transparency ($S_T$) | 0.25 | +0.10 | 0.35 | +0.10 | **0.383** |
| | | Accountability ($S_A$) | 0.30 | +0.10 | 0.40 | +0.10 | |
| | | Fairness ($S_F$) | 0.35 | +0.05 | 0.40 | +0.05 | |
| | 3. Daubert Scientific Protocol | Transparency ($S_T$) | 0.25 | +0.60 | 0.85 | +0.60 | **0.850** |
| | | Accountability ($S_A$) | 0.30 | +0.55 | 0.85 | +0.55 | |
| | | Fairness ($S_F$) | 0.35 | +0.50 | 0.85 | +0.50 | |
| **Case 3: Dataset Provenance** | 1. Unregulated Scaled Ingestion | Transparency ($S_T$) | 0.20 | -0.10 | 0.10 | -0.10 | **0.133** |
| | | Accountability ($S_A$) | 0.25 | -0.15 | 0.10 | -0.15 | |
| | | Fairness ($S_F$) | 0.35 | -0.15 | 0.20 | -0.15 | |
| | 2. Reactive Takedown Portal | Transparency ($S_T$) | 0.20 | +0.20 | 0.40 | +0.20 | **0.433** |
| | | Accountability ($S_A$) | 0.25 | +0.20 | 0.45 | +0.20 | |
| | | Fairness ($S_F$) | 0.35 | +0.10 | 0.45 | +0.10 | |
| | 3. Responsible Provenance Audit | Transparency ($S_T$) | 0.20 | +0.65 | 0.85 | +0.65 | **0.850** |
| | | Accountability ($S_A$) | 0.25 | +0.60 | 0.85 | +0.60 | |
| | | Fairness ($S_F$) | 0.35 | +0.50 | 0.85 | +0.50 | |

*Note*. Score deltas ($\Delta$) indicate shifts relative to the case baseline. Overall alignment is calculated with uniform weights ($w_T = w_A = w_F = \frac{1}{3}$). All values are clamped to the closed interval $[0.0, 1.0]$.

---

## 6. Discussion

<!-- EN: Pedagogical implications, sociotechnical insights, limitations, and future research directions. | ES: Implicaciones pedagogicas, perspectivas sociotecnicas, limitaciones y lineas de investigacion futuras. -->

### 6.1 Pedagogical Efficacy and Moral Reasoning
The interactive simulation mechanics address the core weakness of traditional engineering ethics education: the illusion of the single "optimal" solution. When students select Strategy 3 (Value-Aligned Oversight), they observe significant ethical gains ($I_{\text{align}} = 0.833$ to $0.850$). However, when debriefed on the accompanying operational constraints—namely, that mandatory human oversight increases average resume processing time from 40 milliseconds to 14 minutes, introducing multi-thousand-euro operational expenses—learners confront the reality of engineering economics. This experience cultivates *moral imagination* (Werhane, 1999), preparing future practitioners to articulate rigorous ethical defenses in commercial and governmental environments.

### 6.2 Demystifying Algorithmic Objectivity in Computational Linguistics
The case studies provide empirical demonstrations that language models are not neutral mathematical artifacts. By analyzing the failure of Strategy 2 (Surface Heuristic Masking), learners discover that removing explicit biographical tokens (names, zip codes) fails to eliminate dialectal bias. Latent syntactic markers in AAVE persist through standard word tokenizers and transformer self-attention mechanisms, perpetuating allocative disparities. This outcome teaches engineers that bias mitigation requires deep sociolinguistic understanding, counterfactual data curation, and domain expertise, rather than superficial regex post-processing.

### 6.3 Limitations
While the simulator provides an auditable, reproducible training environment, two primary limitations must be noted:
1. **Discrete Option Space**: Real-world engineering decisions exist along a continuous spectrum rather than among discrete, pre-packaged choices.
2. **Quantitative Proxy Abstraction**: Reducing nuanced normative values (e.g., justice, human dignity, fairness) to normalized floating-point values ($[0.0, 1.0]$) risks reinforcing the computational fallacy that all ethical dilemmas can be solved mathematically. Instructors must emphasize that the matrix serves as a heuristic decision-support mechanism, not an autonomous moral arbiter.

### 6.4 Future Research
Future iterations of the platform will integrate dynamic Large Language Models as real-time evaluators (LLM-as-a-Judge) to semantically analyze open-ended student justifications, challenging logical fallacies and probing the depth of ethical argumentation. Furthermore, we plan to expand the case repository to encompass multilingual machine translation hallucination in asylum proceedings, voice interface accent discrimination in healthcare triage, and retrieval-augmented generation (RAG) provenance tracking.

---

## References

<!-- EN: Comprehensive bibliography formatted strictly according to APA 7th edition standards. | ES: Bibliografia exhaustiva formateada estrictamente bajo las normas APA 7ma edicion. -->

Barocas, S., Hardt, M., & Narayanan, A. (2023). *Fairness and machine learning: Limitations and opportunities*. MIT Press. https://fairmlbook.org/

Bender, E. M., Gebru, T., McMillan-Major, A., & Shmitchell, S. (2021). On the dangers of stochastic parrots: Can language models be too big? In *Proceedings of the 2021 ACM Conference on Fairness, Accountability, and Transparency (FAccT '21)* (pp. 610–623). Association for Computing Machinery. https://doi.org/10.1145/3442188.3445922

Biggs, J. (1996). Enhancing teaching through constructive alignment. *Higher Education*, *32*(3), 347–364. https://doi.org/10.1007/BF00138871

Blodgett, S. L., Barocas, S., Daumé, H., III, & Wallach, H. (2020). Language (technology) is power: A critical survey of "bias" in NLP. In *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics (ACL 2020)* (pp. 5454–5476). Association for Computational Linguistics. https://doi.org/10.18653/v1/2020.acl-main.485

Blodgett, S. L., & O'Connor, B. (2017). Racial disparity in natural language processing: A case study of social media African-American English. In *Proceedings of the 2017 Workshop on Ethics in Natural Language Processing* (pp. 32–41). Association for Computational Linguistics. https://doi.org/10.18653/v1/W17-1605

Bommasani, R., Hudson, D. A., Adeli, E., Altman, R., Arora, S., von Arx, S., ... & Liang, P. (2021). *On the opportunities and risks of foundation models*. arXiv preprint arXiv:2108.07258. https://doi.org/10.48550/arXiv.2108.07258

Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J. D., Dhariwal, P., ... & Amodei, D. (2020). Language models are few-shot learners. *Advances in Neural Information Processing Systems*, *33*, 1877–1901.

Buolamwini, J., & Gebru, T. (2018). Gender shades: Intersectional accuracy disparities in commercial gender classification. In *Proceedings of the 1st Conference on Fairness, Accountability and Transparency (PMLR 81)* (pp. 77–91). Proceedings of Machine Learning Research.

Carlini, N., Tramer, F., Wallace, E., Jagielski, M., Herbert-Voss, A., Lee, K., ... & Raffel, C. (2021). Extracting training data from large language models. In *30th USENIX Security Symposium (USENIX Security 21)* (pp. 2633–2650). USENIX Association.

Chaski, C. E. (2005). Who's at the keyboard? Authorship attribution in digital evidence investigations. *International Journal of Digital Evidence*, *4*(1), 1–13.

Chouldechova, A. (2017). Fair prediction with disparate impact: A study of bias in recidivism prediction instruments. *Big Data*, *5*(2), 153–163. https://doi.org/10.1089/big.2016.0047

Crawford, K. (2017). *The trouble with bias* [Keynote address]. Neural Information Processing Systems (NeurIPS 2017), Long Beach, CA, United States.

Daubert v. Merrell Dow Pharmaceuticals, Inc., 509 U.S. 579 (1993). https://supreme.justia.com/cases/federal/us/509/579/

European Parliament and Council of the European Union. (2024). *Regulation (EU) 2024/1689 of the European Parliament and of the Council of 13 June 2024 laying down harmonised rules on artificial intelligence (Artificial Intelligence Act)*. Official Journal of the European Union, L 2024/1689. http://data.europa.eu/eli/reg/2024/1689/oj

Festinger, L. (1957). *A theory of cognitive dissonance*. Stanford University Press.

Fiesler, C., Garrett, N., & Beard, N. (2020). What do we teach when we teach tech ethics? A syllabi analysis. In *Proceedings of the 51st ACM Technical Symposium on Computer Science Education (SIGCSE '20)* (pp. 289–295). Association for Computing Machinery. https://doi.org/10.1145/3328778.3366825

Floridi, L., Cowls, J., Beltrametti, M., Chatila, R., Chazerand, P., Dignum, V., ... & Vayena, E. (2018). AI4People—An ethical framework for a good AI society: Opportunities, risks, principles, and recommendations. *Minds and Machines*, *28*(4), 689–707. https://doi.org/10.1007/s11023-018-9482-5

Green, B. (2020). The false promise of risk assessments: Epistemic foundations and consequences. In *Proceedings of the 2020 Conference on Fairness, Accountability, and Transparency (FAT* '20)* (pp. 594–606). Association for Computing Machinery. https://doi.org/10.1145/3351095.3372869

Harris, C., Henderson, P., & Mitchell, M. (2022). Exploring dialectal bias in language models: A study of African American English in job matching systems. In *Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing (EMNLP 2022)* (pp. 4120–4135). Association for Computational Linguistics.

IEEE Standards Association. (2021a). *IEEE standard model process for addressing ethical concerns during system design* (IEEE Std 7000-2021). Institute of Electrical and Electronics Engineers. https://doi.org/10.1109/IEEESTD.2021.9536679

IEEE Standards Association. (2021b). *IEEE standard for transparency of autonomous systems* (IEEE Std 7001-2021). Institute of Electrical and Electronics Engineers. https://doi.org/10.1109/IEEESTD.2022.9726144

Juola, P. (2008). Authorship attribution. *Foundations and Trends in Information Retrieval*, *1*(3), 233–334. https://doi.org/10.1561/1500000005

Kleinberg, J., Mullainathan, S., & Raghavan, M. (2016). Inherent trade-offs in the fair determination of risk scores. In *8th Innovations in Theoretical Computer Science Conference (ITCS 2017)* (pp. 43:1–43:23). Schloss Dagstuhl–Leibniz-Zentrum für Informatik. https://doi.org/10.4230/LIPIcs.ITCS.2017.43

Kohlberg, L. (1984). *The psychology of moral development: The nature and validity of moral stages*. Harper & Row.

Kolb, D. A. (1984). *Experiential learning: Experience as the source of learning and development*. Prentice-Hall.

Martin, R. C. (2017). *Clean architecture: A craftsman's guide to software structure and design*. Prentice Hall.

Saltz, J. S., Skirpan, M., Fiesler, C., Gorelick, N., Yeh, T., Heckman, R., ... & Beard, N. (2019). Integrating ethics within machine learning courses. *ACM Transactions on Computing Education*, *19*(4), 1–26. https://doi.org/10.1145/3341164

Touvron, H., Lavril, T., Izacard, G., Martinet, X., Lachaux, M. A., Lacroix, T., ... & Lample, G. (2023). *LLaMA: Open and efficient foundation language models*. arXiv preprint arXiv:2302.13971. https://doi.org/10.48550/arXiv.2302.13971

Werhane, P. H. (1999). *Moral imagination and management decision-making*. Oxford University Press.
