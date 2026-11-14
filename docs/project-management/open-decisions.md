# Decisiones Pendientes de Validación

> Destino en el repositorio: `docs/project-management/open-decisions.md`.

**Proyecto:** SetlistGen
**Versión:** 3.2 (actualización previa a la reunión con tutor y cotutor; sustituye a la 3.1)
**Fecha:** 2026-11-14
**Estado:** documento de trabajo para la reunión con Óscar Gutiérrez Blanco (tutor) y Ángel Javier Álvarez Miguel (cotutor)

---

# 1. Objetivo y uso

Este documento reúne las decisiones que siguen abiertas y que dependen de tutor y cotutor. Está pensado para usarse **durante la reunión**: cada decisión indica el **supuesto que el diseño detallado ya aplica**, el **coste de cambiarlo** si se rechaza, las alternativas y las cuestiones concretas. Los apartados «Resultado» se rellenan en la reunión.

Reglas de uso:

- Un supuesto marcado **[SUPUESTO · OD-xx]** en el resto de la documentación **no cierra** la decisión. Queda como hipótesis explícita hasta su validación.
- Las decisiones técnicas que el autor ha tomado durante el diseño y que **no** requieren validación se listan aparte (sección 7) para que los tutores conozcan su existencia.
- «Coste de cambio» estima el trabajo de reajustar documentos, esquema y código de especificación si se rechaza el supuesto. Es una estimación del autor, no una medición.

## 1.1 Estado general

| Concepto | Estado |
|---|---|
| Análisis (requisitos, casos de uso, matriz, glosario) | Cerrado a nivel de línea base (SRS v4.0, casos de uso v1.1, matriz v3.0, glosario v2.1) |
| Arquitectura de alto nivel | Cerrada (ADR-001 a ADR-006 aceptados) |
| Diseño detallado | **Completado de forma provisional**: dominio v0.2, modelo conceptual v0.1, MER v0.1.2, esquema SQLite v0.1.1, índice `data-model.md` v1.0.1 |
| ADR-007 a ADR-010 | Redactados como propuestos, sin validar |
| Estructura del repositorio | `src/setlistgen/` ya aplicada por el autor (propuesta de ADR-008, **OD-08 sin validar**) |
| Prueba de concepto (hito H2) | No realizada |
| Código en `src/` | Ninguno. El dominio existe como especificación ejecutable en `domain-model.md` |
| Decisiones validadas por tutores | **Ninguna todavía** |
| Siguiente fase | Reunión → cierre de ODs → congelar línea base documental y modelo de datos → memoria e implementación |

## 1.2 Cambios respecto a la versión 3.1

| Cambio | Motivo |
|---|---|
| Cada OD indica el **supuesto aplicado** en el diseño detallado y el **coste de rechazarlo** | Preparar la reunión |
| Nueva sección 7: decisiones derivadas del diseño (DD-01 a DD-17) | Hay decisiones nuevas que los tutores deben conocer o validar |
| OD-06: el autor adopta la instantánea como supuesto | Decisión del autor, pendiente de validación |
| Sustituida la antigua sección «Preparación para el modelo de dominio» | Ya existe el diseño; véase `docs/architecture/data-model.md` |
| Cuestiones nuevas en OD-03, OD-04, OD-08 y OD-10 | Surgieron durante el diseño |
| Nueva cuestión C-06 sobre la política de ramas | Contenido provisional ya presente en `main` |

---

# 2. Resumen ejecutivo

| ID | Decisión | Prioridad | Supuesto aplicado en el diseño | Coste de rechazo | Estado |
|---|---|---|---|---|---|
| OD-01 | RF-29 (evaluación frente a Rekordbox): Should o Must | Alta | Must; agregado Evaluación completo | Bajo a medio | Supuesto aplicado |
| OD-02 | Salto máximo de BPM como parámetro | Alta | Parámetro en BPM absolutos, 5 por defecto (P) | Bajo | Supuesto aplicado |
| OD-03 | Identificación permanente de pistas | **Crítica** | Dos niveles (ADR-010); huellas por pista | Medio | Supuesto aplicado |
| OD-04 | Resultados de varios motores por pista | **Crítica** | Varios resultados indivisibles; motor activo global | **Alto** | Supuesto aplicado |
| OD-05 | Entidad `Library` | Alta | No modelada; migración 2 condicional preparada | Bajo | Supuesto aplicado |
| OD-06 | Persistencia de transiciones | **Crítica** | **Instantánea** (decisión del autor) | Medio | Supuesto aplicado |
| OD-07 | Conjunto de entidades de dominio | **Crítica** | Cuatro agregados, entidades de `domain-model.md` | Medio a alto | Supuesto aplicado |
| OD-08 | Estado de ADR-007 a ADR-010 y estructura del repositorio | Media | Estructura `src/` aplicada; Python ≥ 3.10; SQLite ≥ 3.37 | Bajo (estructura) | Pendiente |
| OD-09 | Motor MIR definitivo | Media | Motor genérico (`EngineRef`); sin librería fijada | Ninguno | Condicionada a la PoC |
| OD-10 | Protocolo de evaluación final | Media | `scope_label`; fallos en el denominador; trazabilidad por pista fuera de la base | Bajo | Supuesto aplicado |

