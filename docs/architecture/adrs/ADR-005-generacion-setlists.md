# ADR-005: Algoritmo de Generación de Setlists

## Estado

Propuesto

## Contexto

El sistema debe construir secuencias de pistas que satisfagan restricciones de duración, BPM, compatibilidad armónica y género.

## Problema

Seleccionar la estrategia de generación de setlists.

## Alternativas

- Algoritmo voraz.
- Búsqueda con restricciones.
- Beam Search.
- Metaheurísticas.
- Estrategia híbrida.

## Criterios de evaluación

- Calidad musical del resultado.
- Cumplimiento de restricciones.
- Tiempo de ejecución.
- Escalabilidad frente al tamaño de la biblioteca.
- Determinismo.
- Facilidad de implementación.
- Facilidad de validación.

## Evaluación de alternativas

| Criterio | Peso |
|-----------|------:|
| Calidad del resultado | 5 |
| Cumplimiento de restricciones | 5 |
| Tiempo de ejecución | 4 |
| Escalabilidad | 4 |
| Determinismo | 4 |
| Facilidad de implementación | 3 |
| Facilidad de validación | 3 |

## Matriz de decisión

| Alternativa | Calidad | Restricciones | Rendimiento | Escalabilidad | Determinismo | Implementación | Validación | Total |
|------------|---------:|--------------:|------------:|--------------:|-------------:|---------------:|-----------:|------:|
| Voraz | | | | | | | | |
| CSP / Restricciones | | | | | | | | |
| Beam Search | | | | | | | | |
| Metaheurística | | | | | | | | |

## Decisión final

Pendiente.

## Justificación

La solución debe equilibrar calidad del resultado y coste computacional.

## Consecuencias

Afectará al rendimiento y a la calidad musical de los setlists generados.
