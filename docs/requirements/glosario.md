# Glosario del Dominio

**Versión:** 2.1 (alineado con SRS v4.0, casos de uso v1.1 y matriz de trazabilidad v3.0) · **Fecha:** 2026-10-30

**Uso:** vocabulario común para el modelo de dominio, el código y la memoria. Los nombres de entidades propuestos para el código se indican entre paréntesis.

**Convenciones:**
- Los términos que dependen de una decisión abierta de `open-decisions.md` se marcan como **[PROPUESTA · OD-xx]**. No cierran la decisión.
- Los términos nuevos de v2.1 se marcan con **(nuevo)** y los redefinidos con **(revisado)**.
- Cuando un concepto ha recibido nombres distintos en documentos anteriores, el nombre canónico es el indicado en la sección 8.

---

# 1. Dominio musical

| Término | Definición | Relevancia en el sistema |
|---|---|---|
| **Tempo / BPM** | Velocidad de una pieza expresada en pulsos por minuto (*beats per minute*). Puede ser no entero. | Descriptor estimado (RF-04) y criterio de compatibilidad entre pistas. |
| **Tonalidad** | Par tónica-modo (por ejemplo, La menor o Do mayor) que describe el centro tonal de una pieza. | Descriptor estimado (RF-05). |
| **Modo** | Mayor o menor. | Determina la letra del código Camelot. |
| **Tonalidad relativa** (nuevo) | Tonalidad mayor y menor que comparten las mismas siete notas (por ejemplo, Do mayor y La menor). | En la rueda Camelot comparten número. Es también un tipo de error de estimación (RNF-09). |
| **Tonalidad paralela** (nuevo) | Tonalidad mayor y menor con la misma tónica (por ejemplo, Do mayor y Do menor). | Tipo de error de estimación (RNF-09). |
| **Círculo de quintas** | Ordenación de las doce notas por intervalos de quinta; las tonalidades vecinas comparten casi todas sus notas. | Fundamento de la compatibilidad armónica. |
| **Rueda Camelot** | Sistema de notación que mapea las 24 tonalidades a códigos del 1 al 12 más una letra: A para menor y B para mayor. | Notación derivada de la tonalidad (RF-06). |
| **Código Camelot** | Identificador de una tonalidad en la Rueda Camelot (1A a 12B). | Valor almacenado y usado por el generador (`CamelotKey`). |
| **Distancia Camelot** (nuevo) | Distancia circular entre los números de dos códigos Camelot: el mínimo entre su diferencia absoluta y 12 menos esa diferencia. | Campo `camelot_distance` de la transición (OD-06) y base de la compatibilidad (ecuación 3.5 de la memoria). |
| **Mezcla armónica** | Práctica de encadenar pistas con tonalidades compatibles para evitar disonancias en la transición. | Fundamenta RF-14 y RF-17. |
| **Compatibilidad armónica** (revisado) | Relación entre dos códigos Camelot que permite una transición según la política armónica vigente. | RF-14, RF-17 y RNF-10. |
| **Política armónica** (nuevo) | Conjunto de reglas que define qué pares de códigos Camelot son compatibles. Por defecto: mismo código, ±1 con la misma letra, o mismo número con letra opuesta. Otros movimientos son parámetros configurables. | RF-14. Campo `harmonic_policy` de la solicitud de generación (OD-07). |
| **Transición** | Paso de una pista a la siguiente dentro de un setlist. | Entidad evaluada por el generador (`Transition`). **[PROPUESTA · OD-06]** Su persistencia está pendiente. |
| **Compatibilidad de transición** | Evaluación de una transición considerando BPM, tonalidad y reglas armónicas. | RF-17 y RF-20. |
| **Salto de tempo** (revisado) | Diferencia de BPM entre dos pistas consecutivas. | Se limita con el salto máximo de BPM (RF-13b) y se evalúa en RF-17. Campo `bpm_delta`. |
| **Error de octava (de tempo)** | Estimación que es múltiplo o submúltiplo del BPM real (×2, ÷2, ×3, ÷3). | RNF-06 y RNF-09. |
| **Descriptor musical** (revisado) | Propiedad de una pista derivada del audio o de sus etiquetas: BPM, tonalidad, Camelot, duración, género o año. | Información consumida por el generador. Los estimados se almacenan como `AnalysisResult` y los leídos de etiquetas como `TrackMetadata` **[PROPUESTA · OD-04, OD-07]**. |
| **Cromagrama** | Representación de la energía de la señal por clases de altura a lo largo del tiempo. | Técnica habitual para estimar tonalidad. |
| **Perfil de tonalidad** | Plantilla con la que se compara la distribución de alturas de una pista para decidir su tonalidad. | Técnica habitual para estimar tonalidad. |
| **MIR** | *Music Information Retrieval*: disciplina que extrae información musical a partir de señales de audio. | Marco teórico del motor de análisis. |