**Ninguna decisión está validada.** Las cinco críticas para congelar el modelo siguen siendo **OD-03, OD-04, OD-05, OD-06 y OD-07**. Orden de resolución recomendado: OD-04 → OD-03 → OD-05 → OD-06 → OD-07.

## 2.1 Si el tiempo de la reunión es limitado

Orden por coste de cambio y efecto sobre la evidencia del TFG:

1. **OD-04** (coste alto) y **DD-05** (cambia cómo se calcula la exactitud).
2. **OD-03** (condiciona RNF-04 y la prueba de concepto).
3. **OD-06** y **DD-16** (la primera ya está aplicada en el esquema).
4. **OD-08** (estructura del repositorio ya modificada).
5. El resto puede cerrarse por escrito.

---

# 3. Orden del día propuesto

| Bloque | Tema | Decisiones |
|---|---|---|
| A | Alcance | OD-01, OD-02, C-01, C-02 |
| B | Dominio y persistencia | OD-04, OD-03, OD-05, OD-06, OD-07 |
| C | Decisiones complementarias | OD-08, OD-09, OD-10, C-03 a C-06 |
| D | Decisiones derivadas del diseño | DD-04, DD-05, DD-11, DD-12, DD-15, DD-16, DD-17 (el resto, solo informar) |
| E | Planificación | Orden de la prueba de concepto, calendario de la memoria (R-06, R-10) |

---

# 4. Decisiones del bloque A: alcance

## OD-01 · Prioridad de la evaluación frente a Rekordbox

**Contexto.** RNF-05 a RNF-09 (Must) dependen de RF-29. El objetivo O7 del anteproyecto consiste en evaluar el sistema.

**Supuesto aplicado.** RF-29 es Must, CU-11 es caso crítico y existe RF-29b. En el diseño: agregado Evaluación (`ReferenceMeasurement`, `EvaluationReport`), servicios `ReferenceMatchingService`, `EvaluationService` y `EstimationErrorClassifier`, y cuatro tablas (`reference_measurement`, `evaluation_report`, `evaluation_error_count`, `evaluation_exclusion`).

| Alternativa | Ventajas | Inconvenientes |
|---|---|---|
| A1. Mantener Should | Menor alcance obligatorio | Debilita la validación experimental |
| A2. Promover a Must | Alinea requisitos funcionales y no funcionales | Incrementa el alcance mínimo |

**Coste de cambio si se rechaza.** Bajo a medio. Se revisan RF-29, RF-29b, CU-11, los recuentos de la matriz y ADR-009. El esquema no necesita migración: las cuatro tablas pueden permanecer sin uso.

**Cuestiones para la reunión.**
1. ¿Se acepta que la evaluación frente a Rekordbox sea parte del alcance mínimo?
2. ¿Se mantiene la valoración por DJs como objetivo condicionado («si es posible»)?

**Resultado:** ______________________________

---

## OD-02 · Salto máximo de BPM

**Contexto.** El anteproyecto pide un «salto de tempo moderado», no verificable.

**Supuesto aplicado.** RF-13b: parámetro `max_bpm_jump` en **BPM absolutos**, valor por defecto 5 (provisional), restricción R3. En el esquema: `generation_request.max_bpm_jump REAL CHECK (>= 0)`.

| Alternativa | Ventajas | Inconvenientes |
|---|---|---|
| A1. Interpretación interna | Menos parámetros | No verificable ni reproducible |
| A2. Parámetro explícito | Verificable; más control para el DJ | Un parámetro más |

**Coste de cambio.** Bajo. Eliminarlo implica revisar RF-13b, R3, RF-17, RNF-10, T-CU05-02, una columna y un campo del dominio. Pasar a un porcentaje obliga a cambiar el tipo o añadir una columna.

