# Arquitectura de SetlistGen

## Descripción

Este directorio contiene la documentación arquitectónica del proyecto SetlistGen.

El objetivo de esta documentación es registrar las decisiones arquitectónicas relevantes del sistema mediante Architecture Decision Records (ADR) y definir la arquitectura objetivo de la aplicación.

---

# Visión general

SetlistGen es una aplicación de escritorio desarrollada en Python que permite generar automáticamente setlists para DJs a partir de una biblioteca musical local.

El sistema:

- Importa bibliotecas musicales locales.
- Analiza automáticamente BPM y tonalidad.
- Calcula compatibilidad armónica mediante la rueda Camelot.
- Almacena resultados de análisis.
- Genera setlists mediante restricciones configurables.
- Exporta playlists compatibles con Rekordbox.

---

# Decisiones arquitectónicas adoptadas

## ADR-001: Forma de distribución

### Decisión

Aplicación de escritorio.

### Motivación

- Acceso directo a bibliotecas musicales locales.
- Funcionamiento completamente offline.
- Integración sencilla con herramientas de análisis musical.
- Orientado a un único usuario.

---

## ADR-002: Arquitectura general

### Decisión

Clean Architecture.

### Motivación

Separar la lógica de negocio de las tecnologías concretas utilizadas para:

- Persistencia.
- Análisis musical.
- Exportación.
- Interfaz de usuario.

### Estructura general

```text
UI
│
Application
│
Domain
│
Ports
│
Adapters
```

---

## ADR-003: Motor de análisis musical

### Decisión

Arquitectura desacoplada basada en puertos y adaptadores.

### Librerías evaluadas

- Essentia
- Librosa
- Madmom

### Estrategia

Essentia será la candidata principal para análisis musical.

Librosa y Madmom permanecerán disponibles para validación, comparación y sustitución futura.

---

## ADR-004: Persistencia

### Decisión

SQLite.

### Motivación

- Base de datos embebida.
- Sin instalación adicional.
- Integración nativa con Python.
- Excelente portabilidad.
- Adecuada para aplicaciones de escritorio monousuario.

---

## ADR-005: Generación de setlists

### Decisión

Constraint Satisfaction Problem (CSP).

### Restricciones mínimas

- BPM.
- Compatibilidad Camelot.
- Duración objetivo.
- Progresión de géneros.
- Pistas ancladas.
- No repetición de pistas.

---

## ADR-006: Integración con Rekordbox

### Decisión

- XML Rekordbox como formato principal.
- M3U8 como formato complementario.

### Restricciones

El sistema no modificará directamente la base de datos interna de Rekordbox.

---

# Lenguaje y stack tecnológico

## Lenguaje principal

```text
Python
```

### Justificación

Python proporciona:

- Integración natural con bibliotecas MIR.
- Soporte para Essentia.
- Soporte para Librosa.
- Soporte para Madmom.
- Ecosistema científico maduro.
- Buen soporte para procesamiento de audio.
- Integración sencilla con SQLite.

---

## Persistencia

```text
SQLite
```

---

## Bibliotecas MIR

```text
Essentia
Librosa
Madmom
```

---

## Formatos de exportación

```text
XML Rekordbox
M3U8
```

---

# Integración de componentes

La integración prevista entre los principales elementos del sistema es la siguiente:

```text
┌───────────────────────────────┐
│         Aplicación UI         │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│         Casos de Uso          │
├───────────────────────────────┤
│ Importar biblioteca           │
│ Analizar biblioteca           │
│ Generar setlist              │
│ Exportar playlist            │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│            Dominio            │
├───────────────────────────────┤
│ Track                         │
│ Library                       │
│ AnalysisResult                │
│ Setlist                       │
│ CamelotKey                    │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│            Puertos            │
├───────────────────────────────┤
│ AnalysisEngine                │
│ TrackRepository               │
│ SetlistRepository             │
│ Exporter                      │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│          Adaptadores          │
├───────────────────────────────┤
│ EssentiaAdapter               │
│ LibrosaAdapter                │
│ MadmomAdapter                 │
│ SQLiteAdapter                 │
│ RekordboxXmlExporter          │
│ M3U8Exporter                  │
└───────────────────────────────┘
```

---

# Flujo principal del sistema

```text
Biblioteca Musical
          │
          ▼
     Importación
          │
          ▼
 Análisis Musical
(BPM, Tonalidad)
          │
          ▼
       SQLite
          │
          ▼
 Generador CSP
          │
          ▼
  Setlist Generado
          │
          ▼
 Exportación XML
    /      \
   /        \
 XML      M3U8
   \
    \
 Rekordbox
```

---

# ADRs

Los ADRs se encuentran en el directorio:

```text
docs/architecture/adrs/
```

Actualmente existen los siguientes registros:

- ADR-001: Forma de Distribución del Sistema
- ADR-002: Arquitectura General del Sistema
- ADR-003: Motor de Análisis Musical
- ADR-004: Persistencia
- ADR-005: Algoritmo de Generación de Setlists
- ADR-006: Exportación e Integración con Rekordbox
