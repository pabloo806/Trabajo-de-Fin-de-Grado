# Decisiones Pendientes de Validación

## Objetivo

Este documento recopila las decisiones de diseño que permanecen abiertas tras la finalización de las fases de análisis de requisitos y diseño arquitectónico.

Su objetivo es facilitar la revisión con el tutor y el cotutor, permitiendo discutir de forma estructurada aquellos aspectos que condicionarán el diseño detallado, la implementación y la validación experimental del proyecto.

---

# OD-01 · Prioridad de la evaluación frente a Rekordbox

## Contexto

Actualmente el requisito RF-29 establece:

> El sistema permitirá contrastar los descriptores estimados con valores de referencia de Rekordbox para las mismas pistas y producirá un informe de discrepancias.

RF-29 está clasificado actualmente como requisito **Should**.

Sin embargo, los siguientes requisitos no funcionales dependen directamente de dicho mecanismo de evaluación:

- RNF-05: Exactitud estricta de BPM.
- RNF-06: Exactitud BPM permitiendo errores de octava.
- RNF-07: Exactitud exacta de tonalidad.
- RNF-08: Exactitud de tonalidad según compatibilidad Camelot.
- RNF-09: Transparencia y análisis de errores.

Adicionalmente, uno de los objetivos específicos del proyecto consiste en evaluar los descriptores obtenidos por el sistema frente a los valores proporcionados por Rekordbox.

## Problema

Existe una posible incoherencia entre la importancia académica de la evaluación experimental y la prioridad asignada al requisito funcional que permite realizar dicha evaluación.

## Alternativas

### A1. Mantener RF-29 como Should

#### Ventajas

- Mantiene la clasificación original del SRS.
- Reduce alcance obligatorio.

#### Inconvenientes

- La evidencia principal del TFG depende de una funcionalidad secundaria.
- Dificulta justificar la validación experimental.

### A2. Promover RF-29 a Must

#### Ventajas

- Refleja la importancia de la validación dentro del proyecto.
- Alinea los requisitos funcionales con los requisitos no funcionales asociados.

#### Inconvenientes

- Incrementa el alcance mínimo obligatorio.

## Propuesta inicial

Promover RF-29 a requisito Must.

## Pendiente de validación

Tutor y cotutor.

---

# OD-02 · Gestión explícita del salto máximo de BPM

## Contexto

Actualmente el sistema permite definir:

- Duración objetivo del setlist.
- Rango de BPM.
- Compatibilidad armónica.
- Progresión de géneros.
- Pistas ancladas.

RF-17 establece que las transiciones deben presentar saltos de tempo moderados.

RNF-10 establece que el 100 % de las transiciones deben respetar las restricciones configuradas.

Actualmente no existe un parámetro explícito que permita definir qué se considera un salto moderado.

## Problema

La restricción no es completamente verificable porque no existe un valor cuantificable asociado.

## Alternativas

### A1. Mantener la situación actual

El sistema interpreta internamente qué significa "salto moderado".

#### Ventajas

- Menor complejidad para el usuario.

#### Inconvenientes

- La restricción no es totalmente verificable.
- La validación experimental es más difícil.

### A2. Añadir un parámetro explícito

Ejemplo:

```text
Salto máximo BPM = 5 BPM
```

#### Ventajas

- Restricción verificable.
- Mayor control para el DJ.
- Facilita la validación experimental.

#### Inconvenientes

- Incrementa el número de parámetros configurables.

## Propuesta inicial

Incorporar un nuevo requisito que permita definir el salto máximo de BPM entre pistas consecutivas.

## Pendiente de validación

Tutor y cotutor.

---

# OD-03 · Estrategia de identificación permanente de pistas

## Contexto

RF-09 establece:

> Una misma pista debe conservar su identidad aunque cambie de nombre o ubicación.

Por tanto, la identidad no puede depender exclusivamente de:

- Nombre del fichero.
- Ruta.
- Carpeta.

## Problema

Debe definirse un mecanismo de identificación estable.

La decisión afecta a:

- Importación.
- Reescaneo.
- Reanálisis.
- Exportación.
- Persistencia.

## Alternativas

### A1. Hash completo del fichero

#### Ventajas

- Fácil implementación.
- Alta unicidad.

#### Inconvenientes

- Cambia al modificar etiquetas.

### A2. Hash del contenido de audio

#### Ventajas

- Independiente de metadatos.

#### Inconvenientes

- Coste computacional elevado.

### A3. Fingerprint acústico

#### Ventajas

- Diseñado específicamente para identificación musical.
- Tolera determinadas modificaciones.

#### Inconvenientes

- Mayor complejidad.

## Propuesta inicial

Evaluar una estrategia basada en fingerprint acústico.

## Pendiente de validación

Tutor y cotutor.

---

# OD-04 · Persistencia de resultados multi-motor

## Contexto

La arquitectura actual contempla la utilización de varios motores de análisis:

- Essentia.
- Librosa.
- Madmom.

Además, RF-07 exige almacenar:

- Origen.
- Motor.
- Versión.

RF-29 requiere comparar resultados obtenidos por distintos motores.

## Problema

Debe decidirse si una pista puede almacenar múltiples resultados de análisis simultáneamente.

## Alternativas

### A1. Un único resultado por pista

#### Ventajas

- Modelo sencillo.
- Menor ocupación.

#### Inconvenientes

- Impide comparativas.
- Dificulta validación experimental.

### A2. Múltiples resultados por pista

Relación:

```text
Track 1:N AnalysisResult
```

#### Ventajas

- Permite comparación entre motores.
- Facilita experimentación.
- Permite coexistencia de versiones.

