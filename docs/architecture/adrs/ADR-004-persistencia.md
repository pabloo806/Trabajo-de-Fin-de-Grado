# ADR-004: Persistencia

## Estado

Propuesto

## Contexto

La aplicación debe almacenar información sobre pistas, análisis realizados, setlists y configuraciones.

## Problema

Seleccionar el mecanismo de persistencia.

## Alternativas

- SQLite.
- PostgreSQL.
- Base de datos embebida alternativa.
- Almacenamiento en ficheros.

## Criterios de evaluación

- Facilidad de despliegue.
- Rendimiento.
- Complejidad operativa.
- Portabilidad.
- Escalabilidad.
- Soporte para consultas.
- Mantenibilidad.

## Decisión

Pendiente de evaluación.

## Justificación

Debe equilibrar simplicidad, despliegue, rendimiento y facilidad de mantenimiento.

## Consecuencias

Condicionará el modelo de datos y la capa de acceso a datos.
