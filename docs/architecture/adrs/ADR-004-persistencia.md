# ADR-004: Persistencia

## Estado

Aceptado

## Fecha

2026-10-28

## Contexto

SetlistGen necesita almacenar de forma persistente la información generada durante el análisis y la planificación de sesiones.

La solución debe permitir almacenar:

- Bibliotecas musicales importadas.
- Metadatos de las pistas.
- Resultados del análisis musical (BPM, tonalidad y código Camelot).
- Setlists generados.
- Historial de generación.
- Configuración de usuario.
- Información necesaria para evitar reprocesar pistas ya analizadas.

De acuerdo con ADR-001, SetlistGen se distribuirá como una aplicación de escritorio destinada a un único usuario que trabaja localmente sobre su propia biblioteca musical.

Además, la solución debe:

- Funcionar sin servicios externos.
- Requerir una instalación mínima.
- Mantener una complejidad operativa reducida.
- Ser portable entre sistemas operativos.
- Integrarse fácilmente con Python.
- Permitir consultas eficientes sobre miles de pistas.

## Problema

Determinar la tecnología de persistencia utilizada por SetlistGen.

## Alternativas consideradas

### A1. SQLite

Motor de base de datos relacional embebido que almacena toda la información en un único fichero local.

#### Ventajas

- No requiere instalación adicional.
- Integrado en Python mediante el módulo `sqlite3`.
- Excelente portabilidad.
- Administración prácticamente inexistente.
- Rendimiento más que suficiente para el volumen esperado de datos.
- Fácil respaldo mediante copia del fichero de base de datos.
- Amplia documentación.

#### Inconvenientes

- Menor capacidad de escalado para escenarios multiusuario.
- Menor capacidad de concurrencia que bases de datos servidor.

---

### A2. PostgreSQL

Sistema gestor de bases de datos relacional cliente-servidor.

#### Ventajas

- Muy potente y escalable.
- Excelente soporte para consultas complejas.
- Amplias capacidades de administración.

#### Inconvenientes

- Requiere instalación y configuración.
- Introduce complejidad operativa innecesaria.
- Dependencia de un servicio en ejecución.
- Sobredimensionado para el alcance del proyecto.

---

### A3. Almacenamiento basado en ficheros

Persistencia mediante JSON, CSV o estructuras similares.

#### Ventajas

- Implementación sencilla.
- Fácil inspección manual.

#### Inconvenientes

- Gestión compleja de relaciones.
- Consultas ineficientes.
- Escalabilidad limitada.
- Mayor riesgo de inconsistencia.
- Más difícil evolucionar el modelo de datos.

---

## Criterios de evaluación

| Criterio | Peso |
|-----------|------:|
| Facilidad de despliegue | 5 |
| Rendimiento | 4 |
| Complejidad operativa | 5 |
| Portabilidad | 5 |
| Escalabilidad | 3 |
| Soporte para consultas | 4 |
| Integración con Python | 5 |
| Mantenibilidad | 4 |

### Escala de valoración

| Valor | Significado |
|--------|-------------|
| 1 | Muy deficiente |
| 2 | Deficiente |
| 3 | Aceptable |
| 4 | Bueno |
| 5 | Excelente |

### Método de cálculo

La puntuación ponderada de cada criterio se calcula como:

```text
Puntuación ponderada = Valoración × Peso
```

La puntuación total de cada alternativa se calcula como:

```text
Total = Σ (Valoración × Peso)
```

---

## Evaluación de alternativas

### SQLite

| Criterio | Peso | Valoración | Resultado |
|-----------|------:|-----------:|----------:|
| Facilidad de despliegue | 5 | 5 | 25 |
| Rendimiento | 4 | 4 | 16 |
| Complejidad operativa | 5 | 5 | 25 |
| Portabilidad | 5 | 5 | 25 |
| Escalabilidad | 3 | 3 | 9 |
| Soporte para consultas | 4 | 5 | 20 |
| Integración con Python | 5 | 5 | 25 |
| Mantenibilidad | 4 | 5 | 20 |

**Total: 165**

---

### PostgreSQL

| Criterio | Peso | Valoración | Resultado |
|-----------|------:|-----------:|----------:|
| Facilidad de despliegue | 5 | 2 | 10 |
| Rendimiento | 4 | 5 | 20 |
| Complejidad operativa | 5 | 2 | 10 |
| Portabilidad | 5 | 4 | 20 |
| Escalabilidad | 3 | 5 | 15 |
| Soporte para consultas | 4 | 5 | 20 |
| Integración con Python | 5 | 4 | 20 |
| Mantenibilidad | 4 | 4 | 16 |

**Total: 131**

---

### Ficheros JSON / CSV

| Criterio | Peso | Valoración | Resultado |
|-----------|------:|-----------:|----------:|
| Facilidad de despliegue | 5 | 5 | 25 |
| Rendimiento | 4 | 2 | 8 |
| Complejidad operativa | 5 | 4 | 20 |
| Portabilidad | 5 | 5 | 25 |
| Escalabilidad | 3 | 1 | 3 |
| Soporte para consultas | 4 | 1 | 4 |
| Integración con Python | 5 | 5 | 25 |
| Mantenibilidad | 4 | 2 | 8 |

**Total: 118**

---

## Modelo de datos previsto

La persistencia deberá cubrir, como mínimo, las siguientes entidades:

```text
Track
├── Metadatos
├── BPM
├── Tonalidad
├── Camelot
└── Estado de análisis

Library
├── Pistas
└── Estadísticas

Setlist
├── Parámetros
├── Pistas seleccionadas
└── Fecha de generación

AnalysisRun
├── Fecha
├── Configuración
└── Resultados
```

La estructura definitiva se concretará durante el diseño detallado.

## Decisión

Se adopta **SQLite** como tecnología de persistencia principal del sistema.

## Justificación

SQLite es la solución que mejor se adapta al contexto del proyecto.

El sistema:

- Es una aplicación de escritorio.
- Está orientado a un único usuario.
- Trabaja sobre datos locales.
- No requiere concurrencia elevada.
- Debe ser sencillo de instalar y distribuir.

SQLite permite almacenar toda la información en un único fichero, elimina la necesidad de administrar servicios adicionales y se integra de forma nativa con Python.

La evaluación multicriterio muestra además que es la alternativa con la puntuación total más alta y el mejor equilibrio entre simplicidad, rendimiento y mantenibilidad.

## Consecuencias

### Positivas

- Instalación extremadamente sencilla.
- Sin dependencias externas.
- Integración nativa con Python.
- Excelente portabilidad.
- Copias de seguridad simples.
- Rendimiento suficiente para el volumen previsto.

### Negativas

- Limitaciones en escenarios multiusuario.
- Menor capacidad de escalado que PostgreSQL.
- Menor capacidad de concurrencia.

## Evidencias utilizadas

- ADR-001: Aplicación de escritorio.
- Requisitos de funcionamiento local.
- Requisitos de mantenibilidad.
- Requisitos de portabilidad.
- Requisitos de persistencia de bibliotecas musicales.
- Necesidad de procesar bibliotecas de tamaño medio sin infraestructura adicional.

## Decisiones relacionadas

- ADR-001: Forma de Distribución del Sistema.
- ADR-002: Arquitectura General del Sistema.
- ADR-003: Motor de Análisis Musical.
- ADR-005: Algoritmo de Generación de Setlists.
- ADR-006: Exportación e Integración con Rekordbox.
