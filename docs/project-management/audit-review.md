# Revisión Técnica de la Documentación

> Destino en el repositorio: `docs/project-management/audit-review.md`.

**Proyecto:** SetlistGen · Sistema de Generación Automática de Setlists para DJs
**Versión:** 3.1 (reescritura completa; sustituye a todas las versiones anteriores)
**Fecha:** 2026-11-06
**Estado:** línea base documental consistente, pendiente de validación por tutor y cotutor

---

# 1. Propósito y alcance

Este documento recoge el estado real del proyecto tras dos auditorías técnicas y la consolidación de la documentación. Sirve para tres fines:

1. Dejar constancia de qué está cerrado, qué está pendiente y qué es una hipótesis sin verificar.
2. Fijar la lista de hallazgos, riesgos y dependencias de diseño que condicionan la fase siguiente.
3. Servir de punto de partida del diseño del modelo de dominio y del modelo de datos.

Las decisiones que esperan validación de tutor y cotutor se tratan en `open-decisions.md`.

## 1.1 Cobertura de la revisión

| Fuente | Revisión |
|---|---|
| Documentos de la línea base (SRS, casos de uso, matriz, glosario, ADR-001 a ADR-010, READMEs) | Completa, con comprobaciones automáticas |
| Anteproyecto aprobado | Completa |
| Memoria (`book.pdf`, capítulos 1 a 4) | Completa |
| Normativa específica de la EPS | Parcial: artículos 1 a 9 |
| Normativa general de TFG y CV | No revisadas en esta pasada |
| Repositorio de GitHub e issues | No verificados |

---

# 2. Estado de madurez del proyecto

| Fase | Estado | Observación |
|---|---|---|
| Análisis (requisitos, casos de uso, trazabilidad, glosario) | **Cerrado** a nivel de línea base | SRS v4.0, casos de uso v1.1, matriz v3.0, glosario v2.1. Pendiente de validación por tutores |
| Arquitectura de alto nivel | **Cerrada** a nivel de línea base | ADR-001 a ADR-006 aceptados, con las condiciones de la sección 3.2 |
| Decisiones complementarias | Redactadas, **no validadas** | ADR-007 a ADR-010, en estado Propuesto |
| Diseño del modelo de dominio | **Siguiente paso** | Puede comenzar con supuestos explícitos (sección 8) |
| Diseño del modelo de datos y de SQLite | Siguiente paso, tras el dominio | La persistencia no se considera cerrada hasta validar `data-model.md` |
| Prueba de concepto (hito H2) | No realizada | Condiciona librería de análisis, importación en Rekordbox, identificación, interfaz y empaquetado |
| Implementación, pruebas y validación experimental | No iniciadas | No existe código ejecutable |
| Memoria | Capítulos 1 a 4 redactados | Requiere actualización (sección 7) |

> **Lectura correcta del estado.** Cerrado significa que la documentación es consistente y suficiente para empezar el diseño detallado. No significa validado por los tutores ni verificado con datos reales.

---

# 3. Línea base documental

## 3.1 Documentos y versiones

| Documento | Versión | Estado |
|---|---|---|
| `requirements.md` (SRS) | 4.0 | Consolidado; 36 RF y 27 RNF |
| `use-cases.md` | 1.1 | Consolidado; 11 casos de uso, 4 críticos |
| `traceability-matrix.md` | 3.0 | Consolidado; 67 casos de prueba previstos |
| `glosario.md` | 2.1 | Consolidado |
| ADR-001 a ADR-006 | Revisados el 2026-10-30 | Aceptados |
| ADR-007 a ADR-010 | Primera redacción | Propuestos |
| `README.md` y `docs/architecture/README.md` | 2.0 | Alineados |
| `open-decisions.md` | 3.1 | Reescrito junto a este documento |

## 3.2 Estado de los ADR y condiciones

