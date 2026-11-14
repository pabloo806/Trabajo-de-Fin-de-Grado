# Decisiones Pendientes de Validación

> Destino en el repositorio: `docs/architecture/open-decisions.md`.

**Proyecto:** SetlistGen
**Versión:** 3.1 (reescritura completa; sustituye a todas las versiones anteriores)
**Fecha:** 2026-11-06
**Estado:** documento de trabajo para la próxima reunión con tutor y cotutor

---

# 1. Objetivo y uso

Este documento reúne las decisiones que siguen abiertas tras cerrar la línea base documental. Está pensado para usarse **durante la reunión** con tutor y cotutor: cada decisión tiene su propuesta, sus alternativas, lo que ocurre si se rechaza y las cuestiones concretas que hay que resolver. El apartado de resultados se rellena en la reunión.

Reglas de uso:

- Una propuesta marcada **[PROPUESTA · OD-xx]** en el resto de la documentación **no cierra** la decisión. Queda como supuesto explícito hasta su validación.
- Solo figuran decisiones relevantes para el diseño del dominio y de la persistencia, o para el alcance.
- Las decisiones que estaban abiertas en versiones anteriores y han quedado absorbidas por un ADR se indican en su sección.

## 1.1 Estado general

| Concepto | Estado |
|---|---|
| Análisis | Cerrado a nivel de línea base |
| Arquitectura de alto nivel | Cerrada (ADR-001 a ADR-006 aceptados) |
| Propuestas de decisión incorporadas a la documentación | OD-01 a OD-07, como propuesta |
| ADR-007 a ADR-010 | Redactados como propuestos |
| Decisiones validadas por tutores | **Ninguna todavía** |
| Siguiente fase | Diseño del modelo de dominio y del modelo de datos |

---

# 2. Resumen ejecutivo

| ID | Decisión | Impacto | Prioridad | ¿Bloquea el modelo? | Estado | Propuesta inicial |
|---|---|---|---|---|---|---|
| OD-01 | RF-29 (evaluación frente a Rekordbox): Should o Must | Alcance mínimo y validación experimental | Alta | No | Propuesta incorporada | Must |
| OD-02 | Salto máximo de BPM como parámetro | Generador y validación | Alta | No | Propuesta incorporada | Parámetro configurable, 5 BPM por defecto |
| OD-03 | Identificación permanente de pistas | Dominio y persistencia | **Crítica** | **Sí** | Propuesta incorporada (ADR-010) | Dos niveles |
| OD-04 | Resultados de varios motores por pista | Dominio y modelo de datos | **Crítica** | **Sí** | Propuesta incorporada | Varios resultados y motor activo |
| OD-05 | Entidad `Library` | Modelo de dominio | Alta | **Sí** | Propuesta incorporada | Mantener la entidad |
| OD-06 | Persistencia de transiciones | Dominio y base de datos | **Crítica** | **Sí** | Abierta | Instantánea al generar, recalculada al editar |
| OD-07 | Conjunto de entidades de dominio | Dominio y persistencia | **Crítica** | **Sí** | Propuesta incorporada | Entidades de la sección 8.2 y 8.3 |
| OD-08 | Estado de ADR-007 a ADR-010 | Licencias, interfaz, evaluación e identidad | Media | No | Pendiente de validación | Aceptar tras la prueba de concepto |
| OD-09 | Motor MIR definitivo | Implementación futura | Media | No | Condicionada a la prueba de concepto | Decidir con los criterios de ADR-003 |
| OD-10 | Protocolo de evaluación final | Validación experimental | Media | No | Propuesta incorporada (ADR-009) | Muestra estratificada más contraste público |

Las cinco decisiones críticas para empezar el modelo son **OD-03, OD-04, OD-05, OD-06 y OD-07**. El diseño puede empezar con supuestos explícitos, pero no puede congelarse sin ellas.

---

# 3. Orden del día propuesto

