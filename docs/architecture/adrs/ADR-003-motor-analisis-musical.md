# ADR-003: Motor de Análisis Musical

## Estado

Propuesto

## Contexto

SetlistGen requiere estimar BPM, tonalidad y código Camelot a partir de archivos de audio.

## Problema

Seleccionar la tecnología de análisis musical.

## Alternativas

- Librosa.
- Essentia.
- Madmom.
- Combinación de librerías.
- Desarrollo propio.

## Criterios de evaluación

- Exactitud de BPM.
- Exactitud de tonalidad.
- Compatibilidad con código Camelot.
- Rendimiento de procesamiento.
- Facilidad de integración.
- Calidad de la documentación.
- Actividad y mantenimiento de la librería.
- Compatibilidad de licencia.

## Evaluación de alternativas

| Criterio | Peso |
|-----------|------:|
| Exactitud BPM | 5 |
| Exactitud tonalidad | 5 |
| Rendimiento | 4 |
| Facilidad de integración | 4 |
| Documentación | 3 |
| Comunidad y mantenimiento | 3 |
| Compatibilidad de licencia | 3 |

## Matriz de decisión

| Alternativa | BPM | Tonalidad | Rendimiento | Integración | Documentación | Comunidad | Licencia | Total |
|------------|----:|----------:|------------:|------------:|--------------:|----------:|---------:|------:|
| Librosa | | | | | | | | |
| Essentia | | | | | | | | |
| Madmom | | | | | | | | |
| Combinación | | | | | | | | |

## Decisión final

Pendiente.

## Justificación

La decisión dependerá de los resultados de la prueba de concepto y de la comparación con Rekordbox.

## Consecuencias

Afectará a la precisión de las estimaciones y al rendimiento del sistema.
