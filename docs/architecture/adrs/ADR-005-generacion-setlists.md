# ADR-005: Algoritmo de Generación de Setlists

## Estado

Aceptado (revisado el 2026-10-30). La **formulación** (satisfacción de restricciones con función de coste) está aceptada. La **estrategia de búsqueda** concreta debe validarse con un prototipo y el benchmark de RNF-03.

## Fecha

2026-10-28 (decisión original) · 2026-10-30 (revisión de alineación con la línea base documental)

## Requisitos relacionados

| Requisito | Relación |
|---|---|
| RF-10 | Persistencia del setlist con sus parámetros y su semilla |
| RF-12 | Duración total con tolerancia (por defecto ±5 %) |
| RF-13, RF-13b | Rango de BPM y salto máximo de BPM entre pistas consecutivas **[PROPUESTA · OD-02]** |
| RF-14 | Política de compatibilidad armónica |
| RF-15, RF-16 | Progresión de géneros y pistas ancladas |
| RF-17 | Orden de reproducción que respete las restricciones y minimice una función de coste |
| RF-18 | Ausencia de repeticiones |
| RF-19 | Detección y explicación de la inviabilidad |
| RF-20 | Evaluación de cada transición |
| RNF-03 | Setlist de 2 h sobre 5 000 pistas en ≤ 60 s, percentil 95 (P) |
| RNF-10 | 100 % de las transiciones de un setlist generado cumplen las restricciones |
| RNF-11 | Determinismo |
| RNF-18 | Crecimiento aproximadamente lineal del tiempo con el tamaño de la biblioteca (P) |

Hallazgos atendidos: H-03 (reformular las restricciones de este ADR), H-04 (salto máximo de BPM), N-07 (ubicación del solver y coherencia con el SRS) y riesgo R-07.

## Contexto

SetlistGen tiene como objetivo generar automáticamente setlists a partir de una biblioteca musical local.

Cada setlist debe satisfacer un conjunto de restricciones definidas por el DJ:

- Duración objetivo.
- Rango de BPM.
- Salto máximo de BPM entre pistas consecutivas.
- Compatibilidad armónica.
- Progresión de géneros.
- Pistas ancladas.
- Ausencia de repeticiones.

Además, el sistema debe:

- Generar resultados reproducibles (RNF-11).
- Ser capaz de explicar si no existe solución (RF-19).
- Mantener tiempos de generación razonables (RNF-03).
- Escalar a bibliotecas de varios miles de pistas (RNF-18).

El SRS y la memoria (ecuaciones 3.7 a 3.11) formulan el problema como una optimización: entre las secuencias factibles se busca la de menor coste. Este ADR se alinea con esa formulación.

## Problema

Determinar la estrategia de generación de setlists que mejor equilibre calidad musical, cumplimiento de restricciones y rendimiento.

## Alternativas consideradas

### A1. Algoritmo voraz (Greedy)

Construcción secuencial de la lista seleccionando en cada paso la mejor pista disponible según una función de puntuación.

#### Ventajas

- Implementación sencilla.
- Muy rápido.
- Fácil de depurar.

#### Inconvenientes

- Puede quedar atrapado en óptimos locales.
- No considera el impacto futuro de las decisiones.
- Difícil detectar situaciones sin solución.

---

### A2. Búsqueda basada en restricciones (Constraint Satisfaction Problem)

Modelar el problema como un conjunto de variables y restricciones que deben cumplirse simultáneamente.

#### Ventajas

- Garantiza el cumplimiento de restricciones.
- Detecta soluciones inviables.
- Facilita justificar el resultado.
- Encaja con la naturaleza del problema.

#### Inconvenientes

- Mayor complejidad de implementación.
- Coste computacional superior.

---

### A3. Beam Search

Explora simultáneamente varias soluciones parciales y conserva únicamente las más prometedoras.

#### Ventajas

- Mejor calidad que un algoritmo voraz.
- Escalable mediante control del ancho del haz.
- Buen equilibrio entre calidad y coste.

#### Inconvenientes

- No garantiza optimalidad.
- Requiere parametrización.
- No demuestra la inviabilidad.

