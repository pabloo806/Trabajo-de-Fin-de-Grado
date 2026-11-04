# ADR-009: Conjunto de Evaluación y Protocolo de Validación

## Estado

**Propuesto.** Pendiente de validación por tutor y cotutor (OD-08) y de la prueba de concepto que ratifica los umbrales provisionales (hito H2). No cierra ninguna decisión abierta por sí mismo.

## Fecha

2026-10-30

## Requisitos relacionados

| Requisito | Relación |
|---|---|
| RF-29 | Informe de discrepancias entre cada motor y la referencia de Rekordbox (Must, OD-01) |
| RF-29b | Importación de los valores de referencia desde el XML de colección o un CSV |
| RNF-05, RNF-06 | Exactitud de BPM estricta y con tolerancia de octava |
| RNF-07, RNF-08 | Exactitud de tonalidad exacta y por compatibilidad Camelot |
| RNF-09 | Desglose de errores con intervalos de confianza |
| RNF-10, RNF-11 | Cumplimiento de restricciones y determinismo del generador |
| RNF-01, RNF-02, RNF-03, RNF-18 | Medidas de rendimiento y de escala |
| RNF-12 | Valoración de la coherencia de los setlists por DJs |
| RNF-13 | Eficiencia de uso de un DJ nuevo |
| RF-23 | Verificación manual de la importación en Rekordbox |

Riesgos asociados: R-01 (exactitud insuficiente), R-04 (la referencia no es una verdad absoluta) y R-09 (poca disponibilidad de DJs). Decisiones relacionadas: OD-01 (RF-29 a Must), OD-04 (multi-motor) y OD-08 (este ADR).

## Contexto

El objetivo O7 del anteproyecto exige evaluar el sistema contrastando los descriptores estimados con los que proporciona Rekordbox sobre las mismas pistas y, si es posible, recogiendo la valoración de DJs reales. Los requisitos RNF-05 a RNF-09 definen las métricas y umbrales provisionales (P) y remiten a este ADR para el conjunto de evaluación.

Condicionantes ya establecidos en la memoria y en otros ADR:

- La referencia de Rekordbox es una estimación de otro sistema, no una verdad absoluta (capítulo 1, sección 1.4, y riesgo R-04).
- El conjunto de partida es la biblioteca personal del autor, con el sesgo de repertorio y de etiquetado que ello implica.
- La selección de la librería de análisis se hace con una prueba de concepto (ADR-003) y no debe contaminar la evaluación final.
- El audio tiene derechos de terceros y no puede publicarse en el repositorio (ADR-007).
- Los umbrales numéricos son provisionales y se ratifican tras la prueba de concepto.
- La disponibilidad de DJs para la valoración no está garantizada (R-09).

## Problema

Definir qué conjunto de pistas se usa para evaluar, cómo se obtiene la referencia, cómo se calculan y se informan las métricas, y cómo se valida el generador y la experiencia de uso, de forma reproducible, honesta sobre sus límites y legalmente correcta.

## 1. Conjunto de evaluación

### Alternativas consideradas

#### D1. Biblioteca personal completa del autor

**Ventajas:** máxima representatividad del uso real; sin esfuerzo de muestreo.

**Inconvenientes:** sesgo de repertorio sin controlar; coste de preparar la referencia de todas las pistas; imposible de publicar o reproducir por terceros; la referencia no es verdad absoluta.

---

#### D2. Muestra estratificada de la biblioteca personal, con referencia de Rekordbox

**Ventajas:** cumple O7 directamente; coste acotado; el muestreo documentado reduce el sesgo de selección; se puede publicar un manifiesto sin audio.

**Inconvenientes:** el sesgo de repertorio persiste; la referencia sigue siendo una estimación de Rekordbox.

---

#### D3. Conjunto público anotado de música electrónica como único conjunto

Conjuntos de tempo y tonalidad de EDM anotados a partir de correcciones de usuarios (Knees et al.), citados en la memoria [21].

**Ventajas:** reproducible por terceros; anotaciones independientes de Rekordbox; fuente externa.

**Inconvenientes:** no responde a O7, porque no contiene los valores de Rekordbox; menor representatividad del repertorio del autor; disponibilidad del audio y licencia por verificar.

---

#### D4. Combinación: D2 como conjunto principal y D3 como contraste

**Ventajas:** cumple O7 y añade una referencia independiente; permite discutir la validez de la referencia de Rekordbox; aumenta la reproducibilidad.

**Inconvenientes:** mayor coste de preparación; depende de la disponibilidad y licencia del conjunto público.

---

### Criterios de evaluación

| Criterio | Peso |
|-----------|------:|
| Cumplimiento del objetivo O7 (comparación con Rekordbox) | 5 |
| Representatividad del uso real | 5 |
| Validez de la referencia | 4 |
| Reproducibilidad | 4 |
| Coste de preparación | 3 |
| Control del sesgo | 4 |
| Aspectos legales (ADR-007) | 4 |

