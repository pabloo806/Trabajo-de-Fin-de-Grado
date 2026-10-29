# Modelo de Datos

## Introducción

Este documento describe el modelo de dominio, el modelo conceptual, el modelo entidad-relación y el modelo físico de persistencia del sistema SetlistGen.

El objetivo es proporcionar una representación consistente de la información gestionada por el sistema y establecer la base para la implementación de la persistencia mediante SQLite.

---

# Objetivos de Diseño

El modelo de datos debe satisfacer los siguientes objetivos:

- Mantener una identidad estable para las pistas musicales.
- Evitar análisis redundantes.
- Permitir la convivencia de múltiples motores de análisis.
- Soportar el histórico de generación de setlists.
- Permitir la evaluación frente a Rekordbox.
- Facilitar la trazabilidad de resultados.
- Mantener compatibilidad con los requisitos RF-01 a RF-29.

---

# Principios de Diseño

## Persistencia local

Toda la información se almacena localmente mediante SQLite.

## Identidad independiente de la ruta

La identidad de una pista debe permanecer estable aunque cambien el nombre o la ubicación del archivo.

## Trazabilidad

Todos los resultados de análisis deben registrar:

- Motor utilizado.
- Versión.
- Parámetros de ejecución.

## Historial

Los setlists generados deben poder recuperarse junto con los parámetros utilizados para su generación.

---

# Modelo de Dominio

## Entidades principales

### Track

Representa una pista musical única.

### TrackLocation

Representa una ubicación física de una pista.

### TrackMetadata

Metadatos obtenidos a partir de etiquetas.

### AnalysisRun

Ejecución concreta de un motor MIR.

### AnalysisResult

Resultado producido por un motor de análisis.

### GenerationRequest

Parámetros utilizados para la generación de un setlist.

### Setlist

Setlist generado por el sistema.

### SetlistTrack

Relación ordenada entre pistas y setlists.

### Transition

Transición entre dos pistas consecutivas.

### ReferenceMeasurement

Valor de referencia procedente de Rekordbox.

### EvaluationReport

Resultado del proceso de validación.

---

# Modelo Conceptual

[Pendiente]

---

# Modelo Entidad-Relación

[Pendiente]

---

# Modelo Relacional

[Pendiente]

---

# Diseño Físico SQLite

[Pendiente]

---

# Índices

[Pendiente]

---

# Restricciones

[Pendiente]

---

# Justificación respecto al SRS

## RF-09

La identidad de pista se implementa mediante Track y TrackLocation.

## RF-09b

La detección de nuevas pistas se basa en la existencia previa de resultados de análisis.

## RF-10

Los setlists y sus parámetros se almacenan separadamente.

## RF-17

Las transiciones se representan explícitamente mediante la entidad Transition.

## RF-29

Los resultados de referencia se almacenan en ReferenceMeasurement.

---

# Cuestiones Abiertas

1. Método definitivo de identificación de pistas.
2. Estrategia multi-motor.
3. Modelo de referencia frente a Rekordbox.
4. Política de migraciones SQLite.
