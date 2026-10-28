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

## Evaluación de alternativas

| Criterio | Peso |
|-----------|------:|
| Facilidad de despliegue | 5 |
| Rendimiento | 4 |
| Complejidad operativa | 4 |
| Portabilidad | 4 |
| Escalabilidad | 3 |
| Soporte de consultas | 4 |
| Mantenimiento | 4 |

## Matriz de decisión

| Alternativa | Despliegue | Rendimiento | Complejidad | Portabilidad | Escalabilidad | Consultas | Mantenimiento | Total |
|------------|-----------:|------------:|------------:|-------------:|--------------:|----------:|---------------:|------:|
| SQLite | | | | | | | | |
| PostgreSQL | | | | | | | | |
| Ficheros | | | | | | | | |

## Decisión final

Pendiente.

## Justificación

Debe equilibrar simplicidad, despliegue, rendimiento y facilidad de mantenimiento.

## Consecuencias

Condicionará el modelo de datos y la capa de acceso a datos.