---

# 2. Dominio DJ

| Término | Definición | Relevancia en el sistema |
|---|---|---|
| **DJ** | Profesional o aficionado que selecciona y mezcla música para una audiencia. | Actor principal. |
| **Pista (Track)** (revisado) | Obra musical única de la biblioteca, identificada de forma permanente e independiente de su nombre o su ubicación. Su fichero se representa por una ubicación. | Entidad central (`Track`). **[PROPUESTA · OD-03, OD-07]** |
| **Biblioteca musical** (revisado) | Conjunto de pistas gestionadas por el DJ. | Entrada principal del sistema (`Library`). **[PROPUESTA · OD-05]** La existencia de la entidad es una decisión abierta. |
| **Biblioteca candidata** (revisado) | Subconjunto de pistas que cumplen los filtros iniciales para la generación: tienen resultados válidos del motor activo y una ubicación disponible. | Entrada del algoritmo (CU-05). |
| **Setlist** | Lista ordenada de pistas preparada para una actuación. | Salida principal del sistema (`Setlist`). |
| **Setlist válido** (revisado) | Setlist generado que cumple todas las restricciones configuradas y no contiene duplicados. No se aplica a un setlist editado manualmente. | RF-17, RF-18 y RNF-10. |
| **Setlist editado** (nuevo) | Setlist cuyo orden ha sido modificado manualmente tras su generación. Puede incumplir restricciones; el sistema señala las transiciones afectadas. | RF-20b. |
| **Solicitud de generación** (nuevo) | Conjunto de parámetros y semilla que definen una generación. Es el nombre canónico de lo que antes se llamaba «parámetros de generación». | Entrada del generador (`GenerationRequest`). **[PROPUESTA · OD-07]** Alias: `GenerationParameters`. |
| **Parámetros de generación** (revisado) | Duración, rango de BPM, salto máximo de BPM, política armónica, progresión de géneros y pistas ancladas. | RF-12 a RF-16 y RF-13b. |
| **Tolerancia de duración** (nuevo) | Desviación admitida respecto a la duración objetivo del setlist. Por defecto ±5 %. | RF-12 y ecuación 3.9 de la memoria. |
| **Salto máximo de BPM** (nuevo) | Diferencia máxima de BPM admitida entre dos pistas consecutivas. Valor por defecto propuesto: 5 BPM (provisional). | RF-13b. **[PROPUESTA · OD-02]** |
| **Progresión de géneros** | Secuencia de géneros asignada a distintos intervalos temporales. | RF-15. |
| **Segmento de género** (nuevo) | Intervalo temporal del setlist con un género asignado. | Elemento de la progresión de géneros (`GenreSegment`). **[PROPUESTA · OD-07]** |
| **Pista anclada** | Pista fijada explícitamente en una posición concreta del setlist. | RF-16. |
| **Ancla** (nuevo) | Registro de una pista anclada en una posición de una solicitud de generación. | `Anchor`. **[PROPUESTA · OD-07]** |
| **Restricción de generación** | Condición que debe cumplirse durante la construcción del setlist. | RF-12 a RF-19. |
| **Función de coste** (nuevo) | Medida que se minimiza entre las soluciones válidas: salto de BPM, coherencia armónica y coherencia de género. | RF-17, ADR-005 y ecuación 3.11 de la memoria. |
| **Orden de reproducción** | Secuencia final de pistas propuesta al DJ. | RF-17. |
| **Conflicto de restricciones** (revisado) | Situación en la que se ha demostrado que no existe un conjunto de pistas capaz de satisfacer simultáneamente todas las restricciones. Se distingue de la interrupción por tiempo límite, que no demuestra inviabilidad. | RF-19. |
| **Tiempo límite de generación** (nuevo) | Duración máxima de la búsqueda. Si se agota sin solución, el sistema lo informa como tal y no como conflicto. | RF-19 y RNF-03. |
| **Semilla** | Valor empleado para inicializar procesos pseudoaleatorios. Se almacena con el setlist. | RNF-11, RF-10 (`random_seed`). |
| **Histórico de setlists** | Registro persistente de los setlists generados y de sus parámetros. | RF-10 y RF-24. |
| **Evaluación de transición** | Valoración de la calidad de una transición. | RF-20. |
| **Ajuste del setlist** | Reordenación manual del setlist antes de su exportación. | RF-20b. |
| **Pista movida** (nuevo) | Pista ya conocida que aparece en una ubicación distinta. Conserva su identificador y su histórico. | RF-09c. |
| **Pista duplicada** (nuevo) | Pista ya conocida que existe en varias ubicaciones a la vez. Mantiene un único identificador. | RF-09c. |
| **Pista ausente** (nuevo) | Pista cuya ubicación registrada ya no existe. Se marca, no se elimina, y se avisa de ella al exportar. | RF-09c y CU-07. |
| **Rekordbox** | Aplicación de gestión musical para DJs de Pioneer DJ (actualmente AlphaTheta). | Destino de exportación y referencia de evaluación. |