| ADR | Decisión | Estado | Condición pendiente |
|---|---|---|---|
| ADR-001 | Aplicación de escritorio | Aceptado | Ninguna sobre la decisión |
| ADR-002 | Clean Architecture con puertos y adaptadores | Aceptado | Incorporar `EvaluationRepository` si se valida la propuesta |
| ADR-003 | Puerto `AudioAnalyzer`; librería por prueba de concepto | Aceptado | Selección de librería tras la prueba de concepto y ADR-007 |
| ADR-004 | SQLite | Aceptado | El esquema depende de OD-03 a OD-07 y de `data-model.md` |
| ADR-005 | Restricciones con función de coste | Aceptado | Validar la estrategia de búsqueda con prototipo y benchmark |
| ADR-006 | XML de Rekordbox con M3U8 complementario | Aceptado | Verificación mediante la prueba de importación |
| ADR-007 | Licencias y compatibilidad legal | Propuesto | Inventario verificado y validación (OD-08) |
| ADR-008 | Lenguaje, interfaz y empaquetado | Propuesto | Prueba de interfaz y de empaquetado y validación (OD-08) |
| ADR-009 | Conjunto de evaluación y protocolo | Propuesto | Prueba de concepto y validación (OD-08, OD-10) |
| ADR-010 | Identificación permanente de pistas | Propuesto | Prueba de identificación y validación (OD-03) |

## 3.3 Resultado de la segunda auditoría

Comprobaciones automáticas sobre los documentos de la línea base. Todas superadas.

| Comprobación | Resultado |
|---|---|
| IDs definidos | 36 RF, 27 RNF, 11 CU y 10 ADR |
| Referencias a RF, RNF, CU, ADR, OD y CMP | Ninguna rota |
| Prioridades MoSCoW | RF: 27 Must, 3 Should y 6 Could. RNF: 22 Must y 5 Should. Coinciden entre SRS y matriz |
| Trazabilidad RF → CU | Idéntica en casos de uso y en la matriz |
| Catálogo de pruebas | 67 pruebas; todas las citadas existen; cada RF y cada RNF tiene al menos una |
| Puntuaciones de los ADR | Aritméticamente correctas en los diez |
| Estados de los ADR | Coherentes en todos los documentos |
| Vocabulario canónico | Sin términos obsoletos fuera de tablas de equivalencia y registros de cambios |

Se recomienda conservar estas comprobaciones como un script del repositorio (`scripts/`) y ejecutarlas antes de cada cambio de línea base.

---

# 4. Hallazgos

Gravedad: **Alta**, **Media** o **Baja**.

## 4.1 Hallazgos de la auditoría inicial

### Resueltos

| ID | Gravedad | Resumen | Resolución |
|---|---|---|---|
| H-01 | Alta | SRS desalineado con los ADR | SRS v4.0 alineado con ADR-001 a ADR-010 |
| H-03 | Alta | Restricciones del generador mal formuladas | ADR-005: restricciones R1 a R7 |
| H-04 | Media | «Salto moderado» de BPM no verificable | RF-13b: salto máximo configurable (OD-02) |
| H-07 | Alta | La evidencia principal dependía de un RF secundario | RF-29 pasa a Must; CU-11 pasa a caso crítico (OD-01) |
| H-08 | Alta | Sin soporte multi-motor | RF-07 a Must; motor activo (OD-04) |
| H-17 | Media | Sin mecanismo para la referencia de Rekordbox | RF-29b: XML de colección o CSV |
| H-19 | Alta | Pistas movidas, duplicadas y ausentes sin tratar | RF-09c y flujos de CU-02 y CU-07 |
| H-26 | Media | `PostgreSQLAdapter` y puertos mal ubicados en ADR-002 | ADR-002 corregido |
| H-22 | Media | Trazabilidad RNF ↔ pruebas incompleta | Matriz v3.0: 27 RNF con componente, ADR y prueba |

### Convertidos en ADR

| ID | Resumen | ADR |
|---|---|---|
| H-11 | Lenguaje, interfaz y empaquetado | ADR-008 |
| H-12 | Licencias y evaluación | ADR-007 y ADR-009 |
| H-38 | Identificación permanente de pistas | ADR-010 |

### Parcialmente resueltos o pendientes