---

### A4. Metaheurísticas

Algoritmos como recocido simulado, algoritmos genéticos o búsqueda tabú.

#### Ventajas

- Capaces de explorar espacios muy grandes.
- Buenos resultados en problemas complejos.

#### Inconvenientes

- Mayor complejidad.
- Menor determinismo.
- Difíciles de justificar académicamente para este alcance.

---

## Criterios de evaluación

| Criterio | Peso |
|-----------|------:|
| Cumplimiento de restricciones | 5 |
| Calidad musical | 5 |
| Determinismo | 4 |
| Detección de inviabilidad | 5 |
| Escalabilidad | 4 |
| Facilidad de implementación | 3 |
| Facilidad de validación | 4 |

### Escala de valoración

| Valor | Significado |
|--------|-------------|
| 1 | Muy deficiente |
| 2 | Deficiente |
| 3 | Aceptable |
| 4 | Bueno |
| 5 | Excelente |

### Método de cálculo

La puntuación ponderada de cada criterio se calcula como:

```text
Puntuación ponderada = Valoración × Peso
```

La puntuación total de cada alternativa se calcula como:

```text
Total = Σ (Valoración × Peso)
```

---

## Evaluación de alternativas

### Algoritmo voraz

| Criterio | Peso | Valoración | Resultado |
|-----------|------:|-----------:|----------:|
| Restricciones | 5 | 2 | 10 |
| Calidad musical | 5 | 3 | 15 |
| Determinismo | 4 | 5 | 20 |
| Detección de inviabilidad | 5 | 2 | 10 |
| Escalabilidad | 4 | 5 | 20 |
| Implementación | 3 | 5 | 15 |
| Validación | 4 | 4 | 16 |

**Total: 106**

---

### CSP (Constraint Satisfaction Problem)

| Criterio | Peso | Valoración | Resultado |
|-----------|------:|-----------:|----------:|
| Restricciones | 5 | 5 | 25 |
| Calidad musical | 5 | 4 | 20 |
| Determinismo | 4 | 5 | 20 |
| Detección de inviabilidad | 5 | 5 | 25 |
| Escalabilidad | 4 | 3 | 12 |
| Implementación | 3 | 3 | 9 |
| Validación | 4 | 5 | 20 |

**Total: 131**

---

### Beam Search

| Criterio | Peso | Valoración | Resultado |
|-----------|------:|-----------:|----------:|
| Restricciones | 5 | 4 | 20 |
| Calidad musical | 5 | 5 | 25 |
| Determinismo | 4 | 4 | 16 |
| Detección de inviabilidad | 5 | 3 | 15 |
| Escalabilidad | 4 | 4 | 16 |
| Implementación | 3 | 3 | 9 |
| Validación | 4 | 4 | 16 |

**Total: 117**

---

### Metaheurísticas

| Criterio | Peso | Valoración | Resultado |
|-----------|------:|-----------:|----------:|
| Restricciones | 5 | 4 | 20 |
| Calidad musical | 5 | 5 | 25 |
| Determinismo | 4 | 2 | 8 |
| Detección de inviabilidad | 5 | 3 | 15 |
| Escalabilidad | 4 | 5 | 20 |
| Implementación | 3 | 1 | 3 |
| Validación | 4 | 2 | 8 |

**Total: 99**

Los cuatro totales se han verificado y no se modifican en esta revisión.

---

## Decisión

Se adopta una estrategia basada en **satisfacción de restricciones (Constraint Satisfaction Problem, CSP)**, con una **función de coste** que ordena las soluciones válidas. Formalmente, el problema es de optimización con restricciones (COP): las restricciones son obligatorias y el coste se minimiza entre las soluciones que las cumplen.

El generador construirá los setlists como soluciones válidas a un conjunto explícito de restricciones derivadas de los parámetros introducidos por el DJ.

## Restricciones del problema

Esta sección reformula las restricciones de la versión 1.0 (hallazgo H-03). Todas son **obligatorias**: una solución que incumpla una de ellas no es válida (RNF-10).

