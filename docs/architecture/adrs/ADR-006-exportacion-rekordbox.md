[ADR-006-exportacion-rekordbox.md](https://github.com/user-attachments/files/34364413/ADR-006-exportacion-rekordbox.md)
# ADR-006: Exportación e Integración con Rekordbox

## Estado

Aceptado (revisado el 2026-10-30). La **estrategia** (XML como formato principal y M3U8 como complemento) está aceptada. Su **verificación** depende de la prueba de importación en Rekordbox (riesgo R-02, RF-23), que todavía no se ha realizado.

## Fecha

2026-10-28 (decisión original) · 2026-10-30 (revisión de alineación con la línea base documental)

## Requisitos relacionados

| Requisito | Relación |
|---|---|
| RF-21 | Exportación del setlist en XML compatible con Rekordbox |
| RF-21b | Exportación complementaria en M3U8 |
| RF-22 | Rutas de las pistas resueltas, con aviso explícito si alguna no lo está |
| RF-23 | Verificación manual de que Rekordbox carga la lista con sus pistas resueltas |
| RF-09c | Aviso de pistas ausentes al exportar |
| RF-28 | Exportación de datos del panel (M3U), con relación indirecta |
| RF-29b | Lectura del XML de colección como fuente de referencia (puerto distinto) |
| RNF-16 | Rutas con espacios, tildes, Unicode y rutas largas en ambos sistemas |
| RNF-19 | Windows y macOS |
| RNF-21 | El dominio no depende del formato de rutas del sistema operativo |
| RNF-22, RNF-23 | Exportador accesible mediante un puerto sustituible |
| RNF-25 | El sistema no envía datos fuera del equipo |

Riesgo asociado: R-02 (el fichero exportado no se carga correctamente en Rekordbox). Hallazgos atendidos: N-02 (M3U8 sin requisito) y N-16 (decisiones aceptadas antes de la prueba de concepto).

## Contexto

Uno de los objetivos principales de SetlistGen es integrarse en el flujo de trabajo real de un DJ.

Para ello, los setlists generados deben poder utilizarse posteriormente en Rekordbox, que es la herramienta de referencia utilizada durante la actuación.

El anteproyecto establece que el setlist se exporta en un formato importable por Rekordbox, citando XML o M3U/M3U8.

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
- Solución incompatible con el alcance del proyecto (SRS, sección 2.5).

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

Los tres totales se han verificado y no se modifican en esta revisión.

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

Las filas de esta tabla proceden de la valoración original y se confirman o corrigen en la prueba de importación.

## Estrategia adoptada

SetlistGen implementará dos formatos de exportación:

### Exportación principal

```text
XML Rekordbox
```

Destinada a la integración completa con Rekordbox (RF-21).

### Exportación secundaria

```text
M3U8
```

Destinada a interoperabilidad y uso en otros reproductores (RF-21b).

## Decisión

Se adopta el formato XML de Rekordbox como mecanismo principal de integración.

Además, se proporcionará exportación adicional en formato M3U8 como característica complementaria.

No se realizará ninguna modificación directa de la base de datos interna de Rekordbox.

Ambos formatos se generan mediante el puerto `SetlistExporter` (ADR-002), con los adaptadores `RekordboxXmlExporter` y `M3u8Exporter`.

## Diseño previsto

### Responsabilidades

| Aspecto | Diseño |
|---|---|
| Entrada | Un setlist generado o editado, con el orden y los descriptores de sus pistas |
| Rutas | El dominio maneja la ubicación de la pista sin formato de sistema operativo. La conversión a la representación que espera cada formato se realiza en el adaptador (RNF-21) |
| Salida | Un fichero en disco; el setlist original no se modifica (CU-07) |
| Pistas ausentes o sin ruta resoluble | Se avisa de forma explícita y el DJ elige entre cancelar y continuar. Si continúa, las pistas se mantienen con su última ubicación conocida **[Cuestión abierta · verificar en la prueba de importación]** (RF-22, RF-09c) |
| Setlist editado a mano | Se exporta con su orden actual, avisando de las transiciones que incumplen restricciones (CU-07, A3) |

### Estructura del XML

Según la documentación del formato [4], el documento tiene un elemento raíz `DJ_PLAYLISTS` con dos secciones: `COLLECTION`, que lista las pistas con un identificador y atributos descriptivos, entre ellos su ubicación, y `PLAYLISTS`, que contiene un árbol de nodos que referencian las pistas por identificador o por ubicación. El detalle de los atributos y su dependencia de la versión de Rekordbox se confirma en la prueba de importación.

### M3U8

Fichero de texto en codificación UTF-8 con una ruta por pista, en el orden del setlist (RF-21b). La inclusión de cabecera y de información ampliada por pista, y el uso de rutas absolutas, son decisiones de diseño que se fijan al implementar.

### Dependencias

No se adopta una librería de terceros para el acceso a Rekordbox. La documentación de pyrekordbox se utiliza únicamente como descripción del formato XML [4]. Si en el futuro se utilizara alguna dependencia de este tipo, deberá pasar la revisión de ADR-007 y no podrá acceder a la base de datos interna de Rekordbox.

### Relación con la lectura de referencia

La lectura del XML de colección que el DJ exporta desde Rekordbox (RF-29b) es una operación de entrada, con un puerto distinto (`ReferenceDataProvider`). Ambos adaptadores pueden compartir conocimiento del formato XML dentro de la infraestructura, sin compartir interfaz.

## Cuestiones abiertas para la prueba de importación

Estas cuestiones no se resuelven con la documentación y requieren probar Rekordbox con ficheros reales. Su resultado puede modificar la estrategia de rutas o la valoración del XML.

| Cuestión | Requisito | Riesgo |
|---|---|---|
| ¿Qué representación de ruta espera Rekordbox en Windows y en macOS (separadores, unidad, prefijo y codificación de caracteres especiales)? | RF-22, RNF-16, RNF-19 | R-02 |
| ¿Cómo se comporta la importación con espacios, tildes, caracteres Unicode y rutas largas? | RNF-16 | R-02 |
| ¿Existe un esquema formal para validar el XML, o la validación es solo estructural y por importación? | RF-21 | R-02 |
| ¿Qué atributos de pista conviene incluir (por ejemplo BPM y tonalidad estimados) sin interferir con el análisis propio de Rekordbox? | RF-21 | R-02 |
| ¿Cómo se carga una pista con ubicación inexistente y qué advierte Rekordbox? | RF-22, RF-09c | R-02 |
| ¿Varía el comportamiento entre versiones de Rekordbox? Se registra la versión usada en cada prueba | RF-23 | R-02 |
| ¿Importa Rekordbox correctamente un M3U8 con rutas absolutas en ambos sistemas? | RF-21b | R-02 |

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
- Validación manual de importación durante las pruebas (RF-23), con dependencia de la versión de Rekordbox instalada.
- Gestión correcta de rutas multiplataforma (RNF-16, RNF-19).
- La valoración del XML parte de la documentación del formato, no de pruebas propias, hasta que se realice la prueba de importación.
- Si la prueba demuestra que el XML no resuelve las rutas de forma fiable, el M3U8 pasaría a ser el formato principal, con revisión de este ADR y de RF-21.

## Trazabilidad

| Elemento | Referencias |
|---|---|
| Requisitos funcionales | RF-09c, RF-21, RF-21b, RF-22, RF-23 |
| Requisitos no funcionales | RNF-16, RNF-19, RNF-21, RNF-22, RNF-23, RNF-25 |
| Componentes | CMP-05 (exportador Rekordbox) |
| Casos de uso | CU-07 (exportar setlist a Rekordbox) |
| Casos de prueba | T-CU07-01, T-CU07-02, T-CU07-03, T-CU07-04, T-RNF-16, T-RNF-19, T-RNF-21 |
| Riesgos | R-02 |

## Evidencias utilizadas

- Requisitos de exportación a Rekordbox (RF-21, RF-21b, RF-22, RF-23).
- Objetivos de integración del proyecto (O5) y su formulación en el anteproyecto.
- Restricciones de funcionamiento local (RNF-25).
- Necesidad de mantener independencia frente a software propietario.
- Documentación del formato XML de Rekordbox [4] y del formato M3U/M3U8 (memoria, secciones 3.6.1 y 3.6.2).

## Impacto en el proyecto

- Fija el puerto `SetlistExporter` y sus dos adaptadores.
- Hace de la prueba de importación en Rekordbox (tarea 2 del plan, hito H2) una condición para validar esta decisión.
- Condiciona el tratamiento de rutas, que debe quedar en infraestructura.
- Obliga a definir el conjunto de setlists de prueba para RF-23, incluidos nombres con caracteres especiales y ambos sistemas operativos.

## Impacto en la memoria

Guardar este contenido para la memoria del TFG.

- **Capítulo 3, sección 3.6:** descripción del XML de Rekordbox y de M3U8, ya redactada. Debe mantenerse coherente con las cuestiones abiertas de la prueba de importación.
- **Capítulo 4, secciones 4.4 y 4.6:** registrar que la estrategia se aceptó antes de la prueba de importación y que su verificación sigue pendiente.
- **Capítulo 6, sección 6.6:** diseño de la exportación.
- **Capítulo 7, sección 7.7:** implementación de los exportadores y de la conversión de rutas.
- **Capítulo 8, sección 8.5:** verificación de la exportación con Rekordbox.
- **Apéndice B, sección B.2:** incluir este ADR.

Bloque reutilizable:

- **Contexto:** los setlists deben llegar a Rekordbox sin tocar su base de datos ni depender de interfaces privadas.
- **Problema:** elegir el mecanismo de exportación.
- **Alternativas:** XML de Rekordbox, M3U8 y escritura directa en la base de datos.
- **Solución adoptada:** XML como formato principal y M3U8 como complemento, mediante el puerto `SetlistExporter`.
- **Justificación:** mayor puntuación (148 frente a 135 y 57) y respeto de la restricción de no modificar la base de datos de Rekordbox.
- **Ventajas:** integración con estructura de listas, intercambio seguro y desacoplado, e interoperabilidad con otros reproductores.
- **Limitaciones:** generación de rutas multiplataforma delicada y validación manual dependiente de la versión de Rekordbox.
- **Impacto:** exige una prueba de importación temprana y condiciona el tratamiento de rutas en infraestructura.

## Decisiones relacionadas

- ADR-001: Forma de Distribución del Sistema.
- ADR-002: Arquitectura General del Sistema.
- ADR-003: Motor de Análisis Musical.
- ADR-004: Persistencia.
- ADR-005: Algoritmo de Generación de Setlists.
- ADR-007: Licencias y compatibilidad legal (propuesto).
- ADR-008: Lenguaje, interfaz gráfica y empaquetado (propuesto).
- ADR-009: Dataset y protocolo de evaluación (propuesto).
- ADR-010: Identificación permanente de pistas (propuesto, OD-03).

## Cambios respecto a la versión original (2026-10-28)

| Cambio | Motivo |
|---|---|
| Estado aclarado: estrategia aceptada, verificación pendiente de la prueba de importación | Riesgo R-02 y hallazgo N-16 |
| M3U8 respaldado por RF-21b | Hallazgo N-02: el SRS v3.0 no tenía requisito para M3U8 del setlist |
| Puerto `SetlistExporter` con adaptadores `RekordboxXmlExporter` y `M3u8Exporter` | Vocabulario canónico (ADR-002) |
| Diseño previsto: responsabilidades, rutas y pistas ausentes | RF-22, RF-09c y RNF-21 |
| Tabla de cuestiones abiertas para la prueba de importación | Hacer verificable R-02 |
| Decisión de no adoptar una librería de terceros para Rekordbox | Coherencia con la restricción de no acceder a la base de datos de Rekordbox y con ADR-007 |
| Relación con la lectura de referencia (RF-29b) | Evitar mezclar los puertos de entrada y de salida |
| Requisitos, trazabilidad, impactos y decisiones ADR-007 a ADR-010 | Formato obligatorio de ADR |

Las puntuaciones y los totales no se modifican.