**Cuestiones para la reunión.**
1. ¿Se acepta un parámetro explícito?
2. ¿El valor por defecto es adecuado? ¿BPM absolutos o porcentaje? (El diseño asume absolutos.)

**Resultado:** ______________________________

---

## Cuestión C-01 · Requisitos que amplían el anteproyecto

La memoria (4.1.4) establece que todo requisito que exceda los objetivos se consulta con los tutores.

| Requisito | Deriva de | Motivo |
|---|---|---|
| RF-09c | O3 | Pistas movidas, duplicadas y ausentes |
| RF-13b | O4 | Hace verificable el «salto moderado» |
| RF-29b | O7 | Mecanismo para contrastar con Rekordbox |
| RNF-27 | O3 | Migraciones del esquema (ya implementadas en el esquema inicial) |

**Cuestión.** ¿Se aceptan estas cuatro ampliaciones? **Resultado:** ______________________________

## Cuestión C-02 · Pistas ausentes al exportar

CU-07 propone avisar y dejar elegir entre cancelar y continuar; si continúa, la pista conserva su última ubicación conocida. En el dominio existe `Track.last_known_location()`. Se confirma con la prueba de importación (R-02).

**Cuestión.** ¿Es aceptable como punto de partida? **Resultado:** ______________________________

---

# 5. Decisiones del bloque B: dominio y persistencia

## OD-04 · Resultados de varios motores por pista

**Contexto.** La arquitectura admite Essentia, librosa y madmom (ADR-003). RF-07 exige registrar motor y versión; RF-29 compara motores.

**Supuesto aplicado.**
- `AnalysisResult` es un **agregado propio**, enlazado a la pista por identidad, con puerto `AnalysisResultRepository` (DD-01).
- Un resultado es **indivisible**: BPM y tonalidad del mismo motor.
- Un motor es la pareja (nombre, versión) y es una **entidad** (`analysis_engine`); cada versión es un motor distinto, así que el histórico de versiones se conserva.
- El **motor activo** es global y vive en la configuración (`app_setting`). La solicitud de generación guarda el motor usado.
- Unicidad prevista por (pista, motor).

| Alternativa | Ventajas | Inconvenientes |
|---|---|---|
| A1. Un resultado por pista | Modelo simple | No permite evaluar motores sobre las mismas pistas |
| A2. Varios resultados por pista | Comparación entre motores; repetibilidad | Más complejidad en el modelo y las consultas |

**Coste de cambio si se rechaza: alto.**
- Dominio: `AnalysisResult` pasa a ser parte de `Track`; desaparece `EngineRef` de la solicitud; cambia el flujo de evaluación.
- Esquema: se reconstruye la unicidad de `analysis_result` (una por pista), se eliminan `analysis_engine` y `app_setting` o se vacían, y los índices por motor. Requiere migración con posible pérdida de resultados de otros motores.
- Documentos: ADR-002, ADR-003, ADR-004, glosario, CU-11 y pruebas T-CU01-06 y T-CU11-05.

**Cuestiones para la reunión.**
1. ¿Deben coexistir varios resultados por pista? *(el diseño responde que sí)*
2. ¿Se conserva el histórico de versiones de un mismo motor? *(sí, cada versión es un motor)*
3. ¿El motor activo es global, por biblioteca o por análisis? *(global)*
4. ¿Se permite combinar BPM de un motor y tonalidad de otro? *(no, el resultado es indivisible)*
5. ¿Se acepta que `TrackRepository` quede solo para Catálogo y se cree `AnalysisResultRepository` (DD-01)?

**Resultado:** ______________________________

---

## OD-03 · Identificación permanente de pistas

**Contexto.** RF-09 exige identidad independiente de nombre y ubicación. RNF-04 exige reescaneos rápidos (5 000 pistas en ≤ 2 min, provisional).

**Supuesto aplicado (ADR-010 y DD-15).**
- Identificación en **dos niveles**: nivel 1 (ubicación, tamaño y fecha; huella rápida) y nivel 2 (huella de contenido) solo para lo no reconocido.
- Las huellas son objeto de valor de la pista, con tipo y versión de algoritmo (`track_fingerprint`).
- `TrackRecognitionService` devuelve ocho resultados: `UNCHANGED`, `NEEDS_FINGERPRINT`, `MOVED`, `DUPLICATE`, `MODIFIED`, `AMBIGUOUS`, `NEW`, `UNREADABLE`. `NEEDS_FINGERPRINT` evita leer ficheros si tamaño y fecha coinciden.
- **Preferir el falso negativo** (un duplicado) al falso positivo (una fusión indebida).
- Una misma grabación en dos formatos son **dos pistas** (huella distinta).
- Fichero modificado en la misma ubicación: se conserva la identidad si la huella rápida coincide; si no, es una pista nueva y la anterior queda ausente.
- Una ruta normalizada solo puede tener una ubicación vigente (índice único parcial).

