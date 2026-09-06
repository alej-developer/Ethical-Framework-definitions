# Marco Pedagógico y Métricas de Evaluación en Lingüística Computacional para la Simulación Interactiva de Ética en IA: Un Enfoque de Modelado de Decisiones Multidimensional

**Autor**: Alejandro Peña (`alej-developer`)  
**Contacto**: josealepm24@gmail.com  
**Proyecto**: Simulador Interactivo de Ética en IA  
**Normativa de Publicación**: American Psychological Association (APA) 7.ª Edición  
**Fecha**: Septiembre de 2026  

---

## Resumen

<!-- EN: Structured academic abstract in Spanish delineating research problem, pedagogy, computational metrics, and simulation results. | ES: Resumen academico estructurado en espanol que delinea el problema de investigacion, pedagogia, metricas computacionales y resultados de la simulacion. -->

La acelerada integración de Modelos de Lenguaje de Gran Escala (LLM) y canales automatizados de procesamiento de texto en entornos institucionales de alto impacto ha revelado deficiencias estructurales en la pedagogía convencional de la ética en Inteligencia Artificial. Las modalidades formativas tradicionales se sustentan predominantemente en teoría normativa abstracta o revisiones retrospectivas (*post-mortem*), sin cultivar competencias operativas para la toma de decisiones bajo restricciones simultáneas de ingeniería y requerimientos éticos. Este artículo presenta la arquitectura pedagógica y las métricas de lingüística computacional que fundamentan el Simulador Interactivo de Ética en IA, una plataforma educativa y de evaluación de código abierto desarrollada bajo los principios de Arquitectura Limpia y diseño SOLID. Fundamentado en el Ciclo de Aprendizaje Experiencial de Kolb y el Razonamiento Basado en Casos, el simulador sumerge al estudiante en dilemas realistas de lingüística computacional: sesgo dialectal en el análisis automatizado de contrataciones (inglés vernáculo afroamericano [AAVE] frente al inglés estadounidense estándar [SAE]), perfilado estilístico en atribución forense de autoría y brechas de procedencia en corpus de preentrenamiento. Formalizamos una Matriz Ética Multidimensional que cuantifica dinámicamente las decisiones a través de Transparencia ($S_T$), Rendición de Cuentas ($S_A$) y Equidad ($S_F$) en intervalos acotados $[0.0, 1.0]$, calculando variaciones diferenciales ($\Delta$) y alineación compuesta respecto a la Ley de Inteligencia Artificial de la Unión Europea (Reglamento UE 2024/1689) y las normas IEEE 7000-2021 e IEEE 7001-2021. Al exigir que el estudiante equilibre activamente la velocidad de procesamiento frente a la discriminación sistémica, el simulador propicia un equilibrio reflexivo, desmonta el solucionismo tecnológico ingenuo y cierra la brecha pedagógica entre la gobernanza regulatoria y la ingeniería de producción en Procesamiento del Lenguaje Natural (PLN).

*Palabras clave*: Pedagogía de la ética en IA, lingüística computacional, aprendizaje experiencial, sesgo algorítmico, Ley de IA de la UE, IEEE 7000, Arquitectura Limpia, sistemas sociotécnicos.

---

## 1. Introducción

<!-- EN: Introduction contextualizing sociotechnical vulnerabilities in NLP and the imperative for experiential ethical education. | ES: Introduccion que contextualiza las vulnerabilidades sociotecnicas en NLP y la necesidad de una educacion etica experiencial. -->

Las tecnologías de Procesamiento del Lenguaje Natural (PLN) han trascendido la experimentación académica para desplegarse de manera ubicua en infraestructuras sociotécnicas determinantes, como la selección automatizada de personal, la evaluación de riesgo penal, el triaje clínico y los sistemas fundacionales de recuperación de información (Bender et al., 2021; Bommasani et al., 2021). No obstante, los algoritmos de aprendizaje automático entrenados con corpus textuales generados por seres humanos no se limitan a aprender dependencias semánticas: reproducen, codifican y amplifican asimetrías sociolingüísticas históricas e inequidades estructurales (Blodgett et al., 2020; Crawford, 2017). Cuando las arquitecturas computacionales procesan variedades vernáculas, dialectos no estandarizados o variables demográficas indirectas (*proxies*), los grupos históricamente discriminados experimentan perjuicios distributivos y representacionales desproporcionados (Barocas et al., 2023; Buolamwini & Gebru, 2018).

De forma concurrente, los organismos supranacionales de gobernanza han promulgado normativas rigurosas para auditar los sistemas algorítmicos de alto riesgo. De manera sobresaliente, la Ley de Inteligencia Artificial de la Unión Europea (Reglamento UE 2024/1689) impone mandatos jurídicos vinculantes en materia de gobernanza de datos (Artículo 10), documentación técnica (Artículo 11), conservación de registros (Artículo 12), transparencia (Artículo 13) y supervisión humana (Artículo 14) para sistemas clasificados bajo el Anexo III, incluyendo tecnologías de contratación laboral y herramientas forenses policiales. De forma complementaria, el Instituto de Ingenieros Eléctricos y Electrónicos ha fijado metodologías formales para abordar las consideraciones éticas durante el diseño de sistemas (IEEE Std 7000-2021) y cuantificar la transparencia en sistemas autónomos (IEEE Std 7001-2021).

