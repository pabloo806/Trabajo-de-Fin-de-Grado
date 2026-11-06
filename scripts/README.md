# Scripts

## Descripción

Este directorio contiene scripts auxiliares utilizados durante el desarrollo, validación y mantenimiento de SetlistGen.

Los scripts no forman parte de la lógica de negocio principal y su propósito es automatizar tareas repetitivas o facilitar actividades de soporte.

---

## Posibles usos

### Gestión de bibliotecas

- Escaneo de carpetas de prueba.
- Generación de bibliotecas sintéticas.
- Verificación de estructuras de directorios.

### Validación experimental

- Ejecución de benchmarks.
- Medición de tiempos de análisis.
- Medición de tiempos de generación.
- Evaluación frente a datos de referencia.

### Persistencia

- Inicialización de SQLite.
- Migraciones.
- Copias de seguridad.
- Carga de datos de ejemplo.

### Testing

- Generación de datos ficticios.
- Automatización de pruebas.
- Preparación de escenarios de validación.

### Memoria y documentación

- Generación de diagramas.
- Exportación de métricas.
- Consolidación de resultados experimentales.

---

## Estado

🔄 Pendiente de implementación.

La estructura definitiva dependerá de:

- ADR-004 Persistencia.
- ADR-009 Evaluación y validación.
- data-model.md.

---

## Scripts previstos

```text
scripts/
├── benchmark-analysis.py
├── benchmark-generator.py
├── create-test-library.py
├── export-evaluation-data.py
├── migrate-database.py
└── backup-database.py
```
