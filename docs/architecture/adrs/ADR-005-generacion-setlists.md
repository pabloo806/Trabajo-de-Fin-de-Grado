# ADR-005: Algoritmo de Generación de Setlists

## Estado

Aceptado

## Fecha

2026-10-28

## Contexto

SetlistGen tiene como objetivo generar automáticamente setlists a partir de una biblioteca musical local.

Cada setlist debe satisfacer un conjunto de restricciones definidas por el DJ:

- Duración objetivo.
- Rango de BPM.
- Compatibilidad armónica.
- Progresión de géneros.
- Pistas ancladas.
- Ausencia de repeticiones.

Además, el sistema debe:

- Generar resultados reproducibles.
- Ser capaz de explicar si no existe solución.
- Mantener tiempos de generación razonables.
- Escalar a bibliotecas de varios miles de pistas.

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

---

## Decisión

Se adopta una estrategia basada en **satisfacción de restricciones (Constraint Satisfaction Problem, CSP)**.

El generador construirá los setlists como soluciones válidas a un conjunto explícito de restricciones derivadas de los parámetros introducidos por el DJ.

## Diseño previsto

Las restricciones mínimas serán:

```text
R1. No repetir pistas.

R2. Respetar rango BPM.

R3. Respetar compatibilidad Camelot.

R4. Respetar duración objetivo.

R5. Respetar pistas ancladas.

R6. Respetar progresión de géneros.
```

En caso de existir múltiples soluciones válidas, se aplicará una función de coste para priorizar:

```text
- Menor salto BPM.
- Mayor coherencia armónica.
- Mayor coherencia de género.
```

## Justificación

El problema planteado por SetlistGen es esencialmente un problema de restricciones.

Los DJs especifican condiciones que deben cumplirse simultáneamente y el sistema debe encontrar una secuencia válida o informar de la imposibilidad de hacerlo.

La formulación CSP permite:

- Representar explícitamente las restricciones.
- Justificar los resultados.
- Detectar conflictos entre requisitos.
- Cumplir los requisitos funcionales del proyecto.

Además, proporciona una base sólida para la evaluación experimental descrita en el capítulo de validación.

## Consecuencias

### Positivas

- Cumplimiento riguroso de restricciones.
- Resultados reproducibles.
- Detección de soluciones inviables.
- Trazabilidad entre requisitos y algoritmo.

### Negativas

- Mayor complejidad inicial.
- Coste computacional superior a un algoritmo voraz.
- Necesidad de diseñar correctamente las restricciones.

## Evidencias utilizadas

- Requisitos funcionales de generación de setlists.
- Restricciones musicales definidas en la especificación.
- Necesidad de validar objetivamente los resultados.
- Necesidad de justificar académicamente el comportamiento del generador.

## Decisiones relacionadas

- ADR-001: Forma de Distribución del Sistema.
- ADR-002: Arquitectura General del Sistema.
- ADR-003: Motor de Análisis Musical.
- ADR-004: Persistencia.
- ADR-006: Exportación e Integración con Rekordbox.
