# Decisiones Pendientes de Validación

## Objetivo

Este documento recopila las decisiones de diseño que permanecen abiertas tras la finalización de las fases de análisis de requisitos y diseño arquitectónico.

Su objetivo es facilitar la revisión con el tutor y el cotutor, permitiendo discutir de forma estructurada aquellos aspectos que condicionarán:

- El diseño del dominio.
- El modelo de datos.
- La persistencia SQLite.
- La implementación.
- La validación experimental.

---

# Estado actual

## Completado

✅ SRS consolidado.

✅ Casos de uso consolidados.

✅ Matriz de trazabilidad consolidada.

✅ Glosario consolidado.

✅ ADR-001 a ADR-006 aceptados.

✅ ADR-007 a ADR-010 propuestos.

✅ Arquitectura de alto nivel definida.

---

## Próximo hito

Diseño del modelo de dominio.

Diseño del modelo de datos.

Diseño físico SQLite.

---

# Resumen Ejecutivo

| ID | Decisión | Impacto | Prioridad | Estado |
|-----|-----------|----------|-----------|---------|
| OD-01 | RF-29 Should o Must | Validación experimental | Alta | Pendiente |
| OD-02 | Salto máximo BPM configurable | Generador y validación | Alta | Pendiente |
| OD-03 | Identidad permanente de pistas | Dominio y persistencia | Crítica | Pendiente |
| OD-04 | Persistencia multi-motor | Dominio y modelo de datos | Crítica | Pendiente |
| OD-05 | Entidad Library | Modelo de dominio | Alta | Pendiente |
| OD-06 | Persistencia de transiciones | Modelo de dominio y BD | Crítica | Pendiente |
| OD-07 | Validación del modelo de dominio | Dominio y persistencia | Crítica | Pendiente |
| OD-08 | Estado de ADR-007 a ADR-010 | Diseño detallado | Media | Pendiente |
| OD-09 | Motor MIR definitivo | Implementación futura | Media | Pendiente |
| OD-10 | Estrategia final de evaluación | Validación experimental | Media | Pendiente |

---

# Cuestiones a Tratar en la Próxima Reunión

## Bloque 1 · Requisitos

### P1. Evaluación experimental

¿Debe RF-29 pasar de Should a Must?

Contexto:

La evidencia principal del TFG depende de la comparación frente a Rekordbox.

Impacto:

- Requisitos.
- Casos de uso.
- Validación.
- Capítulo 8.

---

### P2. Salto máximo BPM

¿Debe existir un parámetro explícito que permita limitar el salto máximo de BPM entre pistas consecutivas?

Propuesta:

RF-13b.

Impacto:

- Generador.
- RNF-10.
- Validación de transiciones.

---

## Bloque 2 · Dominio

### P3. Identidad de las pistas

¿Es adecuada una estrategia de identificación en dos niveles?

Nivel 1:

- Ruta.
- Tamaño.
- Fecha.
- Huella rápida.

Nivel 2:

- Fingerprint acústico.

Impacto:

- RF-09.
- RF-09b.
- RF-09c.
- Persistencia.

---

### P4. Persistencia multi-motor

¿Debe permitirse almacenar múltiples resultados de análisis para una misma pista?

Relación propuesta:

```text
Track 1:N AnalysisResult
```

---

# Decisiones críticas para el inicio del modelo de datos

Las siguientes decisiones afectan directamente al diseño del dominio y de la persistencia:

- OD-03 · Identidad permanente de pistas.
- OD-04 · Persistencia multi-motor.
- OD-05 · Existencia de Library.
- OD-06 · Persistencia de transiciones.
- OD-07 · Modelo de dominio definitivo.

Estas decisiones deberían revisarse prioritariamente durante la próxima reunión con tutor y cotutor.

---

# OD-01 · Prioridad de la evaluación frente a Rekordbox

## Contexto

Actualmente RF-29 establece:

> El sistema permitirá contrastar los descriptores estimados con valores de referencia de Rekordbox para las mismas pistas y producirá un informe de discrepancias.

RF-29 estaba clasificado originalmente como requisito **Should**.

Sin embargo:

- RNF-05 depende de RF-29.
- RNF-06 depende de RF-29.
- RNF-07 depende de RF-29.
- RNF-08 depende de RF-29.
- RNF-09 depende de RF-29.

Además, el objetivo O7 del anteproyecto consiste precisamente en evaluar el sistema.

## Problema

La evidencia principal del TFG depende actualmente de un requisito funcional secundario.

## Alternativas

### A1. Mantener RF-29 como Should

#### Ventajas

- Menor alcance obligatorio.

#### Inconvenientes

- Debilita la validación experimental.

### A2. Promover RF-29 a Must

