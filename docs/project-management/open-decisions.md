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

- Refleja la importancia de la evaluación.
- Alinea requisitos funcionales y no funcionales.

#### Inconvenientes

- Incrementa el alcance mínimo.

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

RF-17 exige transiciones con saltos de tempo moderados.

RNF-10 exige que todas las restricciones configuradas se respeten.

Sin embargo, no existe definición formal de "salto moderado".

## Problema

La restricción no es verificable ni reproducible.

## Alternativas

### A1. Mantener la situación actual

El sistema interpreta internamente qué es un salto moderado.

### A2. Configurar explícitamente un límite

Ejemplo:

```text
Salto máximo BPM = 5 BPM
```

#### Ventajas

- Restricción verificable.
- Más control para el DJ.

#### Inconvenientes

- Incrementa parámetros.

## Propuesta inicial

Crear RF-13b.

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

Debe definirse el mecanismo definitivo de identificación.

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

- Costoso.

### A3. Fingerprint acústico

#### Ventajas

- Específico para identificación musical.

#### Inconvenientes

- Computacionalmente costoso.

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

- Mayor complejidad.

## Propuesta inicial

Estrategia de doble nivel descrita en ADR-010.

## Estado

Pendiente de validación por tutor y cotutor.

---

# OD-04 · Persistencia multi-motor

## Contexto

La arquitectura contempla:

- Essentia
- Librosa
- Madmom

RF-07 exige almacenar:

- motor,
- versión,
- origen.

RF-29 exige comparación de resultados.

## Problema

Debe decidirse si una pista almacena uno o varios resultados.

## Alternativas

### A1. Un resultado por pista

#### Ventajas

- Modelo simple.

#### Inconvenientes

- No permite evaluación comparativa.

### A2. Múltiples resultados por pista

Relación:

```text
Track 1:N AnalysisResult
```

#### Ventajas

- Comparación entre motores.
- Repetibilidad.
- Compatibilidad con RF-07.

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

## Problema

Determinar si el sistema soportará una o varias bibliotecas.

## Alternativas

### A1. Mantener entidad Library

#### Ventajas

- Varias bibliotecas.
- Histórico.
- Estadísticas.

#### Inconvenientes

- Mayor complejidad.

### A2. Eliminar entidad Library

#### Ventajas

- Simplificación.

#### Inconvenientes

- Menor flexibilidad.

## Propuesta inicial

Mantener la entidad Library.

## Estado

Pendiente de validación por tutor y cotutor.

---

# OD-06 · Persistencia de transiciones

## Contexto

RF-17 exige evaluar transiciones.

RF-20 exige mostrarlas.

RF-20b permite reordenar manualmente setlists.

## Problema

Determinar si las transiciones deben persistirse o recalcularse.

## Alternativas

### A1. Recalcular dinámicamente

#### Ventajas

- Siempre consistentes tras cambios.

#### Inconvenientes

- Menor trazabilidad.

### A2. Persistir explícitamente

#### Ventajas

- Auditoría.
- Históricos.

#### Inconvenientes

- Riesgo de inconsistencias.

## Propuesta inicial

Pendiente de decisión.

## Estado

Pendiente de validación por tutor y cotutor.

---

# OD-07 · Modelo de dominio definitivo

## Objetivo

Validar si el conjunto de entidades representa correctamente el dominio.

## Entidades propuestas

- Track
- TrackLocation
- TrackMetadata
- AnalysisRun
- AnalysisResult
- GenerationRequest
- GenreSegment
- Anchor
- Setlist
- SetlistTrack
- Transition
- ReferenceMeasurement
- EvaluationReport

## Estado

Pendiente de validación por tutor y cotutor.

---

# OD-08 · Estado de ADR-007 a ADR-010

## Contexto

ADR-007, ADR-008, ADR-009 y ADR-010 ya existen.

Sin embargo, todavía no han sido validados por los tutores.

## Problema

Determinar si deben mantenerse, modificarse o consolidarse.

## Estado

Pendiente de validación.

---

# OD-09 · Motor MIR definitivo

## Contexto

ADR-003 define una arquitectura desacoplada.

Todavía no se ha seleccionado el motor definitivo.

## Alternativas

- Essentia
- Librosa
- Madmom
- Estrategia híbrida

## Propuesta inicial

Esperar a la prueba de concepto.

## Estado

Pendiente de validación.

---

# OD-10 · Estrategia final de evaluación

## Contexto

ADR-009 propone:

- Biblioteca personal estratificada.
- Dataset complementario.
- Comparación frente a Rekordbox.

## Problema

Determinar el protocolo definitivo de validación.

## Propuesta inicial

Biblioteca personal + dataset público complementario.

## Estado

Pendiente de validación.

---

# Cuestiones a tratar en la próxima reunión

## Bloque 1 · Requisitos

### P1. Evaluación experimental

¿Debe RF-29 pasar de Should a Must?

### P2. Salto máximo BPM

¿Debe existir un parámetro explícito configurable?

---

## Bloque 2 · Dominio

### P3. Identidad de pistas

¿Es adecuada la estrategia de identificación en dos niveles?

### P4. Persistencia multi-motor

¿Deben coexistir múltiples resultados por pista?

### P5. Entidad Library

¿Debe existir o puede asumirse una única biblioteca?

### P6. Entidad Transition

¿Persistir o recalcular?

### P7. Modelo de dominio

¿Representan correctamente estas entidades el problema?

---

## Bloque 3 · Arquitectura

### P8. ADR-007

¿Es necesaria una política explícita de licencias?

### P9. ADR-008

¿Es adecuada Python + PySide6?

### P10. ADR-009

¿Es adecuado el protocolo experimental propuesto?

---

# Resultado esperado de la reunión

Cerrar:

- OD-01
- OD-02
- OD-03
- OD-04
- OD-05
- OD-06
- OD-07

y autorizar el inicio de:

```text
docs/architecture/data-model.md
```

como siguiente gran entregable del proyecto.