Escala de valoración: 1 (muy deficiente) a 5 (excelente). Total = Σ (Valoración × Peso).

### Evaluación (inicial y provisional)

| Criterio | Peso | D1 | D2 | D3 | D4 |
|---|---:|---:|---:|---:|---:|
| Cumplimiento de O7 | 5 | 5 (25) | 5 (25) | 2 (10) | 5 (25) |
| Representatividad | 5 | 5 (25) | 4 (20) | 2 (10) | 4 (20) |
| Validez de la referencia | 4 | 3 (12) | 3 (12) | 4 (16) | 4 (16) |
| Reproducibilidad | 4 | 2 (8) | 3 (12) | 5 (20) | 4 (16) |
| Coste de preparación | 3 | 2 (6) | 4 (12) | 4 (12) | 2 (6) |
| Control del sesgo | 4 | 2 (8) | 3 (12) | 4 (16) | 4 (16) |
| Aspectos legales | 4 | 3 (12) | 4 (16) | 3 (12) | 3 (12) |
| **Total** | | **96** | **109** | **96** | **111** |

La diferencia entre D4 y D2 (111 frente a 109) es pequeña. Como D3 depende de su disponibilidad y licencia, D2 es la base segura y D3 un complemento condicionado.

### Decisión propuesta: D4, con D2 como conjunto mínimo

La evaluación se realiza sobre D2. Si el conjunto público resulta accesible y su licencia lo permite, se añade como contraste. En caso contrario, la evaluación continúa solo con D2 y la memoria discute esa limitación.

## 2. Diseño de la muestra

| Aspecto | Propuesta |
|---|---|
| Unidad de análisis | La pista completa |
| Tamaño mínimo | 300 pistas (provisional). Con una proporción cercana al 85 %, el intervalo del 95 % tiene un semiancho aproximado de ±4 puntos. Se revisa con los tutores |
| Estratificación | Por género (etiquetas), rango de BPM y formato de fichero (MP3, WAV, FLAC, AIFF) |
| Selección | Aleatoria dentro de cada estrato, con semilla fija y documentada |
| Exclusiones | Se definen antes de evaluar y se cuentan: pistas sin referencia en Rekordbox, ficheros ilegibles y pistas con tempo variable que impidan una referencia única |
| Conjunto piloto | Un subconjunto distinto y disjunto de la muestra final, para elegir motor y ratificar umbrales |

### Separación entre selección y evaluación

La elección de motor en la prueba de concepto (ADR-003) y la ratificación de umbrales se hacen con el **conjunto piloto**. La evaluación final se hace con la **muestra reservada**, que no se ha usado para decidir. Así se evita ajustar el sistema o los umbrales a los datos con los que luego se mide.

## 3. Obtención de la referencia

| Paso | Descripción |
|---|---|
| 1 | Rekordbox analiza las pistas de la muestra con su propio análisis |
| 2 | El DJ exporta el XML de colección (RF-29b). Si no contuviera BPM o tonalidad, se prepara un CSV equivalente |
| 3 | El sistema importa la referencia y la asocia a las pistas de la muestra, dejando fuera las asociaciones ambiguas (CU-11, A2) |
| 4 | Se normaliza la notación de tonalidad de la referencia a la del sistema |
| 5 | Se registran la versión de Rekordbox y los ajustes de análisis que afecten a BPM y tonalidad |

La existencia de BPM y tonalidad en el XML de colección es un supuesto sin verificar (SRS 2.4). Su comprobación forma parte de la prueba de concepto.

## 4. Métricas de exactitud (RNF-05 a RNF-09)

| Métrica | Definición | Requisito |
|---|---|---|
| BPM estricto | Estimación dentro de ±4 % de la referencia | RNF-05 |
| BPM con octava | Idem, admitiendo los factores 2, 1/2, 3 y 1/3 | RNF-06 |
| Tonalidad exacta | Coincidencia de tónica y modo | RNF-07 |
| Tonalidad por compatibilidad | Código Camelot idéntico o mezclable con el de referencia según la regla básica | RNF-08 |
| Desglose de errores | Octava, relativa, quinta y otros | RNF-09 |
| Intervalo de confianza | Intervalo de Wilson al 95 % para cada proporción | RNF-09 |

Todas las métricas se calculan **por cada motor** y por estrato, y se almacenan como informe de evaluación con el motor y la versión (RF-07, RF-29).

### Criterio de cumplimiento

El umbral de un requisito se considera:

- **Cumplido** si el valor observado lo alcanza.
- **Confirmado** si además el límite inferior del intervalo lo alcanza.
- **No cumplido** en otro caso.

