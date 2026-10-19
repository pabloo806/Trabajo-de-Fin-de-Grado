# Glosario del Dominio

**Versión:** 2.0 (alineado con SRS v3.0) · **Fecha:** 2026-10-19

**Uso:** vocabulario común para el modelo de dominio, el código y la memoria. Los nombres de entidades propuestos para el código se indican entre paréntesis.

---

# 1. Dominio musical

| Término | Definición | Relevancia en el sistema |
|---|---|---|
| **Tempo / BPM** | Velocidad de una pieza expresada en pulsos por minuto (*beats per minute*). Puede ser no entero. | Descriptor estimado (RF-04) y criterio de compatibilidad entre pistas. |
| **Tonalidad** | Par tónica-modo (por ejemplo, La menor o Do mayor) que describe el centro tonal de una pieza. | Descriptor estimado (RF-05). |
| **Modo** | Mayor o menor. | Determina la letra del código Camelot. |
| **Círculo de quintas** | Ordenación de las doce notas por intervalos de quinta; las tonalidades vecinas comparten casi todas sus notas. | Fundamento de la compatibilidad armónica. |
| **Rueda Camelot** | Sistema de notación que mapea las 24 tonalidades a códigos del 1 al 12 más una letra: A para menor y B para mayor. | Notación derivada de la tonalidad (RF-06). |
| **Código Camelot** | Identificador de una tonalidad en la Rueda Camelot (1A a 12B). | Valor almacenado y usado por el generador (`CamelotKey`). |
| **Mezcla armónica** | Práctica de encadenar pistas con tonalidades compatibles para evitar disonancias en la transición. | Fundamenta RF-14 y RF-17. |
| **Compatibilidad armónica** | Relación entre dos códigos Camelot compatibles para una transición. | RF-14, RF-17 y RNF-10. |
| **Transición** | Paso de una pista a la siguiente dentro de un setlist. | Entidad evaluada por el generador (`Transition`). |
| **Compatibilidad de transición** | Evaluación de una transición considerando BPM, tonalidad y reglas armónicas. | RF-17 y RF-20. |
| **Salto de tempo** | Diferencia de BPM entre dos pistas consecutivas. | Restricción de moderación en RF-17. |
| **Error de octava (de tempo)** | Estimación que es múltiplo o submúltiplo del BPM real (×2, ÷2, ×3, ÷3). | RNF-06 y RNF-09. |
| **Descriptor musical** | Propiedad de una pista derivada del audio o de sus etiquetas: BPM, tonalidad, Camelot, duración, género o año. | Información consumida por el generador (`Descriptor`). |
| **Cromagrama** | Representación de la energía de la señal por clases de altura a lo largo del tiempo. | Técnica habitual para estimar tonalidad. |
| **Perfil de tonalidad** | Plantilla con la que se compara la distribución de alturas de una pista para decidir su tonalidad. | Técnica habitual para estimar tonalidad. |
| **MIR** | *Music Information Retrieval*: disciplina que extrae información musical a partir de señales de audio. | Marco teórico del motor de análisis. |

---

# 2. Dominio DJ

| Término | Definición | Relevancia en el sistema |
|---|---|---|
| **DJ** | Profesional o aficionado que selecciona y mezcla música para una audiencia. | Actor principal. |
| **Pista (Track)** | Fichero de audio de la biblioteca con metadatos y descriptores musicales asociados. | Entidad central (`Track`). |
| **Biblioteca musical** | Conjunto de pistas gestionadas por el DJ. | Entrada principal del sistema (`Library`). |
| **Biblioteca candidata** | Subconjunto de pistas que cumplen los filtros iniciales para la generación. | Entrada del algoritmo. |
| **Setlist** | Lista ordenada de pistas preparada para una actuación. | Salida principal del sistema (`Setlist`). |
| **Setlist válido** | Setlist que cumple todas las restricciones configuradas y no contiene duplicados. | RF-17, RF-18 y RNF-10. |
| **Parámetros de generación** | Duración, BPM, compatibilidad armónica, progresión de géneros y pistas ancladas. | Entrada del generador (`GenerationParameters`). |
| **Progresión de géneros** | Secuencia de géneros asignada a distintos intervalos temporales. | RF-15. |
| **Pista anclada** | Pista fijada explícitamente en una posición concreta del setlist. | RF-16. |
| **Restricción de generación** | Condición que debe cumplirse durante la construcción del setlist. | RF-12 a RF-19. |
| **Orden de reproducción** | Secuencia final de pistas propuesta al DJ. | RF-17. |
| **Conflicto de restricciones** | Situación en la que no existe un conjunto de pistas capaz de satisfacer simultáneamente todas las restricciones. | RF-19. |
| **Semilla** | Valor empleado para inicializar procesos pseudoaleatorios. | RNF-11. |
| **Histórico de setlists** | Registro persistente de los setlists generados y de sus parámetros. | RF-10 y RF-24. |
| **Evaluación de transición** | Valoración de la calidad de una transición. | RF-20. |
| **Ajuste del setlist** | Reordenación manual del setlist antes de su exportación. | RF-20b. |
| **Rekordbox** | Aplicación de gestión musical para DJs de Pioneer DJ. | Destino de exportación y referencia de evaluación. |