| Bloque | Tema | Decisiones |
|---|---|---|
| A | Alcance | OD-01, OD-02, cuestiones C-01 y C-02 |
| B | Dominio y persistencia | OD-04, OD-03, OD-05, OD-06, OD-07 |
| C | Decisiones complementarias | OD-08, OD-09, OD-10, cuestiones C-03 a C-05 |
| D | Planificación | Orden de la prueba de concepto, calendario de la memoria (riesgos R-06 y R-10) |

El orden dentro del bloque B sigue las dependencias de la sección 8.4.

---

# 4. Decisiones del bloque A: alcance

## OD-01 · Prioridad de la evaluación frente a Rekordbox

**Contexto.** RNF-05 a RNF-09 (Must) dependen de RF-29. El objetivo O7 del anteproyecto consiste en evaluar el sistema. La evidencia principal del TFG no puede depender de un requisito secundario.

**Propuesta incorporada.** RF-29 pasa a Must. CU-11 pasa a caso crítico. Se añade RF-29b (importación de la referencia).

| Alternativa | Ventajas | Inconvenientes |
|---|---|---|
| A1. Mantener Should | Menor alcance obligatorio | Debilita la validación experimental |
| A2. Promover a Must | Alinea requisitos funcionales y no funcionales | Incrementa el alcance mínimo |

**Si se rechaza.** Revisar RF-29 y RF-29b, CU-11, los recuentos de la matriz, ADR-009 y la verificación de RNF-05 a RNF-09.

**Cuestiones para la reunión.**
1. ¿Se acepta que la evaluación frente a Rekordbox sea parte del alcance mínimo?
2. ¿Se mantiene la valoración por DJs como objetivo condicionado («si es posible»)?

**Resultado:** ______________________________

---

## OD-02 · Salto máximo de BPM

**Contexto.** El anteproyecto pide un «salto de tempo moderado», que no es verificable. RNF-10 exige el cumplimiento de las restricciones configuradas.

**Propuesta incorporada.** RF-13b: parámetro configurable. Valor por defecto provisional: 5 BPM. Restricción R3 de ADR-005.

| Alternativa | Ventajas | Inconvenientes |
|---|---|---|
| A1. Interpretación interna | Menos parámetros | No verificable ni reproducible |
| A2. Parámetro explícito | Verificable; más control para el DJ | Un parámetro más |

**Si se rechaza.** Eliminar RF-13b y R3; revisar RF-17, RNF-10 y T-CU05-02.

**Cuestiones para la reunión.**
1. ¿Se acepta un parámetro explícito?
2. ¿El valor por defecto es adecuado? ¿Debe expresarse en BPM absolutos o en porcentaje?

**Resultado:** ______________________________

---

## Cuestión C-01 · Requisitos que amplían el anteproyecto

La memoria (4.1.4) establece que todo requisito que exceda los objetivos del anteproyecto se consulta con los tutores antes de incorporarse.

| Requisito | Deriva de | Motivo |
|---|---|---|
| RF-09c | O3 | Consecuencia de RF-09 (pistas movidas, duplicadas y ausentes) |
| RF-13b | O4 | Hace verificable el «salto moderado» |
| RF-29b | O7 | Mecanismo necesario para contrastar con Rekordbox |
| RNF-27 | O3 | Migraciones del esquema |

**Cuestión.** ¿Se aceptan estas cuatro ampliaciones? **Resultado:** ______________________________

## Cuestión C-02 · Pistas ausentes al exportar

CU-07 propone avisar y dejar elegir entre cancelar o continuar. Si continúa, las pistas se mantienen con su última ubicación conocida. Se confirma con la prueba de importación en Rekordbox (R-02).

**Cuestión.** ¿Es aceptable esta política como punto de partida? **Resultado:** ______________________________

---

# 5. Decisiones del bloque B: dominio y persistencia

## OD-04 · Resultados de varios motores por pista