#### Inconvenientes

- Modelo más complejo.

## Propuesta inicial

Permitir múltiples resultados por pista.

## Pendiente de validación

Tutor y cotutor.

---

# OD-05 · Existencia de la entidad Library

## Contexto

La aplicación trabaja sobre una colección musical local.

Debe decidirse si una biblioteca constituye una entidad explícita del dominio.

## Problema

El sistema puede asumir una única biblioteca o permitir múltiples bibliotecas.

## Alternativas

### A1. Mantener entidad Library

#### Ventajas

- Permite múltiples bibliotecas.
- Permite histórico de importaciones.
- Facilita estadísticas.

#### Inconvenientes

- Incrementa complejidad.

### A2. Eliminar entidad Library

#### Ventajas

- Simplificación del dominio.

#### Inconvenientes

- Menor flexibilidad.

## Propuesta inicial

Mantener la entidad Library.

## Pendiente de validación

Tutor y cotutor.

---

# OD-06 · Modelado explícito de transiciones

## Contexto

RF-17 exige evaluar transiciones.

RF-20 exige mostrar información asociada a cada transición.

Las transiciones contienen información propia:

- Compatibilidad armónica.
- Salto BPM.
- Puntuación.
- Estado.

## Problema

Debe decidirse si las transiciones se representan mediante una entidad específica.

## Alternativas

### A1. Calcularlas dinámicamente

#### Ventajas

- Menor persistencia.

#### Inconvenientes

- Menor trazabilidad.

### A2. Persistir explícitamente las transiciones

#### Ventajas

- Facilita trazabilidad.
- Facilita validación.
- Facilita auditoría.

#### Inconvenientes

- Más almacenamiento.

## Propuesta inicial

Persistir explícitamente las transiciones.

### Campos mínimos

```text
transition_id
setlist_id
from_track_id
to_track_id

bpm_delta
camelot_distance

harmonic_valid

transition_score
```

## Pendiente de validación

Tutor y cotutor.

---

# OD-07 · Modelo de dominio propuesto

## Objetivo

Validar si el conjunto de entidades propuesto representa adecuadamente el dominio del problema.

---

## Track

Representa una pista musical única independiente de su ubicación física.

### Campos mínimos

```text
track_id
fingerprint
status
created_at
```

### Justificación

Entidad principal del dominio.

Todos los procesos giran alrededor de ella.

---

## TrackLocation

Representa una ubicación física concreta de una pista.

### Campos mínimos

```text
location_id
track_id

file_path
last_seen_at
status
```

### Justificación

Permite detectar:

- pistas movidas,
- pistas ausentes,
- duplicados.

---

## TrackMetadata

Representa metadatos musicales y descriptivos.

### Campos mínimos

```text
metadata_id
track_id

title
artist
genre
year
duration_seconds
```

### Justificación

Separa la identidad de la pista de sus etiquetas.

---

## AnalysisRun

Representa una ejecución concreta de un motor MIR.

### Campos mínimos

```text
run_id

engine_name
engine_version

executed_at
```

### Justificación

Permite trazabilidad completa de los análisis realizados.

---

## AnalysisResult

Representa el resultado obtenido por un motor de análisis.

### Campos mínimos

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

### Justificación

Permite almacenar múltiples resultados sobre una misma pista.

---

## GenerationRequest

Representa una solicitud de generación.

### Campos mínimos

```text
request_id

target_duration

bpm_min
bpm_max

harmonic_policy

random_seed
```

### Justificación

Permite reproducibilidad del proceso de generación.

---

## GenreSegment

Representa las preferencias de género a lo largo del tiempo.

### Campos mínimos

```text
segment_id
request_id

start_time
end_time

genre
```

### Justificación

Soporta RF-15.

---

## Anchor

Representa una pista fijada en una posición concreta.

### Campos mínimos

```text
anchor_id

request_id
track_id

position
```

### Justificación

Soporta RF-16.

---

## Setlist

Representa un setlist generado.

### Campos mínimos

```text
setlist_id

request_id

created_at

status
```

### Justificación

Entidad principal del resultado del sistema.

---

## SetlistTrack

Representa las pistas pertenecientes a un setlist.

### Campos mínimos

```text
setlist_id
track_id

position
```

### Justificación

Permite representar orden y composición del setlist.

---

## Transition

Representa una transición entre dos pistas.

### Campos mínimos

```text
transition_id

from_track_id
to_track_id

bpm_delta

camelot_distance

transition_score
```

### Justificación

Permite evaluar la calidad de la mezcla.

---

## ReferenceMeasurement

Representa valores de referencia obtenidos desde Rekordbox.

### Campos mínimos

```text
reference_id
track_id

bpm_reference
key_reference
camelot_reference
```

### Justificación

Permite validar el sistema.

---

## EvaluationReport

Representa resultados experimentales agregados.

### Campos mínimos

```text
report_id

generated_at

bpm_accuracy
key_accuracy
camelot_accuracy
```

### Justificación

Permite soportar los RNF de validación.

## Pendiente de validación

Conjunto completo de entidades del dominio.

---

# OD-08 · Nuevos ADR potenciales

## ADR-007

Licencias y compatibilidad legal de dependencias.

## ADR-008

Lenguaje de programación, interfaz gráfica y empaquetado.

## ADR-009

Conjunto de evaluación experimental y protocolo de validación.

## Problema

Estos temas aparecen referenciados en varios documentos, pero actualmente no disponen de una decisión arquitectónica formal asociada.

## Propuesta inicial

Evaluar la necesidad de crear dichos ADR antes del inicio de la implementación.

## Pendiente de validación

Tutor y cotutor.
