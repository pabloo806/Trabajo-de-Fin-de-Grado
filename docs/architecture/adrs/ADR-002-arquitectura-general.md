# ADR-002: Arquitectura General del Sistema

## Estado

Propuesto

## Contexto

El sistema deberá organizarse de forma que la lógica de negocio no dependa de tecnologías concretas.

## Problema

Determinar el estilo arquitectónico del sistema.

## Alternativas

- Arquitectura en capas.
- Arquitectura limpia (Clean Architecture).
- Arquitectura hexagonal.
- Monolito tradicional.

## Criterios de evaluación

- Separación de responsabilidades.
- Facilidad de pruebas.
- Mantenibilidad.
- Escalabilidad.
- Independencia tecnológica.
- Curva de aprendizaje.
- Compatibilidad con los requisitos RNF-22, RNF-23 y RNF-24.

## Evaluación de alternativas

| Criterio | Peso |
|-----------|------:|
| Separación de responsabilidades | 5 |
| Testabilidad | 5 |
| Mantenibilidad | 5 |
| Escalabilidad | 3 |
| Curva de aprendizaje | 2 |
| Independencia tecnológica | 5 |

## Matriz de decisión

| Alternativa | Separación | Testabilidad | Mantenibilidad | Escalabilidad | Curva | Independencia | Total |
|------------|-----------:|-------------:|---------------:|--------------:|------:|--------------:|------:|
| Arquitectura en capas | | | | | | | |
| Clean Architecture | | | | | | | |
| Hexagonal | | | | | | | |
| Monolito tradicional | | | | | | | |

## Decisión final

Pendiente.

## Justificación

La decisión depende de la forma de distribución seleccionada y de los requisitos de mantenibilidad y testabilidad.

## Consecuencias

Influirá en la organización de paquetes, módulos y dependencias.