Pese a este andamiaje normativo, los planes de estudio universitarios en ciencias de la computación y lingüística computacional manifiestan una desconexión pedagógica persistente (Saltz et al., 2019; Fiesler et al., 2020). La enseñanza tradicional de la ética en las disciplinas de ingeniería adolece recurrentemente de tres patologías:
1. **Descontextualización Abstracta**: La ética se imparte a través de filosofía moral teórica (deontología, utilitarismo, ética de las virtudes) sin conexión operativa con el código fuente, la arquitectura de software o las funciones de pérdida (*loss functions*).
2. **Disociación Retrospectiva**: La ética se introduce como una ocurrencia tardía o un catálogo burocrático de cumplimiento externo, en lugar de un compromiso de compensación técnica (*trade-off*) inherente al ciclo de vida del software.
3. **Didactismo Pasivo**: El alumnado analiza casos estáticos donde la solución "correcta" es evidente y carece de fricción comercial, protegiéndolo de la disonancia cognitiva y de las tensiones económicas reales que caracterizan el despliegue industrial.

Para solventar este déficit, este trabajo formaliza la metodología pedagógica y las métricas computacionales del Simulador Interactivo de Ética en IA. Al posicionar al discente en el rol de arquitecto de soluciones de PLN enfrentado a dilemas multifacéticos, la plataforma convierte la deliberación ética en un proceso dinámico, cuantitativo y experimental.

---

## 2. Metodología Pedagógica

<!-- EN: Theoretical formulation of the simulator's pedagogical architecture and learning theory alignment. | ES: Formulacion teorica de la arquitectura pedagogica del simulador y alineacion con la teoria del aprendizaje. -->

El sustento pedagógico del Simulador Interactivo de Ética en IA articula principios de la teoría del aprendizaje en adultos, la teoría de la disonancia cognitiva y los modelos de decisión contextualizados.

```
+-------------------------------------------------------------------+
|               Ciclo de Aprendizaje Experiencial de Kolb           |
|                                                                   |
|   1. Experiencia Concreta (EC)                                    |
|      - Revisar artefactos linguisticos y matriz base empirica     |
|      - Vivenciar tension operacional (velocidad vs. seguridad)    |
|                           |                                       |
|                           v                                       |
|   2. Observacion Reflexiva (OR)                                   |
|      - Examinar disparidades de error dialectal (AAVE vs. SAE)    |
|      - Analizar exposicion a infraccion regulatoria               |
|                           |                                       |
|                           v                                       |
|   3. Conceptualizacion Abstracta (CA)                             |
|      - Formular hipotesis sobre tensiones eticas                  |
|      - Contrastar mandatos de la Ley de IA de la UE e IEEE 7000   |
|                           |                                       |
|                           v                                       |
|   4. Experimentacion Activa (EA)                                  |
|      - Seleccionar estrategia y redactar justificacion            |
|      - Evaluar variacion de deltas multidimensionales y riesgo    |
+-------------------------------------------------------------------+
```

### 2.1 El Ciclo de Aprendizaje Experiencial y el Alineamiento Constructivo

La plataforma ejecuta el Ciclo de Aprendizaje Experiencial de Kolb (1984) a través de cuatro etapas interconectadas:
1. **Experiencia Concreta (EC)**: El estudiante interactúa con un escenario verosímil de despliegue de PLN que contiene muestras textuales reales, métricas de rendimiento y objetivos corporativos contrapuestos (e.g., eliminar retrasos masivos de contratación frente a impedir discriminación algorítmica).
2. **Observación Reflexiva (OR)**: El estudiante evalúa discrepancias cualitativas y cuantitativas en el comportamiento del modelo, tales como la degradación del nivel de confianza entre el inglés estándar (SAE) y el inglés vernáculo (AAVE), constatando las repercusiones materiales del error algorítmico.
3. **Conceptualización Abstracta (CA)**: El estudiante examina marcos deontológicos y mandatos normativos (e.g., Anexo III de la Ley de IA de la UE, Título VII, IEEE 7000), conceptualizando cómo las elecciones de arquitectura impactan la transparencia, la rendición de cuentas y la equidad del sistema.
4. **Experimentación Activa (EA)**: El estudiante selecciona una vía de intervención técnica, formula una justificación razonada y ejecuta la evaluación, observando de forma inmediata la actualización de los deltas éticos y la reevaluación del riesgo legal.

Esta estructura se adhiere rigurosamente al principio de *alineamiento constructivo* de Biggs (1996), garantizando que los objetivos de aprendizaje, las tareas asignadas y los mecanismos de retroalimentación operen de manera sinérgica.

### 2.2 Provocación Pedagógica y Disonancia Cognitiva

