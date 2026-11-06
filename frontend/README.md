# Frontend

## Descripción

Este directorio contendrá la interfaz gráfica de SetlistGen.

La interfaz será responsable de:

- Gestión de bibliotecas musicales.
- Configuración de parámetros de generación.
- Visualización de análisis.
- Visualización de setlists.
- Exportación.
- Consulta de estadísticas.
- Evaluación experimental.

La interfaz no contendrá lógica de negocio.

Toda la lógica permanecerá en las capas de dominio y aplicación según ADR-002.

---

## Objetivos

La interfaz debe permitir a un DJ:

- Importar bibliotecas.
- Analizar pistas.
- Configurar restricciones.
- Generar setlists.
- Revisar resultados.
- Exportar playlists.
- Consultar el historial.

---

## Tecnología prevista

ADR-008 propone actualmente:

```text
Python + PySide6
```

como alternativa principal.

Alternativas evaluadas:

- PySide6
- Tkinter
- wxPython

La decisión definitiva se validará tras la prueba de concepto.

---

## Principios

La interfaz deberá:

- Mantener la separación de responsabilidades.
- No acceder directamente a SQLite.
- No contener lógica de generación.
- Mostrar progreso en operaciones largas.
- Permitir cancelación de procesos.
- Cumplir los requisitos de usabilidad del SRS.

---

## Funcionalidades previstas

### Gestión de Biblioteca

- Exploración de carpetas.
- Visualización de pistas.
- Filtros.
- Ordenación.

### Generación de Setlists

- Configuración de duración.
- Configuración BPM.
- Configuración Camelot.
- Restricciones de género.
- Gestión de anclas.

### Exportación

- XML Rekordbox.
- M3U8.

### Estadísticas

- BPM.
- Camelot.
- Géneros.
- Historial.

### Evaluación

- Comparación frente a Rekordbox.
- Informes de discrepancias.

---

## Estado

🔄 Pendiente de implementación.

La estructura definitiva dependerá de ADR-008 y del diseño de dominio actualmente en elaboración.
