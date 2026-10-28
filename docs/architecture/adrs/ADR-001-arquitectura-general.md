# ADR-001: Arquitectura General del Sistema

## Estado

Propuesto

## Contexto

SetlistGen debe permitir importar una biblioteca musical local, analizar las pistas, almacenar los resultados y generar setlists exportables a Rekordbox.

El sistema debe mantenerse desacoplado de las tecnologías concretas para facilitar cambios futuros.

## Problema

Determinar la arquitectura de alto nivel que permita evolucionar el sistema sin acoplar la lógica de negocio a la interfaz, la persistencia o las librerías de análisis musical.

## Alternativas

- Arquitectura en capas tradicional.
- Arquitectura limpia (Clean Architecture).
- Arquitectura hexagonal.
- Arquitectura monolítica sin separación formal.

## Decisión

Pendiente de evaluación.

## Justificación

Se evaluará tras la prueba de concepto y durante el diseño detallado.

## Consecuencias

La decisión condicionará la organización de paquetes, la mantenibilidad y la facilidad de sustitución de componentes.