Los umbrales (P) se ratifican con el conjunto piloto antes de ejecutar la evaluación final, y su cambio se registra en el control de cambios del SRS.

### Contraste entre motores

La comparación entre dos motores sobre las mismas pistas es un contraste de proporciones apareadas. Se informa de las diferencias y de sus intervalos. Dada la muestra reducida, no se hacen afirmaciones más allá de lo que esos intervalos permitan.

### Auditoría manual opcional

Cuando el motor y Rekordbox discrepan, no se sabe cuál tiene razón. Se propone revisar auditivamente una submuestra de discrepancias para estimar qué parte corresponde a errores de cada sistema. Su tamaño depende del tiempo disponible.

## 5. Evaluación del generador (RNF-10, RNF-11, RNF-03, RNF-18)

| Medida | Descripción | Requisito |
|---|---|---|
| Cumplimiento de restricciones | Todas las transiciones de los setlists generados cumplen el salto de BPM y la política armónica | RNF-10 |
| Salto medio de BPM | Media de los saltos entre pistas consecutivas | RF-17 |
| Transiciones compatibles | Proporción de transiciones armónicamente compatibles | RF-17 |
| Fidelidad de géneros | Proporción de pistas que respetan el género asignado a su intervalo | RF-15 |
| Determinismo | Misma entrada, motor, parámetros y semilla producen el mismo setlist | RNF-11 |
| Detección de inviabilidad | Escenarios inviables por construcción devuelven un diagnóstico y no un setlist | RF-19 |
| Tiempo de generación | Percentil 95 para un setlist de 2 h sobre 5 000 pistas | RNF-03 |
| Escalado | Cociente de tiempos entre 10 000 y 5 000 pistas | RNF-18 |

**Escenarios.** Se define un conjunto fijo de escenarios con semillas: normales, con restricciones ajustadas, inviables por construcción y con anclas.

**Bibliotecas de escala.** La biblioteca del autor puede ser menor de 5 000 pistas. Para RNF-03 y RNF-18 se usan bibliotecas sintéticas de descriptores (sin audio), generadas a partir de la distribución observada, claramente identificadas como sintéticas en los resultados.

**Repetición.** Cada escenario de rendimiento se ejecuta varias veces (provisional: al menos 20) para informar de percentiles y no de medias.

## 6. Valoración por DJs y usabilidad (RNF-12, RNF-13)

| Aspecto | Propuesta |
|---|---|
| Participantes | Al menos 3 DJs (RNF-12). Si no es posible, se aplica el plan alternativo basado en métricas objetivas (R-09) |
| Coherencia | Escala de Likert de 1 a 5 sobre la coherencia de los setlists |
| Comparación | Valoración a ciegas de setlists generados frente a setlists de referencia formados por selección aleatoria con las mismas restricciones |
| Usabilidad | Cuestionario SUS y prueba de tarea de RNF-13 (primer setlist exportado en ≤ 10 min) |
| Análisis | Estadística descriptiva. Con muestras tan pequeñas no se hacen contrastes inferenciales |
| Privacidad | Cuestionario anónimo, con consentimiento informado y sin recogida de datos personales |

La comparación con una referencia aleatoria es una propuesta que refuerza la validez de la valoración, y debe consultarse con los tutores.

## 7. Verificación de la exportación (RF-23)

Se define un conjunto de setlists de prueba que incluya nombres con espacios, tildes y caracteres Unicode, rutas largas y ambos sistemas operativos. Cada importación en Rekordbox se registra con su resultado, la versión de Rekordbox y el sistema usado (ADR-006).

## 8. Reproducibilidad y tratamiento de datos

- Un **manifiesto del conjunto** versionado recoge, por pista, su identificador, su estrato y los valores derivados (BPM, tonalidad y referencia), sin audio.
- La semilla del muestreo, la versión de Rekordbox, las versiones de cada motor y los scripts de evaluación se versionan en el repositorio.
- El repositorio no contiene ficheros de audio (ADR-007). Los conjuntos públicos se usan respetando su licencia.
- Los resultados se almacenan como informes de evaluación con motor y versión (RF-07, RF-29).

## Decisión propuesta

1. Conjunto de evaluación D4: muestra estratificada de la biblioteca del autor como base y conjunto público como contraste condicionado.
2. Separación estricta entre conjunto piloto (selección de motor y ratificación de umbrales) y muestra reservada (evaluación final).
3. Métricas, intervalos y criterio de cumplimiento de las secciones 4 y 5.
4. Valoración por DJs anónima con comparación a ciegas, o plan alternativo si no hay participantes.
5. Manifiesto reproducible sin audio.

## Justificación