#### Ventajas

- Refleja la importancia real de la evaluación.
- Alinea requisitos funcionales y no funcionales.

#### Inconvenientes

- Incrementa el alcance mínimo del proyecto.

## Propuesta inicial

Promover RF-29 a Must.

## Estado

Pendiente de validación por tutor y cotutor.

---

# OD-02 · Gestión explícita del salto máximo de BPM

## Contexto

Actualmente el sistema permite definir:

- Duración objetivo.
- Rango BPM.
- Compatibilidad armónica.
- Progresión de géneros.
- Pistas ancladas.

RF-17 exige transiciones con saltos moderados de BPM.

RNF-10 exige que todas las restricciones configuradas se respeten.

Sin embargo, no existe definición formal de "salto moderado".

## Problema

La restricción no es verificable ni reproducible.

## Alternativas

### A1. Mantener la situación actual

El sistema interpreta internamente qué es un salto moderado.

#### Ventajas

- Menos opciones para el usuario.

#### Inconvenientes

- Difícil de validar.
- Ambiguo.

### A2. Configurar explícitamente un límite

Ejemplo:

```text
Salto máximo BPM = 5 BPM
```

#### Ventajas

- Completamente verificable.
- Más control para el DJ.

#### Inconvenientes

- Incrementa los parámetros de generación.

## Propuesta inicial

Crear RF-13b como requisito específico.

## Estado

Pendiente de validación por tutor y cotutor.

---

# OD-03 · Estrategia de identificación permanente de pistas

## Contexto

RF-09 exige que una pista conserve su identidad aunque:

- cambie de nombre,
- cambie de ubicación,
- sea reimportada.

Además:

- RF-09b exige evitar reanálisis.
- RNF-04 exige reescaneos rápidos.

ADR-010 propone una estrategia de identificación en dos niveles.

## Problema

Debe definirse el mecanismo definitivo de identificación de pistas.

## Alternativas

### A1. Hash completo del fichero

#### Ventajas

- Muy simple.

#### Inconvenientes

- Cambia al modificar etiquetas.

### A2. Hash del contenido de audio

#### Ventajas

- Independiente de los metadatos.

#### Inconvenientes

- Costoso para bibliotecas grandes.

### A3. Fingerprint acústico

#### Ventajas

- Diseñado para identificar música.

#### Inconvenientes

- Coste computacional elevado.

### A4. Identificación en dos niveles

Nivel 1:

```text
ruta
+
tamaño
+
fecha
+
huella rápida
```

Nivel 2:

```text
fingerprint acústico
```

solo cuando sea necesario.

#### Ventajas

- Compatible con RNF-04.
- Escalable.
- Robusto.

#### Inconvenientes

- Más complejo.

## Propuesta inicial

Estrategia de doble nivel propuesta en ADR-010.

## Estado

Pendiente de validación por tutor y cotutor.

---

# OD-04 · Persistencia multi-motor

## Contexto

La arquitectura contempla varios motores MIR:

- Essentia.
- Librosa.
- Madmom.

RF-07 exige almacenar:

- motor,
- versión,
- origen.

RF-29 exige comparación de resultados.

## Problema

Debe decidirse si una pista almacena uno o múltiples resultados.

## Alternativas

### A1. Un resultado por pista

#### Ventajas

- Modelo sencillo.

#### Inconvenientes

- No permite evaluación comparativa.

### A2. Múltiples resultados por pista

Relación:

```text
Track 1:N AnalysisResult
```

#### Ventajas

- Compatible con evaluación.
- Permite coexistencia de motores.
- Compatible con RF-07.

#### Inconvenientes

- Más complejidad.

## Propuesta inicial

Permitir múltiples resultados por pista.

## Estado

Pendiente de validación por tutor y cotutor.

---

# OD-05 · Existencia de la entidad Library

## Contexto

La aplicación trabaja sobre una colección musical local.

Debe decidirse si una biblioteca constituye una entidad explícita del dominio.

## Problema

Determinar si el sistema soportará múltiples bibliotecas o una única biblioteca por usuario.

## Alternativas

### A1. Mantener entidad Library

#### Ventajas

- Soporta múltiples bibliotecas.
- Mantiene histórico de importaciones.
- Facilita estadísticas.

#### Inconvenientes

- Incrementa complejidad.

### A2. Eliminar entidad Library

#### Ventajas

- Simplifica el modelo de dominio.

#### Inconvenientes

- Menor flexibilidad futura.

## Propuesta inicial

Mantener la entidad Library.

## Estado

Pendiente de validación por tutor y cotutor.

---

# OD-06 · Persistencia de transiciones

## Contexto

RF-17 exige evaluar transiciones.