| Alternativa | Ventajas | Inconvenientes |
|---|---|---|
| A1. Hash del fichero | Sencillo y exacto | Cambia al editar etiquetas; lectura completa |
| A2. Hash del audio | Independiente de etiquetas | Exige descodificar |
| A3. Fingerprint acústico | Tolera recodificación | Exige descodificar; umbrales; dependencia con licencia por verificar |
| A4. Dos niveles | Compatible con RNF-04 | Mayor complejidad; técnica del nivel 2 por decidir |

**Coste de cambio.** Medio.
- Si las huellas pasan a la ubicación: migración con copia de datos de `track_fingerprint`, ajuste de `TrackIndex` y pruebas T-ID.
- Si se rechaza el esquema de dos niveles (A1 a A3): se sustituye `TrackRecognitionService` y se rediseña `track_fingerprint`.
- La técnica del nivel 2 queda abierta en cualquier caso y se decide con la prueba de identificación.

**Cuestiones para la reunión.**
1. ¿Es adecuada la identificación en dos niveles?
2. **Alcance de la identidad.** Una grabación en WAV y en MP3: ¿una pista o dos? *(el diseño asume dos)*
3. **Fichero modificado en la misma ubicación (CU-02, A3).** ¿Se acepta la política descrita arriba?
4. ¿Se acepta decidir la técnica del nivel 2 con las medidas de la prueba de identificación?
5. ¿Debe el sistema permitir gestionar duplicados o basta con informar?
6. ¿Se acepta que las huellas sean por pista y no por ubicación?

**Resultado:** ______________________________

---

## OD-05 · Entidad `Library`

**Contexto.** Con `TrackLocation`, la pertenencia a una biblioteca se establece por la ubicación.

**Supuesto aplicado.** `Library` **no entra** en el dominio v0.2 ni en la migración 1. Está preparada la **migración 2 condicional** (`migrations/pending/0002_library_od05.sql`): crea la tabla `library` y añade `track_location.library_id` (nullable, `ON DELETE SET NULL`) sin reconstruir tablas. Probada sobre la migración 1.

| Alternativa | Ventajas | Inconvenientes |
|---|---|---|
| A1. Mantener | Varias bibliotecas, histórico de importaciones, estadísticas por biblioteca | Más complejidad |
| A2. Eliminar | Simplificación | El panel no podría separar colecciones |

**Coste de cambio.** **Bajo.** Aceptar la entidad = aplicar la migración 2 y añadir la entidad al dominio. Rechazarla = nada que migrar.

**Cuestiones para la reunión.**
1. ¿Se soporta una o varias bibliotecas?
2. ¿Una biblioteca corresponde a una carpeta raíz importada?
3. ¿Las estadísticas del panel son por biblioteca o globales?
4. ¿Hace falta un **histórico de importaciones**? Hoy el informe de importación no se persiste (DD-11).

**Resultado:** ______________________________

---

## OD-06 · Persistencia de transiciones

**Contexto.** RF-17 y RF-20 exigen evaluar y mostrar cada transición; RF-20b permite reordenar manualmente. Si cambia el motor activo o se editan etiquetas, un setlist antiguo podría mostrar valores distintos.

**Supuesto aplicado (decisión del autor, pendiente de validación).** **Instantánea.**
- `setlist_track` congela BPM, código Camelot, duración y género de cada pista en el momento de generar.
- `transition` guarda la evaluación (salto de BPM, distancia Camelot, compatibilidad, incoherencia de género y coste). Origen y destino se deducen de la posición.
- Al **editar**: las transiciones se recalculan con las instantáneas, `edited = true`, `optimality = not_proven` y cada entrada conserva su posición generada en `original_position`.

| Alternativa | Ventajas | Inconvenientes |
|---|---|---|
| A1. Recalcular siempre | Siempre consistente con el orden actual | Un setlist histórico puede mostrar valores distintos de los que tenía |
| A2. Instantánea | Histórico estable y reproducible; sirve a RF-27 | Más datos; hay que recalcular al editar |
| A3. Solo agregados | Simple | No permite revisar el detalle |