La combinación responde a O7 y reconoce los límites del conjunto de partida en lugar de ocultarlos. La separación entre piloto y muestra reservada evita ajustar el sistema a los datos de la evaluación. Los intervalos de confianza y la contrastación entre motores dan al capítulo 8 una base defendible aunque la muestra sea modesta.

## Consecuencias

### Positivas

- Una evaluación reproducible y defendible ante el tribunal.
- Los umbrales provisionales se ratifican con un procedimiento explícito y sin sesgo de selección.
- Cubre los capítulos 8.3 a 8.6 de la memoria.
- Las limitaciones (repertorio del autor, referencia no absoluta) quedan documentadas.

### Negativas

- Preparar la referencia y la muestra requiere tiempo en la fase de pruebas, que en el plan comparte calendario con la memoria (R-06).
- El tamaño de muestra es modesto y limita la potencia estadística.
- La valoración por DJs depende de participantes disponibles (R-09).
- Parte de la validez depende de que el XML de Rekordbox contenga BPM y tonalidad.

## Trazabilidad

| Elemento | Referencias |
|---|---|
| Requisitos funcionales | RF-23, RF-29, RF-29b |
| Requisitos no funcionales | RNF-01, RNF-02, RNF-03, RNF-05 a RNF-13, RNF-18 |
| Componentes | CMP-07 (evaluación) y CMP-04 (generador) |
| Casos de uso | CU-11 y CU-07 |
| Casos de prueba | T-RNF-05, T-CU11-01, T-CU11-02, T-RNF-10, T-RNF-11, T-RNF-03, T-RNF-18, T-RNF-12, T-RNF-13, T-CU07-04 |
| Decisiones abiertas | OD-01, OD-04, OD-08 |
| Riesgos | R-01, R-04, R-06, R-09 |

## Evidencias utilizadas

- Objetivo O7 del anteproyecto y requisitos RNF-05 a RNF-09 y RNF-12.
- Fundamentos de evaluación de la memoria (capítulo 3, secciones 3.2.3, 3.3.4 y 3.7).
- Limitaciones declaradas en la memoria (capítulo 1, sección 1.4).
- Conjuntos de datos públicos de tempo y tonalidad de EDM citados en la memoria [21].
- ADR-003 (prueba de concepto), ADR-006 (verificación de la importación) y ADR-007 (tratamiento legal del audio y de los datos).

## Impacto en el proyecto

- Convierte la validación experimental en una tarea con diseño propio, que debe planificarse con antelación.
- Obliga a separar el conjunto piloto de la muestra reservada desde el inicio de la prueba de concepto.
- Condiciona el modelo de datos: las referencias y los informes se almacenan con motor y versión (ADR-004).
- Exige definir un conjunto de escenarios y bibliotecas sintéticas para las pruebas de rendimiento.

## Impacto en la memoria

Guardar este contenido para la memoria del TFG.

- **Capítulo 1, sección 1.4:** limitaciones ya declaradas; coherentes con este ADR.
- **Capítulo 4, sección 4.6:** esta decisión permanece abierta hasta su validación.
- **Capítulo 8, secciones 8.3 a 8.7:** protocolo de evaluación, métricas, valoración por DJs y amenazas a la validez.
- **Apéndice C, secciones C.2 y C.3:** tratamiento del audio y de los datos de validación.
- **Apéndice B, sección B.2:** incluir este ADR.

Bloque reutilizable:

- **Contexto:** el objetivo O7 exige contrastar los descriptores con Rekordbox, cuya estimación no es una verdad absoluta, sobre una biblioteca personal sesgada.
- **Problema:** definir un conjunto y un protocolo de evaluación válidos, reproducibles y legalmente correctos.
- **Alternativas:** biblioteca completa, muestra estratificada, conjunto público y combinación.
- **Solución propuesta:** muestra estratificada de la biblioteca del autor con contraste de un conjunto público, separada del conjunto piloto.
- **Justificación:** mejor puntuación (111 frente a 109, 96 y 96) y cumplimiento de O7 con control del sesgo.
- **Ventajas:** evaluación reproducible, umbrales ratificados sin sesgo y limitaciones explícitas.
- **Limitaciones:** muestra modesta, dependencia de la calidad de la referencia y de los participantes.
- **Impacto:** exige planificar la evaluación y separar piloto y muestra final.

## Decisiones relacionadas

- ADR-001: Forma de Distribución del Sistema.
- ADR-002: Arquitectura General del Sistema.
- ADR-003: Motor de Análisis Musical.
- ADR-004: Persistencia.
- ADR-005: Algoritmo de Generación de Setlists.
- ADR-006: Exportación e Integración con Rekordbox.
- ADR-007: Licencias y compatibilidad legal (propuesto).
- ADR-008: Lenguaje, interfaz gráfica y empaquetado (propuesto).
- ADR-010: Identificación permanente de pistas (propuesto, OD-03).