---

# 3. Datos y formatos

| Término | Definición | Relevancia en el sistema |
|---|---|---|
| **Metadatos / etiquetas** | Información incrustada en un fichero de audio: título, artista, género, año y duración, y a veces BPM y tonalidad. | Fuente de RF-03 (`TrackMetadata`). |
| **ID3** | Estándar de etiquetado utilizado principalmente en MP3. | Utilizado por el lector de metadatos. |
| **Rekordbox XML** | Formato XML de intercambio utilizado por Rekordbox. Contiene una colección de pistas y un árbol de listas de reproducción. | RF-21 (exportación) y RF-29b (importación de la referencia). |
| **XML de colección** (nuevo) | Fichero XML que el DJ exporta desde Rekordbox con su colección. Se usa como fuente de los valores de referencia. | RF-29b y supuesto H-17. |
| **M3U** (revisado) | Formato textual de listas de reproducción basado en rutas de ficheros. | Formato de exportación del panel (RF-28). |
| **M3U8** (revisado) | Variante de M3U con codificación UTF-8. Es la que genera el sistema; en el panel, el M3U de RF-28 se genera también en UTF-8. | Exportación complementaria del setlist (RF-21b). |
| **Ruta resuelta** | Ruta expresada de forma que Rekordbox pueda localizar correctamente la pista. | RF-22. |
| **Identificador de pista** | Valor único e independiente del nombre o ubicación física del archivo. | RF-09 y RF-09b. |
| **Identificación permanente** (nuevo) | Mecanismo que reconoce una pista ya conocida aunque cambie de nombre o ubicación. | RF-09. **[PROPUESTA · OD-03]** ADR-010. |
| **Hash del fichero** (nuevo) | Huella calculada sobre el fichero completo. Cambia si se modifican las etiquetas. | Alternativa A1 de OD-03. |
| **Hash del contenido de audio** (nuevo) | Huella calculada sobre las muestras de audio, independiente de las etiquetas, con coste de cálculo elevado. | Alternativa A2 de OD-03. |
| **Fingerprint acústico** (nuevo) | Huella compacta derivada del contenido sonoro, que tolera determinadas modificaciones del fichero. | Alternativa A3 de OD-03. |
| **Identificación en dos niveles** (nuevo) | Estrategia que reconoce primero la pista con datos baratos (ruta, tamaño, fecha, hash) y recurre al fingerprint solo para lo no reconocido. | Propuesta para compatibilizar OD-03 con RNF-04. |
| **Ubicación de pista** (nuevo) | Ruta física concreta de una pista, con su estado y la última vez que se vio. | `TrackLocation`. **[PROPUESTA · OD-07]** RF-09c. |
| **Estado de pista / ubicación** (nuevo) | Situación de una pista o ubicación: activa, ausente, movida o fallida. | RF-09c y RF-04. |
| **Marca de fallo** (nuevo) | Registro de que un descriptor no pudo estimarse, con su causa. | RF-04, RF-05 y RNF-15. |
| **Actualización incremental** | Importación que analiza únicamente pistas cuyo identificador aún no existe en la base de datos. | RF-09b. |
| **Fuente única de verdad** | Almacén considerado oficial para un conjunto de datos. | Base de datos local. |
| **Origen del descriptor** (revisado) | Indica si un descriptor procede de etiquetas o de análisis automático. Para los estimados se registra además el motor y su versión. | RF-07. |
| **Motor de análisis** (nuevo) | Implementación concreta del puerto `AudioAnalyzer` (Essentia, librosa, madmom u otra), identificada por nombre y versión. | RF-07 y ADR-003. |
| **Motor activo** (nuevo) | Motor cuyos resultados consume el generador. Es configurable. | RF-07 y RNF-11. **[PROPUESTA · OD-04]** |
| **Ejecución de análisis** (nuevo) | Una ejecución concreta de un motor sobre un conjunto de pistas, con su fecha. | `AnalysisRun`. **[PROPUESTA · OD-04, OD-07]** |
| **Resultado de análisis** (nuevo) | Valores de BPM, tonalidad, código Camelot y confianza que un motor obtiene sobre una pista. Una pista puede tener varios. | `AnalysisResult`. **[PROPUESTA · OD-04, OD-07]** |
| **Medición de referencia** (nuevo) | Valores de BPM y tonalidad obtenidos de Rekordbox para una pista, usados como patrón de comparación. | `ReferenceMeasurement`. RF-29b. |
| **Informe de evaluación** (nuevo) | Resultado agregado de contrastar los descriptores estimados con la referencia, por motor. | `EvaluationReport`. RF-29. |
| **Migración** | Cambio versionado en el esquema de la base de datos. | RNF-27. |
| **Panel** | Vista agregada del historial y las estadísticas de la aplicación. | RF-24 a RF-28. |