**Coste de cambio.** Medio. Si se elige A1: se eliminan la tabla `transition` y las columnas de instantánea de `setlist_track` (migración), se quita `Setlist.transitions` y las instantáneas del dominio, y se calcula con `TransitionEvaluatorService` al consultar. Afecta a RF-10, RF-20, RF-20b, RF-27, ADR-004 y T-CU08-01.

**Cuestiones para la reunión.**
1. ¿Debe un setlist histórico conservar la evaluación que tenía al generarse? *(el diseño responde que sí)*
2. Tras una edición manual, ¿se conserva la secuencia original? *(sí, mediante `original_position`)*
3. ¿Qué datos de la transición se conservan? *(los cinco indicados)*

**Resultado:** ______________________________

---

## OD-07 · Modelo de dominio definitivo

**Contexto.** El modelo se diseñó a partir de las entidades candidatas y se detalla en `domain-model.md` y la serie de datos.

**Supuesto aplicado.**
- Cuatro agregados: Catálogo, Análisis, Generación y Evaluación, referenciados solo por identidad.
- `AnalysisRun` desaparece: motor y versión se absorben en `EngineRef` (entidad `AnalysisEngine` en la base) (DD-02).
- `GenerationRequest` es parte de `Setlist`: regenerar crea otro setlist (DD-03).
- `TrackMetadata` es objeto de valor; las huellas son objetos de valor de `Track` (N-26).
- `Transition` es un objeto de valor calculado; `Library`, fuera (OD-05).
- Puertos: se añade `AnalysisResultRepository`; `TrackRepository` solo para Catálogo (DD-01). Se mantienen las propuestas `EvaluationRepository` y `TrackIdentifier`.

**Coste de cambio.** Medio a alto, según la entidad. Cada cambio se propaga: dominio → conceptual → MER → esquema → migración (`data-model.md`, sección 6).

**Cuestiones para la reunión.**
1. ¿Representan estas entidades correctamente el dominio?
2. ¿`TrackMetadata` como objeto de valor o entidad?
3. ¿Se acepta la separación de huellas (N-26) y el puerto `EvaluationRepository`?
4. **Intervalo de género (ADR-005).** Una pista pertenece al intervalo en el que empieza. El validador ya lo implementa. ¿Es el criterio adecuado para RF-15?
5. ¿Se acepta que la solicitud de generación sea parte del setlist (1 a 1)?

**Resultado:** ______________________________

---

# 6. Decisiones del bloque C: complementarias

## OD-08 · Estado de ADR-007 a ADR-010 y estructura del repositorio

**Contexto.** Los cuatro ADR existen como propuestos. Además, el autor **ya ha aplicado** en el repositorio la estructura de paquetes de ADR-008 (`src/setlistgen/`), eliminando `backend/`, `frontend/` y `database/`, y la línea base provisional está en `main` y `develop`.

| ADR | Propuesta | Condición |
|---|---|---|
| ADR-007 | Núcleo con dependencias permisivas y adaptadores opcionales para licencias restrictivas | Inventario verificado y PoC |
| ADR-008 | Python, PySide6 (alternativa Tkinter), distribución en dos niveles y estructura de paquetes | PoC de interfaz y empaquetado; licencias |
| ADR-009 | Muestra estratificada con contraste público | PoC |
| ADR-010 | Identificación en dos niveles | Es la propuesta de OD-03 |

**Supuestos aplicados que añaden a ADR-008.**
- Python **3.10 o superior** (el dominio v0.2 se ha ejecutado en 3.12, no en 3.10).
- SQLite **3.37 o superior** (tablas `STRICT`) y modo `WAL` como propuesta.
- Las migraciones viven **dentro del paquete** (`infrastructure/persistence/migrations/`, con `pending/` para las condicionales) y los tests tienen `architecture/` y `performance/`. ADR-008 no lo recoge todavía (N-57).

**Coste de cambio.** Bajo para la estructura: no hay código, basta con `git mv`. Medio si cambia el mínimo de SQLite (hay que quitar `STRICT` y reforzar con `CHECK`).