| ID | Gravedad | Resumen | Estado | Siguiente paso |
|---|---|---|---|---|
| H-35 | Alta | Modelo de dominio completo | Parcial: entidades candidatas consolidadas | Diseño del dominio y validación de OD-07 |
| H-05 | Baja | Reformulación de RNF-18 | RNF-18 ya es medible (cociente ≤ 2,5, provisional) | Ratificar tras la prueba de concepto |
| H-20 | Media | Semántica de los géneros | Pendiente | Decisión de dominio (OD-06, OD-07) |
| H-21 | Media | Definición formal de las métricas de transición | Pendiente | Diseño del dominio |
| H-29 | Media | Métricas de evaluación | ADR-009 las define; falta ratificar umbrales | Prueba de concepto |
| H-32 | Media | Diseño detallado del solver COP | Pendiente | Diseño del dominio y prototipo |
| H-37 | Media | Modelo de concurrencia | ADR-004 impone un único escritor; falta el diseño | Diseño de infraestructura e interfaz |

### Aparcados

Se revisarán durante la implementación, la validación y la redacción final de la memoria: H-02, H-13, H-14, H-15, H-16, H-18, H-23, H-24, H-25, H-30, H-31, H-33, H-34, H-40, H-41, H-42 y H-43.

## 4.2 Hallazgos de la consolidación

### Resueltos

| ID | Gravedad | Resumen | Resolución |
|---|---|---|---|
| N-01 | Alta | Faltaban ADR-007 a ADR-009 | Redactados como propuestos |
| N-02 | Alta | M3U8 de setlists sin requisito | RF-21b |
| N-05 | Alta | READMEs incoherentes con las decisiones | README principal y de arquitectura reescritos |
| N-06 | Alta | Nombres de puertos distintos según el documento | Vocabulario canónico (SRS 7.0, glosario 8) |
| N-07 | Alta | ADR-005 formulaba CSP cuando el problema es COP | ADR-005 revisado; ubicación del solver definida |
| N-08 | Alta | La matriz no trazaba RNF ni ADR | Matriz v3.0 |
| N-09 | Media | Cabeceras y fechas incoherentes en el SRS | SRS v4.0 |
| N-10 | Media | Los ADR no citaban requisitos | Sección de requisitos relacionados y trazabilidad en cada ADR |
| N-11 | Media | `PostgreSQLAdapter` en ADR-002 | Eliminado |
| N-12 | Media | Puertos fuera de la capa de Aplicación | ADR-002 y diagrama corregidos |
| N-13 | Media | RF-07 era Should pero sustenta requisitos Must | RF-07 a Must; RF-03 ampliado |
| N-14 | Media | Recuentos y asignaciones erróneos en matriz y SRS | Corregidos |
| N-15 | Media | Casos de uso sin flujos alternativos | CU-01, CU-02, CU-05, CU-07 y CU-11 completados |

### Resueltos en la segunda auditoría

| ID | Gravedad | Resumen | Resolución |
|---|---|---|---|
| N-18 | Alta | Los ADR citaban pruebas `T-RNF-xx` inexistentes en la matriz | Citas reasignadas al catálogo real |
| N-19 | Alta | Las pruebas T-ID de ADR-010 no estaban en la matriz | Sección 9.8; 67 pruebas |
| N-20 | Media | Sin puerto para referencias e informes de evaluación | `EvaluationRepository` propuesto en todos los documentos |
| N-21 | Media | RNF-09 omitía la tonalidad paralela | Alineado en SRS, glosario, casos de uso y ADR-009 |
| N-22 | Baja | RNF-12 ausente de la tabla de capas del SRS | Añadido |

### Abiertos