**Contexto.** La arquitectura admite Essentia, librosa y madmom (ADR-003). RF-07 exige registrar motor y versión de cada resultado. RF-29 compara motores.

**Propuesta incorporada.** RF-07 pasa a Must. Una pista puede tener varios resultados de análisis, identificados por motor y versión. Un motor activo configurable determina qué resultado usa el generador.

| Alternativa | Ventajas | Inconvenientes |
|---|---|---|
| A1. Un resultado por pista | Modelo simple | No permite evaluar motores sobre las mismas pistas |
| A2. Varios resultados por pista | Comparación entre motores; repetibilidad | Más complejidad en el modelo y en las consultas |

**Si se rechaza.** Revisar RF-07, RF-29, RNF-11, CU-11, ADR-003, ADR-004 y el glosario. La evaluación por motor exigiría reanalizar y sustituir resultados.

**Cuestiones para la reunión.**
1. ¿Deben coexistir varios resultados por pista?
2. ¿Se conserva el histórico de versiones de un mismo motor?
3. ¿El motor activo se elige por biblioteca, por análisis o de forma global?
4. ¿Se permite combinar BPM de un motor y tonalidad de otro, o cada resultado es indivisible?

**Resultado:** ______________________________

---

## OD-03 · Identificación permanente de pistas

**Contexto.** RF-09 exige que una pista conserve su identidad al cambiar de nombre o de ubicación. RNF-04 exige reescaneos rápidos (5 000 pistas en ≤ 2 min, provisional). Un fingerprint acústico obliga a descodificar el audio, lo que no cabe en ese presupuesto.

**Propuesta incorporada (ADR-010).** Identificación en dos niveles. Nivel 1: ubicación, tamaño, fecha y una huella rápida. Nivel 2: huella de contenido del audio, solo para lo no reconocido. Ante la duda se prefiere el falso negativo (duplicado) al falso positivo (fusión indebida).

| Alternativa | Ventajas | Inconvenientes |
|---|---|---|
| A1. Hash del fichero | Sencillo y exacto | Cambia al editar etiquetas; lectura completa |
| A2. Hash del audio | Independiente de etiquetas | Exige descodificar |
| A3. Fingerprint acústico | Tolera recodificación | Exige descodificar; umbrales; dependencia con licencia por verificar |
| A4. Dos niveles | Compatible con RNF-04 | Mayor complejidad; técnica del nivel 2 por decidir |

**Si se rechaza.** Revisar RF-09, RF-09b, RF-09c, RNF-04, CU-01, CU-02, ADR-004, ADR-010, el glosario y las pruebas T-ID.

**Cuestiones para la reunión.**
1. ¿Es adecuada la identificación en dos niveles?
2. **Alcance de la identidad.** Una misma grabación en WAV y en MP3: ¿una pista o dos? La propuesta es dos.
3. **Fichero modificado en la misma ubicación (CU-02, A3).** La propuesta conserva la identidad si la huella rápida coincide, y crea una pista nueva si no.
4. La técnica del nivel 2 (hash del audio o fingerprint) se decide con la prueba de identificación. ¿Se acepta ese criterio?
5. ¿Debe el sistema permitir al DJ gestionar los duplicados, o basta con informar de ellos?

**Resultado:** ______________________________

---

## OD-05 · Entidad `Library`

**Contexto.** El sistema trabaja sobre una colección local. Con `TrackLocation`, la pertenencia a una biblioteca se establece por la ubicación y no por la pista.

**Propuesta incorporada.** Mantener la entidad `Library`.

| Alternativa | Ventajas | Inconvenientes |
|---|---|---|
| A1. Mantener | Varias bibliotecas, histórico de importaciones y estadísticas por biblioteca | Más complejidad |
| A2. Eliminar | Simplificación | Menos flexibilidad; el panel no podría separar colecciones |

**Si se rechaza.** Eliminar la entidad, revisar CU-01, CU-02, CU-09, RF-24 a RF-27 y el modelo de ubicaciones.