| ID | Restricción | Requisito | Equivalente en v1.0 |
|---|---|---|---|
| R1 | Ninguna pista aparece más de una vez | RF-18 | R1 |
| R2 | El BPM de toda pista está dentro del rango definido | RF-13 | R2 |
| R3 | El salto de BPM entre pistas consecutivas no supera el máximo configurado **[PROPUESTA · OD-02]** | RF-13b | Nueva |
| R4 | Cada transición cumple la política de compatibilidad armónica configurada | RF-14 | R3 |
| R5 | La duración total está dentro de la tolerancia respecto al objetivo (por defecto ±5 %) | RF-12 | R4 |
| R6 | Cada pista anclada ocupa su posición | RF-16 | R5 |
| R7 | Las pistas de cada intervalo pertenecen al género asignado a ese intervalo | RF-15 | R6 |

### Aclaraciones de diseño

Estas aclaraciones son supuestos de diseño que deben confirmarse al implementar:

- **Candidatas.** Solo participan las pistas con resultados válidos del motor activo y con una ubicación disponible. Las pistas ausentes o con análisis fallido quedan fuera.
- **Pistas ancladas.** Una pista anclada también debe cumplir R2, R3, R4 y R7 respecto a sus vecinas. Si no puede, se informa como conflicto (RF-19), no se relaja la restricción.
- **Intervalos de género.** Una pista pertenece a un intervalo según el instante en que empieza su reproducción. Las pistas sin género no pueden ocupar un intervalo con género asignado.
- **Restricciones opcionales.** R6 y R7 solo se aplican si el DJ define anclas o una progresión de géneros (RF-15 y RF-16 son Should).

## Función de coste

Entre las soluciones válidas se minimiza una función de coste formada por penalizaciones de las transiciones:

```text
J(s) = Σ [ α · |salto de BPM| + β · disonancia armónica + γ · incoherencia de género ]
```

- `α`, `β` y `γ` son pesos no negativos, configurables y con valores por defecto fijados en la validación.
- La disonancia armónica es una medida más fina que la compatibilidad binaria, por ejemplo basada en la distancia Camelot.
- La forma concreta de cada término se define en el diseño del dominio (capítulo 6 de la memoria).

La misma evaluación de transición se utiliza para el coste y para la información que se muestra al DJ (RF-20).

## Estrategia de búsqueda prevista

La formulación como CSP indica *qué* se resuelve. La estrategia de búsqueda que lo resuelve debe validarse con un prototipo y el benchmark de RNF-03.

| Elemento | Diseño previsto |
|---|---|
| Reducción previa | Filtrado de candidatas por rango de BPM, género y disponibilidad antes de buscar |
| Búsqueda | Búsqueda con retroceso y propagación de restricciones, con orden de selección guiado por la función de coste |
| Límite de esfuerzo | Número máximo de nodos explorados (determinista) y, como seguridad, un límite de tiempo de reloj |
| Resultado parcial | Si se agota el límite habiendo encontrado una solución válida, se devuelve la mejor encontrada y se indica que no se ha probado que sea óptima |
| Solución de repliegue | Si el benchmark demuestra que no se cumple RNF-03, la búsqueda puede sustituirse por Beam Search conservando el modelo de restricciones y su validación (riesgo R-07) |

### Determinismo (RNF-11)

El resultado debe ser idéntico para los mismos datos, parámetros, motor activo y semilla. Por ello:

- Las candidatas se ordenan de forma estable por su identificador antes de buscar.
- La semilla solo se utiliza para desempatar entre opciones de igual coste, nunca para introducir aleatoriedad que no se pueda reproducir.
- El límite de la búsqueda se expresa en nodos explorados y no en tiempo, porque un límite de reloj produciría resultados distintos en equipos de distinta velocidad.
- Si se activa el límite de reloj de seguridad, el resultado no se garantiza reproducible y el sistema lo indica.

## Diagnóstico de inviabilidad (RF-19)

Cuando no se encuentra ninguna solución, el sistema distingue dos casos:

| Caso | Condición | Mensaje |
|---|---|---|
| Inviabilidad demostrada | La búsqueda ha agotado el espacio de soluciones o una comprobación previa demuestra la imposibilidad | Se informa de, al menos, un subconjunto de restricciones en conflicto |
| Límite agotado | Se alcanza el límite de esfuerzo sin solución ni demostración | Se informa de que no se ha encontrado solución en el límite, sin afirmar que no exista |

Para identificar el subconjunto en conflicto, el sistema aplica primero comprobaciones baratas y después un análisis de relajación:

1. **Comprobaciones previas:** las candidatas no cubren la duración objetivo; un intervalo de género no tiene candidatas; las anclas incumplen R2 a R4 o son incompatibles entre sí; el rango de BPM y el salto máximo no admiten ninguna cadena.
2. **Análisis de relajación:** se repite la comprobación de viabilidad eliminando restricciones de una en una, para determinar qué conjunto las hace incompatibles.

No se genera ni se almacena ningún setlist inválido.

## Ubicación del resolutor

El resolutor puede ser propio o apoyarse en una librería externa de resolución de restricciones.

| Opción | Dónde reside | Condiciones |
|---|---|---|
| Resolutor propio | Dominio, como servicio de dominio | No añade dependencias; requiere implementar la búsqueda y la propagación |
| Librería externa | Tras un puerto de Aplicación (RNF-22) | Debe superar la revisión de licencia (ADR-007) y ser sustituible (RNF-23) |

Se prevé comenzar con un resolutor propio, porque las restricciones son específicas de la secuencia de pistas. Si el prototipo no cumple RNF-03, se evaluará una librería externa, con un puerto nuevo y una revisión de este ADR.

## Justificación

El problema planteado por SetlistGen es esencialmente un problema de restricciones.

Los DJs especifican condiciones que deben cumplirse simultáneamente y el sistema debe encontrar una secuencia válida o informar de la imposibilidad de hacerlo.

La formulación CSP permite:

- Representar explícitamente las restricciones.
- Justificar los resultados.
- Detectar conflictos entre requisitos.
- Cumplir los requisitos funcionales del proyecto.

La función de coste resuelve la existencia de varias soluciones válidas y es coherente con la formulación de optimización de la memoria.

Además, proporciona una base sólida para la evaluación experimental descrita en el capítulo de validación.

## Consecuencias

### Positivas

- Cumplimiento riguroso de restricciones.
- Resultados reproducibles.
- Detección de soluciones inviables, con explicación.
- Trazabilidad entre requisitos y algoritmo.
- Las restricciones se pueden verificar de forma independiente del algoritmo, mediante pruebas de propiedades (RNF-10).

### Negativas

- Mayor complejidad inicial.
- Coste computacional superior a un algoritmo voraz, con riesgo sobre RNF-03 y RNF-18.
- Necesidad de diseñar correctamente las restricciones y los pesos de la función de coste.
- El límite de esfuerzo determinista complica el ajuste del tiempo de respuesta percibido por el DJ.
- El análisis de relajación para explicar los conflictos aumenta el coste de los casos sin solución.

## Trazabilidad

| Elemento | Referencias |
|---|---|
| Requisitos funcionales | RF-10, RF-12 a RF-20 |
| Requisitos no funcionales | RNF-03, RNF-10, RNF-11, RNF-18 |
| Componentes | CMP-04 (generador de setlists) |
| Casos de prueba | T-CU05-01 a T-CU05-06, T-RNF-03, T-RNF-10, T-RNF-11, T-RNF-18 |
| Decisiones abiertas | OD-02 (salto máximo), OD-06 (transiciones) |
| Riesgos | R-07 |

## Evidencias utilizadas

- Requisitos funcionales de generación de setlists (RF-12 a RF-19).
- Restricciones musicales definidas en la especificación y formulación de la memoria (ecuaciones 3.7 a 3.11).
- Necesidad de validar objetivamente los resultados (RNF-10).
- Necesidad de resultados reproducibles (RNF-11) y de rendimiento acotado (RNF-03, RNF-18).
- Necesidad de justificar académicamente el comportamiento del generador.
- Hallazgos H-03, H-04 y N-07.