| ID | Gravedad | Resumen | Impacto | Propuesta |
|---|---|---|---|---|
| N-03 | Alta | Identidad acústica frente al rendimiento de reescaneo (RNF-04) | Dominio y persistencia | ADR-010 propone dos niveles. Pendiente de OD-03 y de la prueba de identificación |
| N-04 | Alta | Licencias e instalación de las librerías candidatas | Elección de motor, empaquetado y distribución | Verificar en la prueba de concepto (ADR-003, ADR-007). Hipótesis sin comprobar |
| N-16 | Media | ADR aceptados antes de la prueba de concepto, contra el plan del anteproyecto | Planificación y memoria | Registrar la desviación en la memoria (4.4) |
| N-17 | Media | `Transition` y `Library` con definiciones distintas según el documento | Modelo de dominio | Resolver con OD-05, OD-06 y OD-07 |
| N-23 | Baja | Existen dos versiones del README de arquitectura | Documentación | Conservar una sola |
| N-24 | Baja | Anotaciones de la consolidación en filas fechadas el 2026-10-30 | Trazabilidad documental | Unificar al congelar la línea base |

### Detectados durante la redacción de los ADR

| ID | Gravedad | Resumen | Impacto | Propuesta |
|---|---|---|---|---|
| N-25 | Alta | El repositorio conserva `backend`, `frontend` y `database`, propios de una arquitectura cliente-servidor descartada | Estructura y mantenibilidad | Reorganizar según la estructura de ADR-008 antes de escribir código |
| N-26 | Media | La entidad `Track` de OD-07 tiene un único campo `fingerprint`; ADR-010 requiere al menos dos huellas | Modelo de dominio y de datos | Revisar `Track` y `TrackLocation` en el diseño del dominio |
| N-27 | Media | La memoria (4.1.3, 4.4 y 4.6) describe 29 RF y todas las decisiones como abiertas | Memoria | Actualizar (sección 7) |
| N-28 | Media | El límite de la búsqueda se expresa en nodos (determinismo, RNF-11) mientras RNF-03 exige 60 s | Calibración del generador | Calibrar con el benchmark |
| N-29 | Media | El intervalo de género por instante de inicio es un supuesto de ADR-005 que afecta a RF-15 | Dominio | Confirmar en el diseño del dominio |
| N-30 | Baja | Los números de riesgo del documento anterior (R-01 a R-04) no coincidían con los de la memoria | Coherencia | Se adopta la numeración de la memoria (sección 5) |

---

# 5. Riesgos abiertos

Numeración de la memoria (capítulo 4, tabla 4.2). Los riesgos R-11 a R-13 son propuestas y deben añadirse a la memoria.

| ID | Riesgo | Prob. | Impacto | Estado | Mitigación | Documentos |
|---|---|---|---|---|---|---|
| R-01 | Exactitud insuficiente de BPM y tonalidad | Alta | Alto | Abierto | Prueba de concepto comparativa; desglose de errores; analizador sustituible | ADR-003, ADR-009 |
| R-02 | El fichero exportado no se carga en Rekordbox | Media | Alto | Abierto | Prueba de importación; verificación manual registrada | ADR-006 |
| R-03 | Etiquetas de género incompletas | Alta | Medio | Abierto | RF-15 es Should; promoción según calidad medida | RF-15, ADR-005 |
| R-04 | La referencia de Rekordbox no es una verdad absoluta | Media | Medio | Mitigado en diseño | Discusión en la evaluación; contraste con conjunto público; auditoría manual | ADR-009 |
| R-05 | Ampliación excesiva del alcance | Alta | Alto | **Vigilar** | RF-09c, RF-13b, RF-29b y RNF-27 amplían el anteproyecto; consultar a los tutores | SRS 9.1 |
| R-06 | Redacción concentrada al final y solapada con la validación | Alta | Alto | Abierto | Memoria incremental. ADR-009 añade carga a la fase de pruebas | Memoria 4.4 |
| R-07 | El generador no encuentra solución o su coste crece en exceso | Media | Medio | Abierto | Prototipo y benchmark; repliegue a Beam Search | ADR-005 |
| R-08 | Licencias incompatibles con la del repositorio | Media | Medio | Abierto | Inventario y política de ADR-007 | ADR-007 |
| R-09 | Poca disponibilidad de DJs para la valoración | Media | Medio | Abierto | Plan alternativo con métricas objetivas | ADR-009 |
| R-10 | Decisiones tecnológicas tardías que bloquean el diseño | Media | Alto | **Activo** | Cierre tras la prueba de concepto; supuestos explícitos en el diseño | ADR-003 a ADR-010 |
| R-11 | La instalación de las librerías MIR falla en Windows o macOS **(propuesto)** | Media | Alto | Abierto | Verificación en la prueba de concepto; adaptadores sustituibles | ADR-003, ADR-008 |
| R-12 | La identificación de pistas incumple RNF-04 o fusiona pistas distintas **(propuesto)** | Media | Alto | Abierto | Dos niveles; preferir el falso negativo; prueba de identificación | ADR-010 |
| R-13 | El modelo de datos se congela antes de validar las decisiones abiertas **(propuesto)** | Media | Alto | **Activo** | Supuestos explícitos; migraciones desde el primer esquema (RNF-27) | ADR-004 |