---

# 4. Evaluación

| Término | Definición | Relevancia en el sistema |
|---|---|---|
| **Valor de referencia** | Valor de BPM o tonalidad empleado como patrón de comparación. En este trabajo, el que calcula Rekordbox para la misma pista; no es una verdad absoluta. | RF-29 y RF-29b. |
| **Exactitud de BPM estricta** | Porcentaje de estimaciones de BPM dentro de la tolerancia establecida (±4 %) respecto a la referencia. | RNF-05. |
| **Exactitud de BPM con tolerancia de octava** | Exactitud admitiendo errores de octava habituales. | RNF-06. |
| **Exactitud de tonalidad** | Coincidencia de tonalidad respecto a la referencia, exacta o por compatibilidad Camelot. | RNF-07 y RNF-08. |
| **Desglose de errores** (nuevo) | Clasificación de los errores de estimación por tipo (BPM: octava y otros; tonalidad: relativa, quinta, paralela y otros). | RNF-09. |
| **Intervalo de Wilson** (nuevo) | Intervalo de confianza para una proporción. | RNF-09. |
| **Conjunto de evaluación** | Colección de pistas utilizada para medir el rendimiento del sistema. | ADR-009 y RF-29. |
| **Benchmark** | Prueba diseñada para medir rendimiento o escalabilidad. | RNF-01, RNF-02, RNF-03 y RNF-18. |
| **Prueba de concepto (PoC)** (nuevo) | Experimento previo que contrasta librerías de análisis y la importación en Rekordbox con datos reales. | Hito H2. Ratifica los umbrales provisionales. |
| **Umbral provisional (P)** (nuevo) | Valor numérico de un requisito sujeto a ratificación tras la PoC. | SRS 1.3 y sección 4. |

---

# 5. Ingeniería del software y arquitectura

| Término | Definición | Relevancia en el sistema |
|---|---|---|
| **Arquitectura limpia (Clean Architecture)** | Organización en capas donde las dependencias apuntan hacia el dominio. | Base arquitectónica del proyecto (ADR-002). |
| **Regla de dependencia** | Las capas internas no dependen de las externas. | RNF-22. |
| **Entidad de dominio** | Objeto con identidad y reglas de negocio propias. | `Track`, `Setlist`, `Transition`. |
| **Caso de uso** | Operación de aplicación que satisface un objetivo del usuario. | Catálogo CU-01 a CU-11. |
| **Puerto** (revisado) | Interfaz que define una dependencia externa. Pertenece a la capa de Aplicación. | `AudioAnalyzer`, `MetadataReader`, `LibraryScanner`, `TrackRepository`, `SetlistRepository`, `StatisticsRepository`, `EvaluationRepository` **[PROPUESTA]**, `SetlistExporter`, `ReferenceDataProvider` y, **[PROPUESTA · OD-03]**, `TrackIdentifier`. |
| **Adaptador** | Implementación concreta de un puerto. | Infrastructure Layer. |
| **Repositorio** | Puerto encargado del almacenamiento y consulta de entidades. | `TrackRepository`, `SetlistRepository`. |
| **Determinismo** | Misma entrada y misma semilla producen el mismo resultado. | RNF-11. |
| **Idempotencia** | Repetir una operación produce el mismo estado final. | RF-09b, RNF-04. |
| **CSP** (nuevo) | *Constraint Satisfaction Problem*: formulación como variables y restricciones que deben cumplirse simultáneamente. | ADR-005. |
| **COP** (nuevo) | *Constraint Optimization Problem*: CSP con una función de coste que se minimiza entre las soluciones válidas. | ADR-005 (por la función de coste de RF-17). |
| **Solver** (nuevo) | Componente que resuelve el CSP o COP. Es una librería externa tras un puerto, o código propio en el dominio. | ADR-005 y SRS 7. |
| **ADR** | *Architecture Decision Record*. Documento que registra decisiones arquitectónicas. | Arquitectura y gestión del proyecto. |
| **OD** (nuevo) | Decisión abierta pendiente de validación por tutor y cotutor. | `open-decisions.md`, OD-01 a OD-08. |
| **Hallazgo (H-xx)** (nuevo) | Observación de la auditoría técnica, con estado aceptado, pendiente o aparcado. | `audit-review.md`. |
| **MoSCoW** | Técnica de priorización basada en Must, Should, Could y Won't. | Priorización de requisitos. |
| **Línea base** | Versión aprobada de un conjunto de documentos. | Hito H1. |
| **Trazabilidad** | Relación verificable entre objetivos, requisitos, casos de uso, pruebas e implementación. | Sección 5 del SRS y matriz de trazabilidad. |