**Cuestiones para la reunión.**
1. ¿Se mantienen, modifican o consolidan estos ADR?
2. **Licencia del repositorio (ADR-007).** `LICENSE` es MIT. ¿Se confirma?
3. **Distribución en dos niveles (ADR-008).** El nivel obligatorio es instalar desde código fuente, lo que puede perjudicar RNF-13. ¿Es aceptable como mínimo?
4. ¿Se valida la estructura `src/` ya aplicada y la ubicación de las migraciones dentro del paquete?
5. ¿Se acepta Python ≥ 3.10 y SQLite ≥ 3.37 como requisitos mínimos? Si el SQLite del sistema es anterior, el esquema no se crea.

**Resultado:** ______________________________

---

## OD-09 · Motor MIR definitivo

**Contexto.** ADR-003 desacopla el análisis mediante un puerto. La elección de librería depende de la prueba de concepto.

**Supuesto aplicado.** El diseño no fija ninguna librería: un motor es (nombre, versión). Cualquier candidata entra sin cambiar el modelo.

**Coste de cambio.** Ninguno en el modelo.

**Cuestiones para la reunión.**
1. ¿Se aprueba el protocolo de la prueba de concepto?
2. ¿Se acepta que se ejecute después de aceptar los ADR? (Desviación respecto al plan, N-16.)

**Resultado:** ______________________________

---

## OD-10 · Protocolo de evaluación final

**Contexto.** ADR-009 propone una muestra estratificada con referencia de Rekordbox, contraste público si es accesible y separación entre piloto y muestra reservada.

**Supuesto aplicado.**
- `EvaluationReport` identifica el ámbito con `scope_label` (piloto, reservada, estrato).
- **Un fallo de estimación cuenta en el denominador** de cada métrica y se informa aparte (DD-05). Una pista sin resultado del motor se **excluye** (CU-11 A4).
- El informe guarda conteos y desglose de errores; el detalle por pista no se persiste en la base y vive en el **manifiesto** de ADR-009 (DD-12).
- Las referencias sin pista, las ambiguas y las pistas sin referencia se guardan como exclusiones.

**Coste de cambio.** Bajo. Cambiar el tratamiento de fallos afecta a un cálculo del dominio y a las pruebas, no al esquema. Guardar el detalle por pista exigiría una tabla nueva.

**Cuestiones para la reunión.**
1. Tamaño mínimo de la muestra. La propuesta es 300 pistas.
2. ¿Se acepta la separación estricta entre piloto y muestra reservada?
3. Valoración por DJs: ¿cuántos participantes y cómo se localizan? ¿Comparación a ciegas con setlists aleatorios?
4. ¿Se acepta una auditoría manual de una submuestra de discrepancias?
5. **Fallos de estimación (DD-05, N-52).** ADR-009 excluye «ficheros ilegibles». ¿Se acepta distinguir entre fichero ilegible para todos los motores (excluido) y fallo propio de un motor (cuenta como fallo)?

**Resultado:** ______________________________

---

## Cuestión C-03 · Desviaciones del plan

La prueba de concepto precede a la arquitectura en el plan, pero los ADR se aceptaron antes de realizarla (N-16). Además, la reorganización del repositorio y la línea base provisional se han consolidado antes de validar OD-08 (N-56).

**Cuestión.** ¿Se acepta registrar ambas desviaciones en la memoria (4.4)? **Resultado:** ______________________________

## Cuestión C-04 · Estructura del repositorio

Ya aplicada: `src/setlistgen/`, sin `backend/`, `frontend/` ni `database/`. Los documentos están integrados. Es parte de OD-08, cuestión 4.

**Cuestión.** ¿Se valida o se pide un cambio? **Resultado:** ______________________________

## Cuestión C-05 · Disponibilidad de DJs

Riesgo R-09. **Cuestión.** ¿Hay candidatos para la valoración? ¿Se prepara el plan alternativo? **Resultado:** ______________________________

## Cuestión C-06 · Política de ramas con contenido provisional

`main` ya contiene diseño provisional, mientras la memoria (4.2.1) describe esa rama como la de versiones estables. Se propone marcar el estado con etiquetas: `baseline-provisional-2026-11-14` ahora y `baseline-v1` cuando los tutores validen.

**Cuestión.** ¿Es aceptable? **Resultado:** ______________________________

---

# 7. Decisiones derivadas del diseño detallado

Decisiones que surgieron al diseñar el dominio, el modelo y el esquema. Las marcadas **Sí** se plantean a los tutores; las marcadas **No** son técnicas y solo se informa.