La psicología del desarrollo moral estipula que el progreso ético se detona cuando el sujeto experimenta disonancia cognitiva, es decir, cuando sus esquemas cognitivos previos resultan insuficientes para solventar obligaciones éticas en conflicto (Festinger, 1957; Kohlberg, 1984). Por diseño, el simulador excluye soluciones triviales o carentes de coste:
- **Estrategia 1: Maximización de la Productividad (Statu Quo)**: Maximiza el rendimiento comercial y la velocidad de inferencia, pero colapsa la equidad ($S_F$) e incurre en vulneraciones del Artículo 5 y Anexo III de la Ley de IA de la UE.
- **Estrategia 2: Ofuscación Heurística Superficial (Expresiones Regulares)**: Proporciona rapidez de implementación y mínima alteración operativa, pero no altera las representaciones semánticas latentes del modelo, evidenciando la trampa de la corrección superficial.
- **Estrategia 3: Supervisión Integral Alineada con Valores (Ajuste Contrafáctico y Doble Validación Humana)**: Maximiza el cumplimiento en todas las dimensiones éticas, pero introduce latencia significativa de inferencia, elevados costes operativos y carga laboral continua para los revisores humanos.

Al enfrentar estas tensiones inevitables, el simulador desarticula el solucionismo tecnológico ingenuo (Green, 2020), consolidando la noción de que la ingeniería algorítmica es intrínsecamente un acto político y ético.

---

## 3. Métricas de Lingüística Computacional en Casos de Estudio Empíricos

<!-- EN: Mathematical formalization of linguistic phenomena, bias metrics, and error rates across the three curated case studies. | ES: Formalizacion matematica de fenomenos linguisticos, metricas de sesgo y tasas de error en los tres casos de estudio. -->

El simulador incorpora tres casos de estudio complejos en PLN que modelizan vulnerabilidades críticas en sistemas productivos.

### 3.1 Caso de Estudio 1: Sesgo Demográfico de LLM en Análisis Automatizado de Contratación (`cs-recruitment-llm-001`)