**Cuestiones para la reunión.**
1. ¿Se soporta una o varias bibliotecas?
2. ¿Una biblioteca corresponde a una carpeta raíz importada?
3. ¿Las estadísticas del panel se calculan por biblioteca o globales?

**Resultado:** ______________________________

---

## OD-06 · Persistencia de transiciones

**Contexto.** RF-17 y RF-20 exigen evaluar y mostrar cada transición. RF-20b permite reordenar manualmente, lo que obliga a reevaluarlas. Si cambia el motor activo o se reanalizan pistas, la evaluación de un setlist antiguo podría variar.

| Alternativa | Ventajas | Inconvenientes |
|---|---|---|
| A1. Recalcular siempre | Siempre consistente con el orden actual | Un setlist histórico puede mostrar valores distintos de los que tenía al generarse |
| A2. Persistir como instantánea | Trazabilidad e histórico estable; sirve a RF-27 | Riesgo de inconsistencia tras editar si no se recalcula |
| A3. Persistir solo agregados | Simple y suficiente para las estadísticas | No permite revisar el detalle de transiciones antiguas |

**Propuesta inicial del autor.** A2: guardar una instantánea al generar, con el motor, la versión y la política usadas, y recalcularla al editar el setlist. Es una propuesta; **no hay decisión**.

**Si se resuelve de otra forma.** Revisar RF-10, RF-17, RF-20, RF-20b, RF-27, CU-05, CU-08 y ADR-004.

**Cuestiones para la reunión.**
1. ¿Debe un setlist histórico conservar la evaluación que tenía al generarse?
2. Tras una edición manual, ¿se guarda la secuencia original generada?
3. ¿Qué datos de la transición deben conservarse: salto de BPM, distancia Camelot, coste?

**Resultado:** ______________________________

---

## OD-07 · Modelo de dominio definitivo

**Contexto.** El modelo se diseña a partir de las entidades candidatas de la sección 8.2 y 8.3 y se detalla en `data-model.md`.

**Propuesta incorporada.** Se adopta el conjunto de entidades de la sección 8, con los nombres canónicos del glosario.

**Si se rechaza.** Revisar el glosario (sección 6), ADR-002, ADR-004 y `data-model.md`.

**Cuestiones para la reunión.**
1. ¿Representan estas entidades correctamente el dominio?
2. ¿`TrackMetadata` es una entidad propia o parte de `Track`?
3. ¿Hace falta una entidad propia para los datos de identificación (huellas) en lugar de un campo único en `Track`? Véase N-26.
4. ¿Se acepta el puerto `EvaluationRepository` para referencias e informes de evaluación?
5. **Intervalo de género (ADR-005).** Una pista pertenece a un intervalo según su instante de inicio. ¿Es el criterio adecuado para RF-15?

**Resultado:** ______________________________

---

# 6. Decisiones del bloque C: complementarias

## OD-08 · Estado de ADR-007 a ADR-010

**Contexto.** Los cuatro ADR existen como propuestos. Ningún tutor los ha validado.

| ADR | Propuesta | Condición |
|---|---|---|
| ADR-007 | Núcleo con dependencias permisivas y adaptadores opcionales para licencias restrictivas | Inventario verificado y prueba de concepto |
| ADR-008 | Python, PySide6 (alternativa Tkinter) y distribución en dos niveles | Prueba de interfaz y de empaquetado; licencias |
| ADR-009 | Muestra estratificada de la biblioteca del autor con contraste público | Prueba de concepto |
| ADR-010 | Identificación en dos niveles | Es la propuesta de OD-03 |

**Cuestiones para la reunión.**
1. ¿Se mantienen, se modifican o se consolidan estos ADR?
2. **Licencia del repositorio (ADR-007).** `LICENSE` es MIT, y el README ya no describe el proyecto como «exclusivamente académico». ¿Se confirma la licencia MIT?
3. **Distribución en dos niveles (ADR-008).** El nivel obligatorio es instalar desde código fuente, lo que puede perjudicar RNF-13 para un DJ no técnico. ¿Es aceptable como mínimo, con el ejecutable como mejora?