---

# 6. Hipótesis sin verificar

Ninguna de estas afirmaciones está comprobada. Cada una tiene un documento y un momento de verificación.

| Hipótesis | Dónde se usa | Verificación |
|---|---|---|
| Essentia tiene licencia copyleft fuerte y puede no instalarse con facilidad en Windows | ADR-003, ADR-007 | Prueba de concepto y lectura de la licencia vigente |
| Los modelos de madmom tienen restricciones de uso no comercial | ADR-003, ADR-007 | Ídem |
| Mutagen tiene licencia copyleft | ADR-003, ADR-007 | Ídem |
| El XML de colección de Rekordbox contiene BPM y tonalidad por pista | SRS 2.4, RF-29b, ADR-009 | Prueba de concepto |
| Formato de rutas, codificación y esquema de validación del XML de Rekordbox | ADR-006 | Prueba de importación |
| Los costes de identificación de ADR-010 (órdenes de magnitud) | ADR-010 | Medición en la prueba de identificación |
| Licencia de la interfaz gráfica y del empaquetador | ADR-007, ADR-008 | Verificación de licencias |
| Normativa de la UAH sobre propiedad intelectual de los TFG | ADR-007 | Lectura de la normativa |
| Correspondencia entre issues de GitHub y casos de uso | Matriz, sección 8 | Revisión del tablero |

---

# 7. Estado de la memoria

| Capítulo o sección | Estado | Actualización necesaria |
|---|---|---|
| 1 Introducción | Redactado | Coherente con la línea base |
| 2 Estado del arte | Redactado | Sin cambios; Music.py ya figura como descartada para el análisis |
| 3 Fundamentos teóricos | Redactado | Sin cambios |
| 4.1.3 Gestión de requisitos | Redactado | Actualizar recuentos (36 RF y 27 RNF) |
| 4.4 Seguimiento y desviaciones | Redactado | Registrar que los ADR se aceptaron antes de la prueba de concepto (N-16) y las ampliaciones de requisitos |
| 4.5 Gestión de riesgos | Redactado | Añadir R-11 a R-13 |
| 4.6 Gestión de decisiones | Redactado | Sustituir «todas abiertas» por el estado de los diez ADR |
| 5 a 9 y apéndices | Sin redactar | Se alimentan de los ADR (sección «Impacto en la memoria» de cada uno) |

---

# 8. Dependencias de diseño

## 8.1 Qué condiciona el modelo de dominio

| Elemento | Origen |
|---|---|
| Identidad de pista, ubicaciones y huellas | OD-03, ADR-010, RF-09, RF-09c |
| Resultados de análisis por motor y versión | OD-04, RF-07 |
| Existencia de `Library` | OD-05 |
| Evaluación de transiciones | OD-06, RF-17, RF-20, RF-20b |
| Conjunto de entidades y nombres | OD-07 |
| Restricciones R1 a R7, función de coste y semilla | ADR-005, RF-12 a RF-19 |

## 8.2 Qué condiciona el modelo de datos

| Elemento | Origen |
|---|---|
| Todo lo anterior | Dominio |
| Índice de reconocimiento de pistas conocidas | RNF-04, ADR-010 |
| Consultas sobre el motor activo | RF-11, RF-11b, OD-04 |
| Atomicidad y claves foráneas | RNF-17, ADR-004 |
| Rutas como texto Unicode | RNF-16, RNF-21 |
| Migraciones versionadas | RNF-27 |
| Un único escritor | ADR-004 |
| Reproducibilidad de setlists | RF-10, RNF-11 |
| Referencias e informes de evaluación | RF-29, RF-29b, ADR-009 |