RF-20 exige mostrar información asociada a cada transición.

Las transiciones contienen:

- Compatibilidad armónica.
- Salto BPM.
- Puntuación.
- Estado.

Sin embargo RF-20b permite modificar manualmente un setlist.

## Problema

Determinar si las transiciones deben persistirse o recalcularse.

## Alternativas

### A1. Recalcular dinámicamente

#### Ventajas

- Menor almacenamiento.
- Siempre coherente tras modificaciones.

#### Inconvenientes

- Menor trazabilidad.

### A2. Persistir explícitamente

#### Ventajas

- Facilita auditoría.
- Facilita análisis histórico.

#### Inconvenientes

- Riesgo de inconsistencias tras edición manual.

## Propuesta inicial

Pendiente de decisión.

## Estado

Pendiente de validación por tutor y cotutor.

---

# OD-07 · Modelo de dominio definitivo

## Objetivo

Validar si el conjunto de entidades propuesto representa correctamente el dominio del problema.

---

## Entidades propuestas

### Track

Representa una pista musical independiente de su ubicación.

Campos mínimos:

```text
track_id
fingerprint
status
created_at
```

---

### TrackLocation

Representa una ubicación física concreta.

Campos mínimos:

```text
location_id
track_id
file_path
last_seen_at
status
```

Permite gestionar:

- pistas movidas,
- pistas duplicadas,
- pistas ausentes.

---

### TrackMetadata

Representa metadatos obtenidos de etiquetas.

Campos mínimos:

```text
metadata_id
track_id

title
artist
genre
year
duration_seconds
```

---

### AnalysisRun

Representa una ejecución concreta de un motor MIR.

Campos mínimos:

```text
run_id

engine_name
engine_version

executed_at
```

---

### AnalysisResult

Resultado producido por un motor MIR.

Campos mínimos:

```text
analysis_id

track_id
run_id

bpm
key_tonic
key_mode
camelot_code

confidence
status
```

---

### GenerationRequest

Representa una solicitud de generación.

Campos mínimos:

```text
request_id

target_duration

bpm_min
bpm_max

harmonic_policy

random_seed
```

---

### GenreSegment

Define géneros por intervalos.

Campos mínimos:

```text
segment_id
request_id

start_time
end_time

genre
```

---

### Anchor

Representa una pista anclada.

Campos mínimos:

```text
anchor_id
request_id
track_id
position
```

---

### Setlist

Representa un setlist generado.

Campos mínimos:

```text
setlist_id
request_id

created_at

status
```

---

### SetlistTrack

Representa una pista perteneciente a un setlist.

Campos mínimos:

```text
setlist_id
track_id
position
```

---

### Transition

Representa una transición musical.

Campos mínimos:

```text
transition_id

from_track_id
to_track_id

bpm_delta
camelot_distance

transition_score
```

---

### ReferenceMeasurement

Representa datos procedentes de Rekordbox.

Campos mínimos:

```text
reference_id
track_id

bpm_reference
key_reference
camelot_reference
```

---

### EvaluationReport

Representa resultados experimentales agregados.

Campos mínimos:

```text
report_id

generated_at

bpm_accuracy
key_accuracy
camelot_accuracy
```

## Estado

Pendiente de validación por tutor y cotutor.

---

# OD-08 · Nuevos ADRs ya creados

## Estado

Resuelto.

Los siguientes ADR ya existen:

- ADR-007 Licencias y compatibilidad legal.
- ADR-008 Lenguaje, interfaz y empaquetado.
- ADR-009 Evaluación y validación experimental.
- ADR-010 Identificación permanente de pistas.

Se mantienen en estado Propuesto hasta su validación.

---

# Preguntas prioritarias para la próxima reunión

## Alta prioridad

1. ¿Debe RF-29 convertirse en Must?

2. ¿Debe existir un parámetro explícito de salto máximo BPM?

3. ¿Es adecuada la estrategia de identificación en dos niveles?

4. ¿Deben coexistir varios resultados por pista?

5. ¿Debe mantenerse la entidad Library?

6. ¿Las transiciones deben persistirse o recalcularse?

7. ¿Es correcto el conjunto de entidades propuesto para el dominio?

## Media prioridad

8. ¿Son necesarios ADR-007 a ADR-010?

9. ¿Es adecuada la estrategia de evaluación propuesta por ADR-009?

10. ¿Existen restricciones institucionales respecto a las licencias de dependencias?

---

# Resultado esperado de la reunión

Finalizar:

- OD-01
- OD-02
- OD-03
- OD-04
- OD-05
- OD-06
- OD-07

y obtener autorización para iniciar:

```text
docs/architecture/data-model.md
```

como siguiente entregable principal del proyecto.
