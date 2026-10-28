# ADR-001: Forma de Distribución del Sistema

## Estado

Propuesto

## Contexto

SetlistGen debe asistir al DJ en la preparación de setlists a partir de una biblioteca musical local y permitir la exportación hacia Rekordbox.

Actualmente no se ha decidido el modo de distribución de la aplicación.

## Problema

Determinar cómo se ejecutará SetlistGen.

## Alternativas

- Aplicación de escritorio.
- Aplicación web local.
- Complemento o integración con Rekordbox.
- Aplicación híbrida.

## Criterios de evaluación

- Facilidad de acceso a la biblioteca musical local.
- Experiencia de usuario para DJs.
- Compatibilidad con Windows y macOS.
- Complejidad de despliegue.
- Mantenibilidad.
- Posibilidad de crecimiento futuro.
- Integración con Rekordbox.

## Evaluación de alternativas

| Criterio | Peso |
|-----------|------:|
| Acceso a archivos locales | 5 |
| Experiencia de usuario | 5 |
| Complejidad de desarrollo | 4 |
| Portabilidad | 4 |
| Integración con Rekordbox | 5 |
| Mantenibilidad | 4 |
| Escalabilidad futura | 3 |

### Matriz de decisión

| Alternativa | Archivos | UX | Complejidad | Portabilidad | Rekordbox | Mantenibilidad | Evolución | Total |
|------------|----------:|---:|------------:|-------------:|-----------:|---------------:|----------:|------:|
| Escritorio | | | | | | | | |
| Web local | | | | | | | | |
| Plugin Rekordbox | | | | | | | | |

## Decisión final

Pendiente.

## Justificación

La decisión condicionará la arquitectura, la experiencia de usuario, la persistencia y las tecnologías utilizadas.

## Consecuencias

La solución elegida servirá de base para el resto de decisiones arquitectónicas.