**Resultado:** ______________________________

---

## OD-09 · Motor MIR definitivo

**Contexto.** ADR-003 desacopla el análisis mediante un puerto. La elección de librería depende de la prueba de concepto, no de los tutores.

**Propuesta.** Decidir con los criterios de ADR-003: instalación en Windows y macOS y licencia son eliminatorios; después se comparan exactitud y coste. Candidatas: Essentia, librosa y madmom.

**Cuestiones para la reunión.**
1. ¿Se aprueba el protocolo de la prueba de concepto?
2. ¿Se acepta que la prueba se ejecute después de aceptar los ADR? Es una desviación respecto al plan del anteproyecto (N-16).

**Resultado:** ______________________________

---

## OD-10 · Protocolo de evaluación final

**Contexto.** ADR-009 propone una muestra estratificada de la biblioteca del autor con referencia de Rekordbox, contraste con un conjunto público si es accesible, y separación entre conjunto piloto y muestra reservada.

**Cuestiones para la reunión.**
1. Tamaño mínimo de la muestra. La propuesta es 300 pistas.
2. ¿Se acepta la separación estricta entre piloto y muestra reservada?
3. Valoración por DJs: ¿cuántos participantes y cómo se localizan? ¿Se acepta la comparación a ciegas con setlists aleatorios?
4. ¿Se acepta una auditoría manual de una submuestra de discrepancias?

**Resultado:** ______________________________

---

## Cuestión C-03 · Desviación del plan

La prueba de concepto precede a la arquitectura en el plan del anteproyecto, pero los ADR se aceptaron antes de realizarla. **Cuestión.** ¿Se acepta registrar esta desviación en la memoria (4.4)? **Resultado:** ______________________________

## Cuestión C-04 · Reorganización del repositorio

El repositorio conserva `backend`, `frontend` y `database`, propios de una arquitectura cliente-servidor descartada. **Cuestión.** Se propone reorganizar según ADR-008 antes de escribir código. **Resultado:** ______________________________

## Cuestión C-05 · Disponibilidad de DJs

Riesgo R-09. **Cuestión.** ¿Hay candidatos para la valoración? ¿Se prepara el plan alternativo? **Resultado:** ______________________________

---

# 7. Registro de resultados de la reunión

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
| C-01 a C-05 | | |

Fecha de la reunión: ____________ · Asistentes: ______________________________

---

# 8. Preparación para el modelo de dominio

Esta sección identifica lo que ya puede usarse y lo que debe tratarse con cautela. **No es el modelo de dominio.** No define atributos, relaciones ni tablas.

## 8.1 Información ya consolidada

| Elemento | Contenido | Fuente |
|---|---|---|
| Vocabulario canónico | Nombres de puertos y entidades | SRS 7.0, glosario sección 8 |
| Catálogo de puertos | `LibraryScanner`, `MetadataReader`, `AudioAnalyzer`, `TrackRepository`, `SetlistRepository`, `StatisticsRepository`, `SetlistExporter`, `ReferenceDataProvider`; propuestos `TrackIdentifier` y `EvaluationRepository` | ADR-002 |
| Reglas de dependencia | Dominio solo con la biblioteca estándar | ADR-002, RNF-22 |
| Restricciones del generador | R1 a R7 | ADR-005 |
| Función de coste | Salto de BPM, disonancia armónica e incoherencia de género, con pesos configurables | ADR-005 |
| Regla armónica básica | Mismo código, ±1 con la misma letra, o mismo número con letra opuesta; el resto, configurable | RF-14, ecuación 3.6 de la memoria |
| Correspondencia Camelot | Las 24 tonalidades con su código, derivada en el dominio | RF-06 |
| Parámetros por defecto | Tolerancia de duración ±5 %; salto máximo de BPM 5 (provisional) | RF-12, RF-13b |
| Origen de un descriptor | Estimado o etiqueta, con motor y versión | RF-07 |
| Estados | Pista o ubicación: activa, ausente, movida o fallida | RF-09c, RF-04 |
| Marca de fallo | Un descriptor no estimable se marca con su causa, sin valor inventado | RF-04, RNF-15 |
| Reproducibilidad | Un setlist se guarda con su solicitud, semilla y versión del algoritmo | RF-10, RNF-11 |
| Setlist editado | Puede incumplir restricciones; se señalan las transiciones afectadas | RF-20b |
| Formatos de audio | MP3, WAV, FLAC y AIFF | RF-02 |
| Umbrales numéricos | Provisionales (P) hasta la prueba de concepto | SRS 1.3 |