| ID | Decisión | Origen | ¿Valida el tutor? | Coste de cambio |
|---|---|---|---|---|
| DD-01 | `AnalysisResult` agregado propio y puerto `AnalysisResultRepository`; `TrackRepository` solo Catálogo | N-32, OD-04 | **Sí**, con OD-04 | Medio: ADR-002 y ADR-004 |
| DD-02 | `AnalysisRun` desaparece; `EngineRef` en el dominio y `analysis_engine` en la base | N-31 | No | Bajo |
| DD-03 | `GenerationRequest` dentro de `Setlist` (regenerar = nuevo setlist) | OD-07 | **Sí**, con OD-07 | Bajo a medio |
| DD-04 | `allowed_keys` como **pre-filtro** de candidatas (RF-14), sin restricción R8; una ancla excluida se informa como conflicto | RF-14, ADR-005 | **Sí** | Bajo |
| DD-05 | Un fallo de estimación **cuenta en el denominador** de las métricas y se informa aparte | RNF-05 a RNF-09, ADR-009 | **Sí** (metodológica) | Bajo en código, alto en la interpretación de resultados |
| DD-06 | Instantáneas de descriptores y transiciones | OD-06 | **Sí**, con OD-06 | Medio |
| DD-07 | Una ruta normalizada tiene una sola ubicación vigente (`active` o `failed`) | M-01 | No | Bajo |
| DD-08 | `camelot_code` como columna generada y almacenada | M-06 | No | Bajo |
| DD-09 | `rekordbox_version = 'unknown'` cuando no se conoce | M-05 | No | Bajo |
| DD-10 | Política armónica como tabla hija (`request_harmonic_move`) | M-02 | No | Bajo |
| DD-11 | El informe de importación no se persiste | M-03 | **Sí**, con OD-05 | Bajo a medio (tabla de importaciones) |
| DD-12 | La trazabilidad por pista de la evaluación vive en el manifiesto de ADR-009, no en la base | M-04 | **Sí**, con OD-10 | Medio |
| DD-13 | Estructura `src/` y migraciones dentro del paquete | N-25 | **Sí**, con OD-08 | Bajo |
| DD-14 | `Library` fuera de la migración 1; migración 2 condicional | OD-05 | **Sí**, con OD-05 | Bajo |
| DD-15 | Reconocimiento con `NEEDS_FINGERPRINT`; preferencia por el falso negativo; `AMBIGUOUS` sin fusionar | OD-03, ADR-010 | **Sí**, con OD-03 | Medio |
| DD-16 | El pre-filtro de candidatas **no** filtra por género (los segmentos pueden no cubrir todo el setlist) | N-48 | **Sí** | Bajo |
| DD-17 | Una pista sin duración no puede ser candidata (RF-12 necesita duración) | N-51 | **Sí** | Bajo |

**Cuestiones adicionales para la reunión.**
- **DD-16.** ADR-005 (aceptado) dice que la reducción previa filtra por «rango de BPM, género y disponibilidad». El dominio no filtra por género. ¿Se precisa ADR-005 (filtrar por género solo si los segmentos cubren toda la duración) o se implementa el filtro condicional?
- **DD-17.** RF-03 admite una duración nula. ¿Se obtiene la duración al decodificar el audio durante el análisis cuando falta la etiqueta, o se excluye la pista de la generación e informa al DJ?

**Resultado de DD-04, DD-05, DD-11, DD-12, DD-15, DD-16, DD-17:** ______________________________

---

# 8. Registro de resultados de la reunión

| ID | Resultado | Cambios en la documentación |
|---|---|---|
| OD-01 | | |
| OD-02 | | |
| OD-03 | | |
| OD-04 | | |
| OD-05 | | |
| OD-06 | | |
| OD-07 | | |
| OD-08 | | |
| OD-09 | | |
| OD-10 | | |
| C-01 a C-06 | | |
| DD-01, DD-03, DD-04, DD-05, DD-06 | | |
| DD-11 a DD-17 | | |

Fecha de la reunión: ____________ · Asistentes: ______________________________

---

# 9. Dependencias y mapa de cambio

## 9.1 Dependencias entre decisiones

| Decisión | Condiciona a | Motivo |
|---|---|---|
| OD-04 | OD-07, OD-01, OD-06, DD-01, OD-10 | Define `AnalysisResult`; la evaluación por motor depende de ella; si cambia el motor activo, las evaluaciones antiguas pueden variar |
| OD-03 | OD-07, OD-05, DD-15 | Define la identidad de `Track` y los campos de `TrackLocation`; la pertenencia a biblioteca se deduce de la ubicación |
| OD-05 | OD-07, DD-11, DD-14 | Determina si `Library` entra en el modelo y si hay histórico de importaciones |
| OD-06 | OD-07, RF-20b, RF-27, DD-06 | Determina si se persisten transiciones e instantáneas |
| OD-01 | OD-07, OD-10 | Si RF-29 deja de ser Must, las entidades de evaluación pasan a opcionales |
| OD-02 | Ninguna | Es un campo de la solicitud |
| OD-07 | Todo el modelo | Integra las anteriores |

