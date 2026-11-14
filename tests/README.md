# Testing

## Objetivo

Garantizar la calidad, fiabilidad y corrección de SetlistGen mediante una estrategia de pruebas alineada con:

- requirements.md
- use-cases.md
- traceability-matrix.md
- ADR-009

---

## Estrategia de pruebas

### Pruebas unitarias

Validan:

- Objetos de dominio.
- Objetos de valor.
- Reglas de negocio.
- Conversión Camelot.
- Restricciones de generación.

Herramienta:

```text
pytest
```

---

### Pruebas de integración

Validan:

- Persistencia SQLite.
- Repositorios.
- Adaptadores de análisis musical.
- Exportación.

---

### Pruebas funcionales

Validan:

- Casos de uso completos.
- Cumplimiento de RF.
- Cumplimiento de restricciones.

---

### Pruebas de rendimiento

Validan:

- RNF-01
- RNF-02
- RNF-03
- RNF-04
- RNF-18

---

### Validación experimental

Validan:

- RNF-05
- RNF-06
- RNF-07
- RNF-08
- RNF-09

mediante comparación frente a Rekordbox.

---

### Evaluación por usuarios

Validan:

- RNF-12
- RNF-13

mediante sesiones con DJs.

---

## Trazabilidad

Las pruebas deben mantenerse alineadas con:

```text
docs/requirements/traceability-matrix.md
```

de forma que:

```text
RF
↓
RNF
↓
CU
↓
Casos de prueba
```

mantengan trazabilidad completa.

---

## Estructura prevista

```text
tests/
├── unit/
├── integration/
├── functional/
├── performance/
└── validation/
```

---

## Estado

🔄 En preparación.

El catálogo de pruebas se encuentra definido en:

```text
docs/testing/test-catalog.md
```

y en la matriz de trazabilidad.