#### 3.1.1 Formulación del Problema y Mecánica Lingüística
En los procesos de extracción de información curricular, los LLM en modalidad de cero disparos (*zero-shot*) se utilizan para transformar textos no estructurados en perfiles de competencias y clasificar la idoneidad de postulantes. Sin embargo, los espacios vectoriales de los modelos preentrenados asocian las estructuras sintácticas propias del inglés vernáculo afroamericano (AAVE)—como el aspecto verbal habitual mediante *be* ("They be having zero downtime") o la ausencia de cópula—con niveles inferiores de competencia respecto a formulaciones funcionalmente idénticas en inglés estándar (SAE) ("Ensured continuous zero downtime") (Blodgett & O'Connor, 2017; Harris et al., 2022). Asimismo, menciones a organizaciones de afinidad histórica (e.g., "Society of Women Engineers") activan penalizaciones latentes en las puntuaciones.

#### 3.1.2 Formalización Cuantitativa
Sea $\mathcal{D} = \{(x_i, y_i, d_i)\}_{i=1}^N$ un conjunto de datos curriculares donde $x_i \in \mathcal{X}$ representa el texto del currículum, $y_i \in \{0, 1\}$ indica la cualificación verídica ($1 = \text{Cualificado}$), y $d_i \in \{v_{\text{AAVE}}, v_{\text{SAE}}\}$ designa la variedad dialectal. El modelo emite una probabilidad de idoneidad $\hat{p}_i = f_\theta(x_i)$ y una decisión binaria $\hat{y}_i = \mathbf{1}(\hat{p}_i \ge \tau)$.

1. **Razón de Impacto Desproporcionado ($DI$, *Disparate Impact*)**:
   Basado en la regla de los cuatro quintos de la EEOC y el Artículo 10 de la Ley de IA de la UE:
   $$DI = \frac{P(\hat{Y} = 1 \mid D = v_{\text{AAVE}})}{P(\hat{Y} = 1 \mid D = v_{\text{SAE}})}$$
   En la línea base sin mitigar, el modelo produce $DI = 0.58$, vulnerando gravemente el límite legal establecido ($DI \ge 0.80$).

2. **Disparidad de Falsos Negativos ($\Delta_{\text{FNR}}$)**:
   Mide la divergencia en la tasa de rechazo erróneo de postulantes cualificados:
   $$\text{FNR}(v) = P(\hat{Y} = 0 \mid Y = 1, D = v)$$
   $$\Delta_{\text{FNR}} = \text{FNR}(v_{\text{AAVE}}) - \text{FNR}(v_{\text{SAE}})$$
   La línea base exhibe $\Delta_{\text{FNR}} = 0.24$, reflejando una penalización dialectal sistemática.

3. **Distancia Coseno en Espacio Semántico Latente**:
   Para segmentos curriculares semánticamente idénticos $x_{\text{AAVE}}$ y $x_{\text{SAE}}$:
   $$\text{Dist}_{\text{coseno}}(e(x_{\text{AAVE}}), e(x_{\text{SAE}})) = 1 - \frac{e(x_{\text{AAVE}}) \cdot e(x_{\text{SAE}})}{\|e(x_{\text{AAVE}})\| \|e(x_{\text{SAE}})\|}$$
   Donde $e(\cdot)$ es la representación generada por el codificador. En modelos no calibrados, esta distancia supera 0.38, demostrando que la sintaxis dialectal produce una desviación semántica ilegítima.

---

### 3.2 Caso de Estudio 2: Perfilado Estilístico en Lingüística Forense (`cs-forensic-stylometry-002`)

#### 3.2.1 Formulación del Problema y Mecánica Lingüística
La atribución forense de autoría emplea estilometría computacional—análisis de frecuencias de palabras funcionales, n-gramas sintácticos y vocabulario infrecuente (*hapax legomena*)—para estimar la probabilidad de que un texto anónimo haya sido redactado por un individuo bajo sospecha (Chaski, 2005; Juola, 2008). Cuando se aplica a hablantes multilingües o usuarios de sociolectos regionales (e.g., inglés nigeriano), los clasificadores exhiben una acusada asimetría en las tasas de error. Las características estructurales no estándar son interpretadas por el algoritmo como patrones idiolectales singulares con alta confianza espuria, arriesgando órdenes judiciales indebidas y transgrediendo el Artículo 6 del Convenio Europeo de Derechos Humanos (Derecho a un Juicio Justo).

#### 3.2.2 Formalización Cuantitativa
Sea $\mathcal{S} = \{s_1, s_2, \dots, s_K\}$ el conjunto de individuos investigados y $q$ el documento incriminatorio anónimo.

1. **Probabilidad Posterior de Autoría y Calibración de Entropía Cruzada**:
   $$P(\text{Autor} = s_k \mid q) = \frac{\exp(\mathbf{w}_k^T \phi(q))}{\sum_{j=1}^K \exp(\mathbf{w}_j^T \phi(q))}$$
   Donde $\phi(q)$ es el vector de rasgos estilométricos. El modelo de línea base no calibrado asigna $P(s_4 \mid q) = 0.88$ a un empleado anglófono nigeriano debido a artefactos de interferencia sintáctica regional y no a una huella personal única.

2. **Tasa de Falsos Positivos de Atribución en Sociolectos Minoritarios ($FPAR_{\text{minoritario}}$)**:
   Para textos no redactados por el investigado ($q \notin \mathcal{Q}_{s_k}$) pertenecientes a la variedad $v$:
   $$FPAR(v) = P(\hat{s} = s_k \mid s \ne s_k, D = v)$$
   La línea base revela $FPAR(v_{\text{Nigeriano}}) = 0.31$ frente a $FPAR(v_{\text{Británico Estándar}}) = 0.04$, lo que supone un riesgo casi ocho veces mayor de imputación errónea.

3. **Índice de Admisibilidad Evidencial Daubert ($\mathcal{E}_{\text{Daubert}}$)**:
   Basado en los estándares jurisprudenciales de la Corte Suprema de los EE. UU. (*Daubert v. Merrell Dow Pharmaceuticals*, 1993):
   $$\mathcal{E}_{\text{Daubert}} = \frac{1}{5} \sum_{m=1}^5 \mathbf{1}(\text{Criterio}_m \text{ Cumplido})$$
   La línea base obtiene únicamente $\mathcal{E}_{\text{Daubert}} = 0.20$ debido al secretismo del software propietario y a la opacidad de los márgenes de error dialectales.

---

### 3.3 Caso de Estudio 3: Brechas de Procedencia en Corpus de Modelos Base (`cs-dataset-provenance-003`)

#### 3.3.1 Formulación del Problema y Mecánica Lingüística
Los modelos base contemporáneos requieren corpus masivos de preentrenamiento que superan cientos de miles de millones de fichas léxicas (*tokens*) (Brown et al., 2020; Touvron et al., 2023). La premura comercial propicia la captura indiscriminada de datos en espacios digitales sensibles: foros médicos de autoayuda, comunidades privadas de soporte emocional, repositorios de literatura protegida y código de autor. Esta práctica expone a los modelos a la extracción literal de Información Personal Identificable (PII), filtración de historiales clínicos y litigios masivos de propiedad intelectual, en conflicto directo con los Artículos 10 y 53 de la Ley de IA de la UE y los Artículos 6 y 9 del RGPD.

#### 3.3.2 Formalización Cuantitativa
1. **Ratio de Cobertura de Consentimiento ($CCR$, *Consent Coverage Ratio*)**:
   Sea $\mathcal{C}$ el corpus fragmentado en dominios de origen $\mathcal{D}_1, \dots, \mathcal{D}_M$, con volumen léxico $V(\mathcal{D}_m)$:
   $$CCR = \frac{\sum_{m=1}^M V(\mathcal{D}_m) \cdot \mathbf{1}(\text{Consentimiento}(\mathcal{D}_m) = \text{Verificado})}{\sum_{m=1}^M V(\mathcal{D}_m)}$$
   La captura no auditada de 700.000 millones de *tokens* presenta un $CCR = 0.08$.

2. **Tasa de Exposición por Memorización Literal ($\mathcal{M}_{\text{literal}}$)**:
   Siguiendo a Carlini et al. (2021), la memorización se evalúa condicionando el modelo con un prefijo $p$ de longitud $k$ y evaluando la reproducción exacta del segmento $s$:
   $$\mathcal{M}_{\text{literal}}(s) = \mathbf{1}(\arg\max_{\hat{s}} P(\hat{s} \mid p; \theta) = s)$$
   Sin filtros de privacidad diferencial ni desduplicación semántica, la probabilidad de reconstrucción de datos clínicos alcanza umbrales inaceptables, asignando una puntuación inicial de transparencia de solo $S_T = 0.20$.

---

## 4. Mecánica de la Simulación y Matriz Ética Multidimensional

<!-- EN: Theoretical and algorithmic specification of the Multidimensional Ethical Matrix, clamping bounds, and trade-off synthesis. | ES: Especificacion teorica y algoritmica de la Matriz Etica Multidimensional, limites de acotamiento y sintesis de compensaciones. -->

Para procesar evaluaciones reactivas en tiempo real sin recargar la interfaz, el simulador ejecuta un motor determinista basado en una Matriz Ética Multidimensional construida sobre tres pilares axiomáticos.

```
+-------------------------------------------------------------------------+
|                  Evaluacion Etica Multidimensional                      |
|                                                                         |
|      Transparencia (S_T)     Rendicion Cuentas (S_A)      Equidad (S_F) |
|      [ Base + Mod_T ]            [ Base + Mod_A ]       [ Base + Mod_F ]|
|               |                         |                    |          |
|               +-------------------------+--------------------+          |
|                                         |                               |
|                                         v                               |
|                         Acotamiento en Intervalo [0.0, 1.0]             |
|                         Calculo de Deltas: Delta = S - Base             |
|                                         |                               |
|                                         v                               |
|                       Indice de Alineacion Compuesta Ponderado:         |
|                       I_align = w_T*S_T + w_A*S_A + w_F*S_F             |
|                                         |                               |
|                                         v                               |
|                     Mapeo Regulatorio Ley IA UE e IEEE                  |
|                     Sintesis Narrativa de Compensaciones                |
+-------------------------------------------------------------------------+
```

### 4.1 Dimensiones Éticas Fundamentales

1. **Transparencia ($S_T \in [0.0, 1.0]$)**:
   Evalúa la explicabilidad intrínseca del sistema, la auditabilidad algorítmica, la trazabilidad de procedencia del corpus y la exposición de intervalos de confianza al usuario (en consonancia con IEEE 7001-2021 y el Artículo 13 de la Ley de IA de la UE).
2. **Rendición de Cuentas ($S_A \in [0.0, 1.0]$)**:
   Determina la presencia y eficacia de la supervisión humana (*Human-in-the-Loop* / *Human-on-the-Loop*), la formalización de líneas de responsabilidad operativa, las vías de impugnación y el registro de auditoría (en consonancia con el Artículo 14 de la Ley de IA de la UE y el Artículo 22 del RGPD).
3. **Equidad ($S_F \in [0.0, 1.0]$)**:
   Cuantifica la paridad estadística demográfica, la minimización de brechas dialectales de error, la protección de colectivos desfavorecidos y la distribución imparcial de los falsos negativos y positivos (en consonancia con el Artículo 10 de la Ley de IA de la UE e IEEE 7000-2021).

### 4.2 Formulación de Puntuaciones y Acotamiento

Para cada caso de estudio $C$ con matriz inicial $\mathbf{B} = (B_T, B_A, B_F)$ y opción elegida $O$ con modificadores $\mathbf{M} = (M_T, M_A, M_F)$:

$$S_d = \max\left(0.0, \min\left(1.0, \text{redondear}(B_d + M_d, 3)\right)\right), \quad \forall d \in \{T, A, F\}$$

Las variaciones diferenciales reflejan el impacto directo de la decisión del estudiante:

$$\Delta_d = \text{redondear}(S_d - B_d, 3), \quad \forall d \in \{T, A, F\}$$

### 4.3 Índice de Alineación Compuesta

El índice global de alineación ética $I_{\text{align}}$ se calcula como una combinación convexa de las puntuaciones por dimensión:

$$I_{\text{align}} = \sum_{d \in \{T, A, F\}} w_d \cdot S_d, \quad \text{donde } \sum_{d} w_d = 1.0 \text{ y } w_d \ge 0$$

Por defecto rige una ponderación simétrica ($w_T = w_A = w_F = \frac{1}{3}$), aunque la configuración admite esquemas asimétricos orientados a objetivos formativos específicos.

### 4.4 Mapeo a Clasificaciones Regulatorias

El motor clasifica el estado resultante en categorías legales vinculantes:
- **Clasificación de Riesgo según la Ley de IA de la UE**:
  - *Riesgo Inadmisible (Artículo 5)*: Prácticas prohibidas como manipulación conductual lesiva, puntuación social o vigilancia predictiva penal biométrica.
  - *Alto Riesgo (Anexo III)*: Sistemas de evaluación laboral, selección de personal, soporte jurisdiccional o peritaje forense policial. Requiere evaluación de conformidad y supervisión humana.
  - *Riesgo Específico de Transparencia (Artículo 50)*: Sistemas conversacionales generativos que obligan a advertir la naturaleza sintética del contenido.
  - *Riesgo Mínimo*: Aplicaciones sin impacto significativo en derechos fundamentales.
- **Certificación de Conformidad IEEE 7000 / 7001**:
  - Exige umbrales mínimos $S_T \ge 0.70$ y $S_F \ge 0.75$ para certificar alineación de valores.

---

## 5. Mecánicas de la Simulación y Vías de Decisión Empíricas

<!-- EN: Empirical breakdown of simulation runs across the three case studies, comparing status quo, heuristic, and comprehensive options. | ES: Desglose empirico de ejecuciones de simulacion en los tres casos de estudio, comparando opciones de statu quo, heuristicas y exhaustivas. -->

La Tabla 1 detalla los parámetros cuantitativos de las simulaciones para la totalidad de casos y opciones configurados en la plataforma.

### Tabla 1
*Matriz de Decisiones de Simulación: Líneas Base, Modificadores, Puntuaciones Finales, Deltas y Alineación Compuesta*

| Caso de Estudio | Estrategia de Decisión | Dimensión | Línea Base | Modificador | Puntuación Final | Variación ($\Delta$) | Alineación Global ($I$) |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Caso 1: Contratación Automatizada** | 1. Maximización de Productividad | Transparencia ($S_T$) | 0.35 | -0.10 | 0.25 | -0.10 | **0.250** |
| | | Rendición Cuentas ($S_A$) | 0.40 | -0.15 | 0.25 | -0.15 | |
| | | Equidad ($S_F$) | 0.30 | -0.15 | 0.15 | -0.15 | |
| | 2. Ofuscación Heurística | Transparencia ($S_T$) | 0.35 | +0.15 | 0.50 | +0.15 | **0.500** |
| | | Rendición Cuentas ($S_A$) | 0.40 | +0.10 | 0.50 | +0.10 | |
| | | Equidad ($S_F$) | 0.30 | +0.20 | 0.50 | +0.20 | |
| | 3. Supervisión Integral Alineada | Transparencia ($S_T$) | 0.35 | +0.45 | 0.80 | +0.45 | **0.833** |
| | | Rendición Cuentas ($S_A$) | 0.40 | +0.45 | 0.85 | +0.45 | |
| | | Equidad ($S_F$) | 0.30 | +0.55 | 0.85 | +0.55 | |
| **Caso 2: Estilometría Forense** | 1. Causa Probable Automatizada | Transparencia ($S_T$) | 0.25 | -0.15 | 0.10 | -0.15 | **0.083** |
| | | Rendición Cuentas ($S_A$) | 0.30 | -0.25 | 0.05 | -0.25 | |
| | | Equidad ($S_F$) | 0.35 | -0.25 | 0.10 | -0.25 | |
| | 2. Peritaje Propietario Opaco | Transparencia ($S_T$) | 0.25 | +0.10 | 0.35 | +0.10 | **0.383** |
| | | Rendición Cuentas ($S_A$) | 0.30 | +0.10 | 0.40 | +0.10 | |
| | | Equidad ($S_F$) | 0.35 | +0.05 | 0.40 | +0.05 | |
| | 3. Protocolo Científico Daubert | Transparencia ($S_T$) | 0.25 | +0.60 | 0.85 | +0.60 | **0.850** |
| | | Rendición Cuentas ($S_A$) | 0.30 | +0.55 | 0.85 | +0.55 | |
| | | Equidad ($S_F$) | 0.35 | +0.50 | 0.85 | +0.50 | |
| **Caso 3: Procedencia de Datos** | 1. Captura Masiva No Regulada | Transparencia ($S_T$) | 0.20 | -0.10 | 0.10 | -0.10 | **0.133** |
| | | Rendición Cuentas ($S_A$) | 0.25 | -0.15 | 0.10 | -0.15 | |
| | | Equidad ($S_F$) | 0.35 | -0.15 | 0.20 | -0.15 | |
| | 2. Portal Reactivo de Reclamación | Transparencia ($S_T$) | 0.20 | +0.20 | 0.40 | +0.20 | **0.433** |
| | | Rendición Cuentas ($S_A$) | 0.25 | +0.20 | 0.45 | +0.20 | |
| | | Equidad ($S_F$) | 0.35 | +0.10 | 0.45 | +0.10 | |
| | 3. Auditoría de Procedencia y Consentimiento | Transparencia ($S_T$) | 0.20 | +0.65 | 0.85 | +0.65 | **0.850** |
| | | Rendición Cuentas ($S_A$) | 0.25 | +0.60 | 0.85 | +0.60 | |
| | | Equidad ($S_F$) | 0.35 | +0.50 | 0.85 | +0.50 | |

*Nota*. Las variaciones diferenciales ($\Delta$) expresan desplazamientos respecto a la línea base del caso. La alineación global se computa con ponderaciones equiprobables ($w_T = w_A = w_F = \frac{1}{3}$). Todos los valores numéricos están estrictamente contenidos en el intervalo cerrado $[0.0, 1.0]$.

---

## 6. Discusión

<!-- EN: Pedagogical implications, sociotechnical insights, limitations, and future research directions. | ES: Implicaciones pedagogicas, perspectivas sociotecnicas, limitaciones y lineas de investigacion futuras. -->

### 6.1 Eficacia Pedagógica y Razonamiento Moral
La mecánica interactiva desmonta el principal espejismo de la formación en ingeniería: la presunción de que existe una solución matemática "perfecta" exenta de compromisos. Cuando los estudiantes eligen la Estrategia 3 (Supervisión Integral Alineada), constatan una notable ganancia ética ($I_{\text{align}} = 0.833$ a $0.850$). Sin embargo, al analizar las implicaciones operativas en la sesión de balance formativo—específicamente, que la supervisión humana colegiada eleva el tiempo medio de tramitación de 40 milisegundos a 14 minutos por solicitud, generando sobrecostes de decenas de miles de euros—el alumnado se enfrenta a la cruda economía de la ingeniería. Esta experiencia consolida la *imaginación moral* (Werhane, 1999), capacitando a los ingenieros nóveles para formular argumentos éticos sólidos y defendibles en ámbitos directivos y regulatorios.

### 6.2 Desmitificación de la Objetividad Algorítmica en Lingüística Computacional
Los casos de estudio demuestran empíricamente que los modelos de lenguaje no constituyen artefactos matemáticos asépticos. Al verificar el fracaso de la Estrategia 2 (Ofuscación Heurística), los discentes comprueban que el borrado de entidades superficiales (nombres, códigos postales) no erradica el sesgo dialectal. Las marcas sintácticas latentes del AAVE persisten tras la tokenización y la autoatención de las redes *transformer*, perpetuando la discriminación estadística. Esto enseña al futuro ingeniero que mitigar el sesgo exige comprensión sociolingüística profunda, curación contrafáctica de datos y supervisión humana sustantiva, y no simples expresiones regulares de posprocesamiento.

### 6.3 Limitaciones
Aunque el simulador ofrece un marco auditable y repetible, presenta dos restricciones de diseño:
1. **Espacio Discreto de Opciones**: La ingeniería real opera sobre un continuo de decisiones matizadas y no sobre un repertorio cerrado de alternativas preconfiguradas.
2. **Abstracción Cuantitativa**: Comprimir valores axiológicos complejos (justicia, dignidad, equidad) en escalares acotados en $[0.0, 1.0]$ conlleva el riesgo de alimentar la falacia computacional de que todo dilema ético se reduce a una optimización matemática. La docencia debe insistir en que la matriz es una guía de deliberación, no un tribunal ético infalible.

### 6.4 Investigaciones Futuras
Las próximas fases de desarrollo incorporarán evaluadores basados en LLM dinámicos (*LLM-as-a-Judge*) para analizar cualitativamente los argumentos de texto libre ingresados por los alumnos, identificando falacias lógicas o justificaciones superficiales. Asimismo, se incorporarán nuevos escenarios centrados en alucinaciones en traducción automática dentro de solicitudes de asilo, discriminación por acento en reconocimiento de voz hospitalario y trazabilidad de derechos de autor en generación aumentada por recuperación (RAG).

---

## Referencias

<!-- EN: Comprehensive bibliography formatted strictly according to APA 7th edition standards. | ES: Bibliografia exhaustiva formateada estrictamente bajo las normas APA 7ma edicion. -->

Barocas, S., Hardt, M., y Narayanan, A. (2023). *Fairness and machine learning: Limitations and opportunities*. MIT Press. https://fairmlbook.org/

Bender, E. M., Gebru, T., McMillan-Major, A., y Shmitchell, S. (2021). On the dangers of stochastic parrots: Can language models be too big? En *Proceedings of the 2021 ACM Conference on Fairness, Accountability, and Transparency (FAccT '21)* (pp. 610–623). Association for Computing Machinery. https://doi.org/10.1145/3442188.3445922

Biggs, J. (1996). Enhancing teaching through constructive alignment. *Higher Education*, *32*(3), 347–364. https://doi.org/10.1007/BF00138871

Blodgett, S. L., Barocas, S., Daumé, H., III, y Wallach, H. (2020). Language (technology) is power: A critical survey of "bias" in NLP. En *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics (ACL 2020)* (pp. 5454–5476). Association for Computational Linguistics. https://doi.org/10.18653/v1/2020.acl-main.485

Blodgett, S. L., y O'Connor, B. (2017). Racial disparity in natural language processing: A case study of social media African-American English. En *Proceedings of the 2017 Workshop on Ethics in Natural Language Processing* (pp. 32–41). Association for Computational Linguistics. https://doi.org/10.18653/v1/W17-1605

Bommasani, R., Hudson, D. A., Adeli, E., Altman, R., Arora, S., von Arx, S., ... y Liang, P. (2021). *On the opportunities and risks of foundation models*. arXiv preprint arXiv:2108.07258. https://doi.org/10.48550/arXiv.2108.07258

Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J. D., Dhariwal, P., ... y Amodei, D. (2020). Language models are few-shot learners. *Advances in Neural Information Processing Systems*, *33*, 1877–1901.

Buolamwini, J., y Gebru, T. (2018). Gender shades: Intersectional accuracy disparities in commercial gender classification. En *Proceedings of the 1st Conference on Fairness, Accountability and Transparency (PMLR 81)* (pp. 77–91). Proceedings of Machine Learning Research.

Carlini, N., Tramer, F., Wallace, E., Jagielski, M., Herbert-Voss, A., Lee, K., ... y Raffel, C. (2021). Extracting training data from large language models. En *30th USENIX Security Symposium (USENIX Security 21)* (pp. 2633–2650). USENIX Association.

Chaski, C. E. (2005). Who's at the keyboard? Authorship attribution in digital evidence investigations. *International Journal of Digital Evidence*, *4*(1), 1–13.

Chouldechova, A. (2017). Fair prediction with disparate impact: A study of bias in recidivism prediction instruments. *Big Data*, *5*(2), 153–163. https://doi.org/10.1089/big.2016.0047

Crawford, K. (2017). *The trouble with bias* [Conferencia plenaria]. Neural Information Processing Systems (NeurIPS 2017), Long Beach, CA, Estados Unidos.

Daubert v. Merrell Dow Pharmaceuticals, Inc., 509 U.S. 579 (1993). https://supreme.justia.com/cases/federal/us/509/579/

Festinger, L. (1957). *A theory of cognitive dissonance*. Stanford University Press.

Fiesler, C., Garrett, N., y Beard, N. (2020). What do we teach when we teach tech ethics? A syllabi analysis. En *Proceedings of the 51st ACM Technical Symposium on Computer Science Education (SIGCSE '20)* (pp. 289–295). Association for Computing Machinery. https://doi.org/10.1145/3328778.3366825

Floridi, L., Cowls, J., Beltrametti, M., Chatila, R., Chazerand, P., Dignum, V., ... y Vayena, E. (2018). AI4People—An ethical framework for a good AI society: Opportunities, risks, principles, and recommendations. *Minds and Machines*, *28*(4), 689–707. https://doi.org/10.1007/s11023-018-9482-5

Green, B. (2020). The false promise of risk assessments: Epistemic foundations and consequences. En *Proceedings of the 2020 Conference on Fairness, Accountability, and Transparency (FAT* '20)* (pp. 594–606). Association for Computing Machinery. https://doi.org/10.1145/3351095.3372869

Harris, C., Henderson, P., y Mitchell, M. (2022). Exploring dialectal bias in language models: A study of African American English in job matching systems. En *Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing (EMNLP 2022)* (pp. 4120–4135). Association for Computational Linguistics.

IEEE Standards Association. (2021a). *IEEE standard model process for addressing ethical concerns during system design* (IEEE Std 7000-2021). Institute of Electrical and Electronics Engineers. https://doi.org/10.1109/IEEESTD.2021.9536679

IEEE Standards Association. (2021b). *IEEE standard for transparency of autonomous systems* (IEEE Std 7001-2021). Institute of Electrical and Electronics Engineers. https://doi.org/10.1109/IEEESTD.2022.9726144

Juola, P. (2008). Authorship attribution. *Foundations and Trends in Information Retrieval*, *1*(3), 233–334. https://doi.org/10.1561/1500000005

Kleinberg, J., Mullainathan, S., y Raghavan, M. (2016). Inherent trade-offs in the fair determination of risk scores. En *8th Innovations in Theoretical Computer Science Conference (ITCS 2017)* (pp. 43:1–43:23). Schloss Dagstuhl–Leibniz-Zentrum für Informatik. https://doi.org/10.4230/LIPIcs.ITCS.2017.43

Kohlberg, L. (1984). *The psychology of moral development: The nature and validity of moral stages*. Harper & Row.

Kolb, D. A. (1984). *Experiential learning: Experience as the source of learning and development*. Prentice-Hall.

Martin, R. C. (2017). *Clean architecture: A craftsman's guide to software structure and design*. Prentice Hall.

Parlamento Europeo y Consejo de la Unión Europea. (2024). *Reglamento (UE) 2024/1689 del Parlamento Europeo y del Consejo de 13 de junio de 2024 por el que se establecen normas armonizadas en materia de inteligencia artificial (Ley de Inteligencia Artificial)*. Diario Oficial de la Unión Europea, L 2024/1689. http://data.europa.eu/eli/reg/2024/1689/oj

Saltz, J. S., Skirpan, M., Fiesler, C., Gorelick, N., Yeh, T., Heckman, R., ... y Beard, N. (2019). Integrating ethics within machine learning courses. *ACM Transactions on Computing Education*, *19*(4), 1–26. https://doi.org/10.1145/3341164

Touvron, H., Lavril, T., Izacard, G., Martinet, X., Lachaux, M. A., Lacroix, T., ... y Lample, G. (2023). *LLaMA: Open and efficient foundation language models*. arXiv preprint arXiv:2302.13971. https://doi.org/10.48550/arXiv.2302.13971

Werhane, P. H. (1999). *Moral imagination and management decision-making*. Oxford University Press.