---

# 6. Entidades del dominio propuestas

Vocabulario de las entidades que se validarán en OD-07. Es una propuesta: no fija atributos ni relaciones, que se concretarán en `data-model.md`.

| Entidad | Descripción |
|---|---|
| `Track` | Pista única, independiente de su ubicación física |
| `TrackLocation` | Ubicación física concreta de una pista |
| `TrackMetadata` | Metadatos leídos de las etiquetas |
| `AnalysisRun` | Ejecución concreta de un motor de análisis |
| `AnalysisResult` | Resultado de un motor sobre una pista |
| `GenerationRequest` | Solicitud de generación con sus parámetros y semilla |
| `GenreSegment` | Intervalo de la progresión de géneros |
| `Anchor` | Pista anclada en una posición |
| `Setlist` | Setlist generado |
| `SetlistTrack` | Pista dentro de un setlist, con su posición |
| `Transition` | Transición entre dos pistas consecutivas (OD-06) |
| `ReferenceMeasurement` | Valores de referencia de Rekordbox para una pista |
| `EvaluationReport` | Resultado agregado de la evaluación |
| `Library` | Colección de pistas (OD-05) |

---

# 7. Siglas

| Sigla | Significado |
|---|---|
| ADR | *Architecture Decision Record* |
| BPM | *Beats per minute* |
| COP | *Constraint Optimization Problem* |
| CSP | *Constraint Satisfaction Problem* |
| EDM | *Electronic Dance Music* |
| MIR | *Music Information Retrieval* |
| OD | Decisión abierta |
| PoC | Prueba de concepto |
| RF / RNF | Requisito funcional / no funcional |
| SRS | *Software Requirements Specification* |
| STFT | *Short-Time Fourier Transform* |
| TFG | Trabajo de Fin de Grado |

---

# 8. Vocabulario canónico

Los nombres de la columna izquierda sustituyen a los de la derecha en todos los documentos de la línea base.

| Nombre canónico | Nombres anteriores |
|---|---|
| `AudioAnalyzer` | `AnalysisEngine` (ADR-002, ADR-003) |
| `SetlistExporter` | `Exporter` (ADR-002) |
| `GenerationRequest` **[PROPUESTA · OD-07]** | `GenerationParameters` |
| `AnalysisResult` **[PROPUESTA · OD-04, OD-07]** | `Descriptor` (para los estimados) |
| M3U8 | M3U/M3U8 usados indistintamente |
| Salto máximo de BPM | «Salto moderado» (sin valor cuantificable) |

---

# 9. Referencias

Las referencias bibliográficas asociadas a BPM, tonalidad, Camelot, MIR y Rekordbox corresponden a la bibliografía del anteproyecto y de la memoria del TFG. Esta sección se sincronizará con el fichero BibTeX definitivo utilizado por la memoria.

---

# 10. Control de cambios

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0 | — | Versión inicial |
| 2.0 | 2026-10-19 | Alineación con SRS v3.0 |
| 2.1 | 2026-10-30 | Alineación con SRS v4.0, casos de uso v1.1 y matriz v3.0. Términos nuevos: política armónica, salto máximo de BPM, pista movida, duplicada y ausente, motor activo, resultado y ejecución de análisis, medición de referencia, identificación permanente, fingerprint, ubicación de pista, CSP y COP, entre otros. Términos revisados: pista, biblioteca candidata, setlist válido, conflicto de restricciones, puerto, M3U y M3U8. Nuevas secciones: entidades propuestas, siglas y vocabulario canónico |