## 8.2 Entidades y objetos consolidados

Su existencia está respaldada por requisitos Must. Los atributos se concretan en el diseño.

| Elemento | Tipo | Respaldo |
|---|---|---|
| `Setlist` y `SetlistTrack` | Entidades | RF-10, RF-17, RF-18 |
| `GenerationRequest` | Entidad | RF-10, RF-12 a RF-14, RNF-11 |
| `TrackMetadata` | Entidad (o parte de `Track`, véase OD-07) | RF-03 |
| `TrackLocation` | Entidad | RF-09c, RF-22 |
| `ReferenceMeasurement` y `EvaluationReport` | Entidades (si se acepta OD-01) | RF-29, RF-29b |
| `GenreSegment` y `Anchor` | Entidades dependientes de `GenerationRequest` | RF-15, RF-16 (Should) |
| `CamelotKey` | Objeto de valor | RF-06 |
| BPM, duración y política armónica | Objetos de valor | RF-12, RF-13b, RF-14 |
| Compatibilidad armónica | Servicio de dominio | RF-14 |
| Evaluación de una transición (cálculo) | Servicio de dominio | RF-17, RF-20 |
| Validación de setlists | Servicio de dominio | RF-18, RNF-10 |
| Resolutor de restricciones | Servicio de dominio, propio | ADR-005 |

## 8.3 Entidades controvertidas

| Entidad | Controversia | OD | Qué puede asumir el diseño mientras tanto |
|---|---|---|---|
| `Track` | Su identidad y sus huellas: un solo campo o varios datos de identificación, en la pista o en la ubicación | OD-03, OD-07 (N-26) | Identificador interno independiente de la ruta. Los datos de identificación se tratan como un grupo separado |
| `AnalysisResult` y `AnalysisRun` | Si hay uno o varios por pista; cómo se elige el activo | OD-04 | Varios por pista, identificados por motor y versión |
| `Library` | Si existe y qué la define | OD-05 | Existe; la pertenencia se establece por la ubicación |
| `Transition` | Si se persiste, qué datos y cuándo se recalcula | OD-06 | Se calcula siempre en el dominio; la persistencia se decide aparte |
| Datos de identificación (huellas) | Si son entidad propia | OD-03, OD-07 | Grupo de datos con versión del algoritmo |

## 8.4 Dependencias entre decisiones abiertas

| Decisión | Condiciona a | Motivo |
|---|---|---|
| OD-04 | OD-07, OD-01, OD-06 | Define `AnalysisResult`; la evaluación por motor depende de ella; si cambia el motor activo, las evaluaciones antiguas pueden variar |
| OD-03 | OD-07, OD-05 | Define la identidad de `Track` y los campos de `TrackLocation`; la pertenencia a la biblioteca se establece por ubicación |
| OD-05 | OD-07 | Determina si `Library` entra en el modelo |
| OD-06 | OD-07, RF-20b, RF-27 | Determina si se persisten transiciones y cómo se recalculan al editar |
| OD-01 | OD-07, OD-10 | Si RF-29 deja de ser Must, las entidades de evaluación pasan a opcionales |
| OD-02 | Ninguna | Es un campo de `GenerationRequest` |
| OD-07 | Todo el modelo de datos | Integra las anteriores |