**Orden de resolución recomendado:** OD-04, OD-03, OD-05, OD-06 y, por último, OD-07.

## 9.2 Qué se toca si una decisión cambia

`X` = requiere cambio; `·` = no.

| Decisión | `domain-model` | `conceptual` | `er-model` | `database-schema` + SQL | ADR | SRS / CU / glosario |
|---|---|---|---|---|---|---|
| OD-01 | `X` | `X` | `X` | `·` | ADR-009 | `X` |
| OD-02 | `X` | `·` | `X` | `X` | ADR-005 | `X` |
| OD-03 | `X` | `X` | `X` | `X` | ADR-010, ADR-004 | `X` |
| OD-04 | `X` | `X` | `X` | `X` (migración) | ADR-002, 003, 004 | `X` |
| OD-05 | `X` | `X` | `X` | `X` (migración 2) | ADR-004 | `X` |
| OD-06 | `X` | `X` | `X` | `X` (migración) | ADR-004 | `X` |
| OD-07 | `X` | `X` | `X` | `X` | ADR-002 | `X` |
| OD-08 | `·` | `·` | `·` | `·` | ADR-008, 007, 009 | `·` |
| OD-09 | `·` | `·` | `·` | `·` | ADR-003 | `·` |
| OD-10 | `X` | `·` | `·` | `·` | ADR-009 | `·` |

Orden de propagación y reglas: `docs/architecture/data-model.md`, sección 6. Una migración aplicada no se edita: se añade otra.

## 9.3 Riesgos para el modelo de datos

| ID | Riesgo | Origen | Mitigación aplicada |
|---|---|---|---|
| DM-01 | Cambiar la identidad de pista tras congelar el esquema obliga a migrar huellas e identificadores | OD-03, R-12 | Versión del algoritmo en cada huella; migraciones desde la primera versión |
| DM-02 | Las consultas por motor activo complican las uniones y pueden penalizar RNF-03 y RF-11b | OD-04 | Índices por motor en el esquema; candidatas en memoria al generar |
| DM-03 | Transiciones inconsistentes tras editar un setlist | OD-06 | Recalcular siempre al editar; marca de editado; `original_position` |
| DM-04 | Pertenencia a biblioteca por ubicación complica el histórico | OD-05 | Resolver OD-05 antes de congelar; migración 2 preparada |
| DM-05 | SQLite es permisivo con tipos y restricciones | ADR-004 | Tablas `STRICT`, `CHECK`, claves foráneas activas; pruebas de integridad |
| DM-06 | Un único escritor limita el análisis paralelo | ADR-004, H-37 | Un coordinador persiste los resultados (diseño pendiente) |
| DM-07 | Rutas con Unicode, espacios y longitud extrema | RNF-16 | Texto Unicode; normalización en el repositorio (N-37) |
| DM-08 | Reproducir un setlist exige semilla, motor, versión y pesos | RNF-11 | Guardados en `generation_request` |
| DM-09 | Las referencias dependen de que el XML de Rekordbox contenga BPM y tonalidad | RF-29b | Referencia independiente del origen; CSV alternativo |
| DM-10 | Un modelo muy detallado antes de validar OD-03 a OD-07 | R-13 | Marcado como provisional; migraciones |

---

# 10. Control de cambios

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-10 | Primer registro de decisiones abiertas |
| 2.0 | 2026-11-04 | Actualización tras la consolidación |
| 3.0 | 2026-11-05 | Reescritura como documento de trabajo para la reunión |
| 3.1 | 2026-11-06 | Revisión contra la línea base; sin cambios de contenido |
| 3.2 | 2026-11-14 | Previa a la reunión con tutores: supuestos aplicados y coste de cambio por OD; decisiones derivadas del diseño (DD-01 a DD-17); mapa de cambio por decisión; OD-06 adoptado por el autor como instantánea; cuestiones nuevas en OD-03, OD-04, OD-08 y OD-10; cuestión C-06; sustituida la sección «Preparación para el modelo de dominio» por el diseño detallado (`data-model.md`) |
