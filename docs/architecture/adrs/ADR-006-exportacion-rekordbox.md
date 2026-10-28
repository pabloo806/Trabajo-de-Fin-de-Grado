# ADR-006: Exportación e Integración con Rekordbox

## Estado

Aceptado

## Fecha

2026-10-28

## Contexto

Uno de los objetivos principales de SetlistGen es integrarse en el flujo de trabajo real de un DJ.

Para ello, los setlists generados deben poder utilizarse posteriormente en Rekordbox, que es la herramienta de referencia utilizada durante la actuación.

El sistema no debe:

- Modificar la base de datos interna de Rekordbox.
- Depender de APIs privadas.
- Requerir acceso a Internet.
- Comprometer la portabilidad del sistema.

Por tanto, la integración debe realizarse mediante formatos de intercambio soportados por Rekordbox.

## Problema

Determinar el mecanismo de exportación de setlists para garantizar la integración con Rekordbox.

## Alternativas consideradas

### A1. XML de Rekordbox

Exportación utilizando el formato XML compatible con Rekordbox.

#### Ventajas

- Preserva la estructura de playlists.
- Permite transmitir metadatos asociados.
- Integración directa con el flujo de importación de Rekordbox.
- Formato diseñado específicamente para intercambio con Rekordbox.
- Compatible con las necesidades del proyecto.

#### Inconvenientes

- Formato más complejo.
- Requiere respetar una estructura concreta.
- Necesidad de mapear correctamente las rutas de las pistas.

---

### A2. M3U8

Exportación mediante listas de reproducción en formato M3U8.

#### Ventajas

- Muy sencillo de generar.
- Fácil de inspeccionar manualmente.
- Compatible con numerosos reproductores.

#### Inconvenientes

- No transporta información adicional relevante.
- Menor integración con Rekordbox.
- Dependencia exclusiva de las rutas de los archivos.

---

### A3. Escritura directa sobre la base de datos de Rekordbox

Modificación directa de la base de datos interna de la aplicación.

#### Ventajas

- Integración aparentemente completa.

#### Inconvenientes

- Dependencia de una estructura interna no documentada.
- Riesgo elevado de incompatibilidades.
- Acoplamiento a una versión concreta de Rekordbox.
- Solución incompatible con el alcance del proyecto.

---

## Criterios de evaluación

| Criterio | Peso |
|-----------|------:|
| Compatibilidad con Rekordbox | 5 |
| Robustez | 5 |
| Facilidad de implementación | 4 |
| Facilidad de uso para el DJ | 5 |
| Mantenibilidad | 4 |
| Portabilidad | 4 |
| Riesgo tecnológico | 5 |

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

### XML de Rekordbox

| Criterio | Peso | Valoración | Resultado |
|-----------|------:|-----------:|----------:|
| Compatibilidad con Rekordbox | 5 | 5 | 25 |
| Robustez | 5 | 5 | 25 |
| Facilidad de implementación | 4 | 3 | 12 |
| Facilidad de uso para el DJ | 5 | 5 | 25 |
| Mantenibilidad | 4 | 4 | 16 |
| Portabilidad | 4 | 5 | 20 |
| Riesgo tecnológico | 5 | 5 | 25 |

**Total: 148**

---

### M3U8

| Criterio | Peso | Valoración | Resultado |
|-----------|------:|-----------:|----------:|
| Compatibilidad con Rekordbox | 5 | 3 | 15 |
| Robustez | 5 | 4 | 20 |
| Facilidad de implementación | 4 | 5 | 20 |
| Facilidad de uso para el DJ | 5 | 3 | 15 |
| Mantenibilidad | 4 | 5 | 20 |
| Portabilidad | 4 | 5 | 20 |
| Riesgo tecnológico | 5 | 5 | 25 |

**Total: 135**

---

### Escritura directa sobre la base de datos

| Criterio | Peso | Valoración | Resultado |
|-----------|------:|-----------:|----------:|
| Compatibilidad con Rekordbox | 5 | 2 | 10 |
| Robustez | 5 | 1 | 5 |
| Facilidad de implementación | 4 | 1 | 4 |
| Facilidad de uso para el DJ | 5 | 5 | 25 |
| Mantenibilidad | 4 | 1 | 4 |
| Portabilidad | 4 | 1 | 4 |
| Riesgo tecnológico | 5 | 1 | 5 |

**Total: 57**

---

## Comparación funcional

| Característica | XML Rekordbox | M3U8 |
|---------------|---------------|------|
| Importación directa en Rekordbox | Sí | Parcial |
| Estructura de playlists | Sí | Limitada |
| Metadatos asociados | Sí | No |
| Compatibilidad con otros reproductores | Limitada | Muy alta |
| Complejidad de implementación | Media | Baja |
| Formato principal recomendado | Sí | No |

## Estrategia adoptada

SetlistGen implementará dos formatos de exportación:

### Exportación principal

```text
XML Rekordbox
```

Destinada a la integración completa con Rekordbox.

### Exportación secundaria

```text
M3U8
```

Destinada a interoperabilidad y uso en otros reproductores.

## Decisión

Se adopta el formato XML de Rekordbox como mecanismo principal de integración.

Además, se proporcionará exportación adicional en formato M3U8 como característica complementaria.

No se realizará ninguna modificación directa de la base de datos interna de Rekordbox.

## Justificación

El XML de Rekordbox proporciona la mejor integración posible respetando las restricciones del proyecto.

Permite intercambiar playlists de forma segura, reproducible y desacoplada de la implementación interna de Rekordbox.

La exportación adicional a M3U8 mejora la interoperabilidad sin introducir complejidad significativa.

## Consecuencias

### Positivas

- Integración completa con Rekordbox.
- Ausencia de dependencias privadas.
- Solución robusta frente a cambios internos.
- Mayor interoperabilidad mediante M3U8.
- Fácil validación experimental.

### Negativas

- Necesidad de implementar el generador XML.
- Validación manual de importación durante las pruebas.
- Gestión correcta de rutas multiplataforma.

## Evidencias utilizadas

- Requisitos de exportación a Rekordbox.
- Objetivos de integración del proyecto.
- Restricciones de funcionamiento local.
- Necesidad de mantener independencia frente a software propietario.

## Decisiones relacionadas

- ADR-001: Forma de Distribución del Sistema.
- ADR-002: Arquitectura General del Sistema.
- ADR-003: Motor de Análisis Musical.
- ADR-004: Persistencia.
- ADR-005: Algoritmo de Generación de Setlists.