---

# 3. Datos y formatos

| Término | Definición | Relevancia en el sistema |
|---|---|---|
| **Metadatos / etiquetas** | Información incrustada en un fichero de audio: título, artista, género, año y duración. | Fuente de RF-03. |
| **ID3** | Estándar de etiquetado utilizado principalmente en MP3. | Utilizado por el lector de metadatos. |
| **Rekordbox XML** | Formato XML de intercambio utilizado por Rekordbox. | RF-21. |
| **M3U / M3U8** | Formato textual de listas de reproducción basado en rutas de ficheros. | RF-28. |
| **Ruta resuelta** | Ruta expresada de forma que Rekordbox pueda localizar correctamente la pista. | RF-22. |
| **Identificador de pista** | Valor único e independiente del nombre o ubicación física del archivo. | RF-09 y RF-09b. |
| **Actualización incremental** | Importación que analiza únicamente pistas cuyo identificador aún no existe en la base de datos. | RF-09b. |
| **Fuente única de verdad** | Almacén considerado oficial para un conjunto de datos. | Base de datos local. |
| **Origen del descriptor** | Indica si un descriptor procede de etiquetas o de análisis automático. | RF-07. |
| **Migración** | Cambio versionado en el esquema de la base de datos. | Mantenimiento de O3. |
| **Panel** | Vista agregada del historial y las estadísticas de la aplicación. | RF-24 a RF-28. |

---

# 4. Evaluación

| Término | Definición | Relevancia en el sistema |
|---|---|---|
| **Valor de referencia** | Valor de BPM o tonalidad empleado como patrón de comparación. | RF-29. |
| **Exactitud de BPM estricta** | Porcentaje de estimaciones de BPM dentro de la tolerancia establecida respecto a la referencia. | RNF-05. |
| **Exactitud de BPM con tolerancia de octava** | Exactitud admitiendo errores de octava habituales. | RNF-06. |
| **Exactitud de tonalidad** | Coincidencia de tonalidad respecto a la referencia. | RNF-07 y RNF-08. |
| **Conjunto de evaluación** | Colección de pistas utilizada para medir el rendimiento del sistema. | ADR-009 y RF-29. |
| **Benchmark** | Prueba diseñada para medir rendimiento o escalabilidad. | RNF-01, RNF-02, RNF-03 y RNF-18. |

---

# 5. Ingeniería del software y arquitectura

| Término | Definición | Relevancia en el sistema |
|---|---|---|
| **Arquitectura limpia (Clean Architecture)** | Organización en capas donde las dependencias apuntan hacia el dominio. | Base arquitectónica del proyecto. |
| **Regla de dependencia** | Las capas internas no dependen de las externas. | RNF-22. |
| **Entidad de dominio** | Objeto con identidad y reglas de negocio propias. | `Track`, `Setlist`, `Transition`. |
| **Caso de uso** | Operación de aplicación que satisface un objetivo del usuario. | Catálogo CU-01 a CU-11. |
| **Puerto** | Interfaz que define una dependencia externa. | `AudioAnalyzer`, `TrackRepository`, `SetlistExporter`. |
| **Adaptador** | Implementación concreta de un puerto. | Infrastructure Layer. |
| **Repositorio** | Puerto encargado del almacenamiento y consulta de entidades. | `TrackRepository`, `SetlistRepository`. |
| **Determinismo** | Misma entrada y misma semilla producen el mismo resultado. | RNF-11. |
| **Idempotencia** | Repetir una operación produce el mismo estado final. | RF-09b, RNF-04. |
| **ADR** | *Architecture Decision Record*. Documento que registra decisiones arquitectónicas. | Arquitectura y gestión del proyecto. |
| **MoSCoW** | Técnica de priorización basada en Must, Should, Could y Won't. | Priorización de requisitos. |
| **Línea base** | Versión aprobada de un conjunto de documentos. | Hito H1. |
| **Trazabilidad** | Relación verificable entre objetivos, requisitos, casos de uso, pruebas e implementación. | Sección 5 del SRS. |

---

# 6. Referencias

Las referencias bibliográficas asociadas a BPM, tonalidad, Camelot, MIR y Rekordbox corresponden a la bibliografía del anteproyecto y de la memoria del TFG. Esta sección se sincronizará con el fichero BibTeX definitivo utilizado por la memoria.