## Impacto en el proyecto

- Fija el conjunto de restricciones R1 a R7, que sustituye al de la versión 1.0 y debe usarse en el modelo de dominio, los casos de prueba y la memoria.
- Convierte el prototipo del generador y el benchmark de RNF-03 en una validación temprana, necesaria para confirmar la estrategia de búsqueda.
- Requiere definir la función de coste y sus pesos, que se validan con la evaluación experimental.
- Condiciona el modelo de datos: la solicitud de generación almacena la semilla y los parámetros (RF-10), y las transiciones pueden persistirse (OD-06).
- Puede requerir una revisión de este ADR si se adopta una librería externa.

## Impacto en la memoria

Guardar este contenido para la memoria del TFG.

- **Capítulo 3, sección 3.5:** ya anticipa la formulación y deja la elección del algoritmo a un ADR; este ADR la resuelve.
- **Capítulo 4, sección 4.6:** el algoritmo de generación deja de figurar como decisión abierta.
- **Capítulo 6, sección 6.5:** diseño del generador, con restricciones R1 a R7, función de coste y diagnóstico de conflictos.
- **Capítulo 7, sección 7.6:** implementación de la búsqueda.
- **Capítulo 8, sección 8.4:** evaluación del generador, con las pruebas de RNF-03, RNF-10, RNF-11 y RNF-18.
- **Apéndice B, sección B.2:** incluir este ADR.

Bloque reutilizable:

- **Contexto:** el DJ define restricciones simultáneas (duración, BPM, armonía, géneros, anclas) y espera un setlist que las cumpla o una explicación de por qué no es posible.
- **Problema:** elegir la estrategia que equilibre cumplimiento de restricciones, calidad musical y rendimiento.
- **Alternativas:** algoritmo voraz, CSP, Beam Search y metaheurísticas.
- **Solución adoptada:** CSP con función de coste (COP), con siete restricciones obligatorias.
- **Justificación:** mayor puntuación (131 frente a 117, 106 y 99) y capacidad de detectar y explicar la inviabilidad.
- **Ventajas:** cumplimiento riguroso, reproducibilidad y trazabilidad entre requisitos y algoritmo.
- **Limitaciones:** mayor coste computacional y necesidad de validar el rendimiento con un benchmark.
- **Impacto:** condiciona el modelo de dominio, los datos persistidos y las pruebas de propiedades.

## Decisiones relacionadas

- ADR-001: Forma de Distribución del Sistema.
- ADR-002: Arquitectura General del Sistema.
- ADR-003: Motor de Análisis Musical.
- ADR-004: Persistencia.
- ADR-006: Exportación e Integración con Rekordbox.
- ADR-007: Licencias y compatibilidad legal (propuesto).
- ADR-008: Lenguaje, interfaz gráfica y empaquetado (propuesto).
- ADR-009: Dataset y protocolo de evaluación (propuesto).
- ADR-010: Identificación permanente de pistas (propuesto, OD-03).

## Cambios respecto a la versión original (2026-10-28)

| Cambio | Motivo |
|---|---|
| Restricciones reformuladas de R1-R6 a R1-R7, con salto máximo de BPM (R3) y requisitos asociados | H-03, H-04 y RF-13b |
| Decisión precisada como CSP con función de coste (COP) | Coherencia con RF-17 y la formulación de la memoria |
| Función de coste con los tres términos y sus pesos | La v1.0 solo enumeraba los criterios |
| Estrategia de búsqueda, límite de esfuerzo y solución de repliegue | RNF-03 y riesgo R-07 |
| Determinismo: límite de esfuerzo en nodos y no en tiempo | RNF-11 |
| Diagnóstico de inviabilidad: distinción entre inviabilidad demostrada y límite agotado | RF-19 |
| Ubicación del resolutor: propio en el dominio o librería tras un puerto | Hallazgo N-07 y RNF-22 |
| Requisitos, trazabilidad, impactos y decisiones ADR-007 a ADR-010 | Formato obligatorio de ADR |

Las puntuaciones y los totales no se modifican.