**Orden de resolución recomendado:** OD-04, OD-03, OD-05, OD-06 y, por último, OD-07.

## 8.5 Riesgos para el modelo de datos

| ID | Riesgo | Origen | Mitigación |
|---|---|---|---|
| DM-01 | Cambiar la identidad de pista tras congelar el esquema obliga a migrar huellas e identificadores | OD-03, R-12 | Versión del algoritmo en cada huella; migraciones desde la primera versión (RNF-27) |
| DM-02 | Las consultas sobre el motor activo complican las uniones y pueden penalizar RNF-03 y RF-11b | OD-04 | Cargar las candidatas en memoria para la generación; índices por motor |
| DM-03 | Transiciones persistidas inconsistentes tras editar un setlist | OD-06 | Recalcular siempre al editar; marca de setlist editado |
| DM-04 | La pertenencia a una biblioteca por ubicación complica el histórico y las estadísticas | OD-05 | Resolver OD-05 antes del modelo conceptual |
| DM-05 | SQLite es permisivo con tipos y restricciones; parte de la integridad queda en el dominio | ADR-004 | Pruebas de integridad; claves foráneas activadas |
| DM-06 | Un único escritor limita el análisis paralelo | ADR-004, H-37 | Un coordinador persiste los resultados |
| DM-07 | Rutas con Unicode, espacios y longitud extrema | RNF-16 | Texto Unicode; conversión solo en infraestructura |
| DM-08 | Reproducir un setlist exige conservar semilla, motor, versión y pesos | RNF-11, RF-10 | Guardarlos con la solicitud de generación |
| DM-09 | Las referencias de evaluación dependen de que el XML de Rekordbox contenga BPM y tonalidad | RF-29b, ADR-009 | Diseñar la tabla de referencias independiente del origen, con CSV como alternativa |
| DM-10 | Un modelo demasiado detallado antes de validar OD-03 a OD-07 | R-13 | Mantener el modelo como versión provisional marcada |

## 8.6 Supuestos de trabajo

Hasta la validación de los tutores, el diseño usa los supuestos de ADR-004:

| OD | Supuesto |
|---|---|
| OD-03 | La identidad permanente no depende de la ruta; el mecanismo se define en ADR-010 |
| OD-04 | Una pista puede tener varios resultados de análisis, identificados por motor y versión |
| OD-05 | Existe la entidad `Library` |
| OD-06 | Las transiciones se pueden persistir; si el setlist se edita, deben recalcularse |
| OD-07 | Se adoptan las entidades de las secciones 8.2 y 8.3 |

## 8.7 Orden de trabajo recomendado

1. Modelo de dominio: entidades, objetos de valor y servicios, con cada supuesto marcado.
2. Comprobación del dominio contra los once casos de uso.
3. Modelo conceptual de datos.
4. MER.
5. Modelo relacional.
6. Diseño físico de SQLite.

Cada documento se entrega como versión provisional. Se congela cuando los tutores validen OD-03 a OD-07.

---

# 9. Control de cambios

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-10 | Primer registro de decisiones abiertas |
| 2.0 | 2026-11-04 | Actualización tras la consolidación |
| 3.0 | 2026-11-05 | Reescritura completa como documento de trabajo para la reunión: tabla resumen, propuestas incorporadas, alternativas, consecuencias de un rechazo, cuestiones para los tutores, registro de resultados, cuestiones C-01 a C-05 y sección «Preparación para el modelo de dominio». OD-01 a OD-07 pasan a «propuesta incorporada»; OD-09 y OD-10 se reformulan en relación con ADR-003 y ADR-009 |
| 3.1 | 2026-11-06 | Revisión de la v3.0 contra la línea base: identificadores (OD, C, DM, N, H, R) y referencias a RF, RNF, CU, ADR y pruebas comprobados; sin cambios de contenido |