## 8.3 Decisiones abiertas que condicionan el diseño

El detalle, las alternativas y las cuestiones para la reunión figuran en `open-decisions.md`.

| ID | Decisión | Prioridad | ¿Bloquea el modelo? | Estado |
|---|---|---|---|---|
| OD-01 | RF-29 (evaluación frente a Rekordbox) como Must | Alta | No | Propuesta incorporada |
| OD-02 | Salto máximo de BPM como parámetro | Alta | No | Propuesta incorporada |
| OD-03 | Identificación permanente de pistas (ADR-010) | Crítica | **Sí** | Propuesta incorporada |
| OD-04 | Resultados de varios motores por pista | Crítica | **Sí** | Propuesta incorporada |
| OD-05 | Entidad `Library` | Alta | **Sí** | Propuesta incorporada |
| OD-06 | Persistencia de transiciones | Crítica | **Sí** | Abierta |
| OD-07 | Conjunto de entidades de dominio | Crítica | **Sí** | Propuesta incorporada |
| OD-08 | Estado de ADR-007 a ADR-010 | Media | No | Pendiente de validación |
| OD-09 | Motor MIR definitivo | Media | No | Condicionada a la prueba de concepto |
| OD-10 | Protocolo de evaluación final | Media | No | Propuesta incorporada (ADR-009) |

Ninguna decisión ha sido validada todavía por tutor y cotutor.

---

# 9. Próximas acciones

| Prioridad | Acción | Responsable |
|---|---|---|
| 1 | Reunión con tutor y cotutor para validar OD-01 a OD-10 y las cuestiones adicionales | Autor |
| 2 | Diseño del modelo de dominio con los supuestos de la sección 8 | Autor |
| 3 | Diseño del modelo conceptual, el MER, el modelo relacional y el diseño físico de SQLite (`data-model.md`) | Autor |
| 4 | Reorganizar el repositorio según ADR-008 y eliminar `backend`, `frontend` y `database` (N-25) | Autor |
| 5 | Prueba de concepto: análisis, importación en Rekordbox, identificación, interfaz y empaquetado | Autor |
| 6 | Actualizar la memoria (sección 7) | Autor |
| 7 | Guardar el script de comprobación documental en `scripts/` | Autor |

---

# 10. Veredicto

| Cuestión | Respuesta |
|---|---|
| ¿Está cerrado el análisis? | **Sí**, a nivel de línea base documental. Pendiente de validación por tutores |
| ¿Está cerrada la arquitectura de alto nivel? | **Sí**, con las condiciones de la sección 3.2 |
| ¿Quedan contradicciones graves entre los documentos? | **No.** Quedan hallazgos menores y los de la sección 4.2, ninguno bloquea el diseño |
| ¿Está validada la línea base por los tutores? | **No** |
| ¿Se ha verificado con datos reales? | **No.** La prueba de concepto está pendiente |
| ¿Puede comenzar el diseño del dominio y del modelo de datos? | **Sí, en modo provisional**, con supuestos explícitos. No puede congelarse hasta validar OD-03 a OD-07 |

El siguiente paso del proyecto es el **diseño del modelo de dominio** y, a continuación, el del modelo de datos.

---

# 11. Control de cambios

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-10 | Auditoría técnica inicial |
| 2.0 | 2026-11-04 | Actualización tras la consolidación documental |
| 3.0 | 2026-11-05 | Reescritura completa: estado de madurez, línea base, segunda auditoría, hallazgos resueltos y abiertos (N-01 a N-30), riesgos con la numeración de la memoria (R-11 a R-13 propuestos), hipótesis sin verificar, estado de la memoria, dependencias de diseño y veredicto |
| 3.1 | 2026-11-06 | Revisión de la v3.0 contra la línea base (identificadores y cifras comprobados); se añade el resumen de decisiones abiertas (sección 8.3) |
