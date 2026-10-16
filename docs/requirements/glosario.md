# Glosario del Dominio

**Versión:** 1.0 (propuesta) · **Fecha:** 2026-10-09
**Uso:** vocabulario común para el modelo de dominio, el código y la memoria. Los nombres de entidades propuestos para el código se indican entre paréntesis.

---

## 1. Dominio musical

| Término | Definición | Relevancia en el sistema |
|---|---|---|
| **Tempo / BPM** | Velocidad de una pieza expresada en pulsos por minuto (*beats per minute*). Puede ser no entero. | Descriptor estimado (RF-04) y criterio de compatibilidad entre pistas. |
| **Tonalidad** | Par tónica-modo (por ejemplo, La menor o Do mayor) que describe el centro tonal de una pieza. | Descriptor estimado (RF-05). |
| **Modo** | Mayor o menor. | Determina la letra del código Camelot. |
| **Círculo de quintas** | Ordenación de las doce notas por intervalos de quinta; las tonalidades vecinas comparten casi todas sus notas. | Fundamento de la compatibilidad armónica [6]. |
| **Rueda Camelot** | Sistema de notación que mapea las 24 tonalidades a códigos del 1 al 12 más una letra: **A** para menor y **B** para mayor. Por ejemplo, 8A es La menor y 8B es Do mayor. | Notación derivada de la tonalidad (RF-06). |
| **Código Camelot** | Identificador de una tonalidad en la Rueda Camelot (1A a 12B). | Valor almacenado y usado por el generador (`CamelotKey`). |
| **Mezcla armónica** | Práctica de encadenar pistas con tonalidades compatibles para evitar disonancias en la transición. | Regla central del generador (RF-17). |
| **Compatibilidad armónica** | Relación entre dos códigos Camelot que permite mezclarlos: el mismo código, ±1 en el número con la misma letra, o el mismo número con la letra opuesta (tonalidad relativa). | Criterio de RF-14 y RNF-10. Otras reglas más avanzadas quedan fuera de alcance. |
| **Transición** | Paso de una pista a la siguiente dentro de un setlist. | Unidad que el generador valora y el sistema muestra (`Transition`). |
| **Salto de tempo** | Diferencia de BPM entre dos pistas consecutivas. | Restricción de moderación en RF-17. |
| **Error de octava (de tempo)** | Estimación que es múltiplo o submúltiplo del BPM real (×2, ÷2, ×3, ÷3). | Se contabiliza aparte en RNF-06 y RNF-09. |
| **Descriptor musical** | Propiedad de una pista derivada del audio o de sus etiquetas: BPM, tonalidad, código Camelot, duración, género, año. | Conjunto de datos que consume el generador (`Descriptor`). |
| **Cromagrama** | Representación de la energía de la señal por clases de altura (doce notas) a lo largo del tiempo. | Técnica habitual en la estimación de tonalidad [1]. |
| **Perfil de tonalidad** | Plantilla de referencia con la que se compara la distribución de alturas de una pista para decidir su tonalidad. | Técnica habitual en la estimación de tonalidad. |
| **MIR** | *Music Information Retrieval*: disciplina que extrae información de la música a partir de la señal. | Marco teórico del motor de análisis [1], [3], [4]. |

## 2. Dominio DJ

| Término | Definición | Relevancia en el sistema |
|---|---|---|
| **DJ** | Profesional o aficionado que selecciona y mezcla música para una audiencia. | Actor principal. |
| **Pista (Track)** | Fichero de audio de la biblioteca con sus metadatos y descriptores. | Entidad central (`Track`). |
| **Biblioteca musical** | Conjunto de pistas del DJ almacenadas en una carpeta local. | Entrada del sistema (`Library`). |
| **Setlist** | Lista ordenada de pistas preparada para una actuación. | Salida del generador (`Setlist`). |
| **Parámetros de generación** | Duración total, rango de BPM, tonalidades o compatibilidad exigida, progresión de géneros y pistas ancladas. | Entrada del generador (`GenerationParameters`). |
| **Progresión de géneros** | Secuencia de géneros asignada a intervalos de tiempo del setlist. | RF-15. |
| **Pista anclada** | Pista que el DJ fija en una posición concreta del setlist. | RF-16. |
| **Rekordbox** | Aplicación de gestión de bibliotecas y reproducción para DJs de Pioneer DJ. | Destino de la exportación y fuente de referencia [7]. |

## 3. Datos y formatos

| Término | Definición | Relevancia en el sistema |
|---|---|---|
| **Metadatos / etiquetas** | Información incrustada en el fichero de audio: título, artista, género, año, duración. | Fuente de RF-03. |
| **ID3** | Estándar de etiquetas de los ficheros MP3. Otros formatos usan mecanismos equivalentes (por ejemplo, comentarios Vorbis en FLAC o trozos ID3 en WAV y AIFF). | El lector de metadatos abstrae estas diferencias. |
| **Rekordbox XML** | Formato XML de intercambio de bibliotecas y listas de Rekordbox, con una colección de pistas y un árbol de listas que las referencian por identificador. Cada pista incluye atributos como la ubicación del fichero. | Formato candidato de exportación (RF-21, ADR-005). |
| **M3U / M3U8** | Formato de texto de listas de reproducción: una ruta de fichero por línea; M3U8 usa codificación UTF-8. | Formato alternativo de exportación; también usado en el panel (RF-28). |
| **Ruta resuelta** | Ruta de un fichero expresada de modo que la aplicación destino lo localice sin ambigüedad. | RF-22, RNF-22. |
| **Identificador de pista** | Valor que identifica de forma única una pista con independencia de su nombre o ubicación (por ejemplo, un resumen criptográfico del contenido). | Base de RF-09 y RNF-04. |
| **Fuente única de verdad** | Almacén que contiene la versión oficial de los datos. | La base de datos local (O3). |
| **Origen del descriptor** | Indicación de si un valor procede de las etiquetas o de la estimación. | RF-07. |

## 4. Evaluación

| Término | Definición | Relevancia en el sistema |
|---|---|---|
| **Valor de referencia** | Valor de BPM o tonalidad usado como patrón de comparación (aquí, el de Rekordbox para las mismas pistas). | RF-29. No es una verdad absoluta y se discute en la memoria. |
| **Exactitud de BPM estricta** | Proporción de pistas cuyo BPM estimado está dentro de una tolerancia relativa de la referencia (propuesta: ±4 %). | RNF-05. |
| **Exactitud de BPM con tolerancia de octava** | Igual que la anterior, admitiendo múltiplos y submúltiplos habituales. | RNF-06. |
| **Exactitud de tonalidad** | Proporción de pistas con tónica y modo idénticos a la referencia, o compatibles según Camelot. | RNF-07 y RNF-08. |
| **SUS** | *System Usability Scale*: cuestionario estándar de usabilidad con puntuación de 0 a 100. | RNF-14. |

## 5. Ingeniería del software y arquitectura

| Término | Definición | Relevancia en el sistema |
|---|---|---|
| **Arquitectura limpia (Clean Architecture)** | Organización en capas concéntricas (dominio, aplicación, infraestructura e interfaz) donde las dependencias apuntan hacia el dominio. | Principio rector del diseño (RNF-23). |
| **Regla de dependencia** | Las capas internas no conocen a las externas. | Verificable en CI. |
| **Entidad de dominio** | Objeto con identidad y reglas de negocio independientes de la tecnología. | `Track`, `Setlist`, etc. |
| **Caso de uso** | Operación de la capa de aplicación que orquesta entidades y puertos para lograr un objetivo del usuario. | Catálogo CU-01 a CU-10. |
| **Puerto** | Interfaz definida por el dominio o la aplicación que describe una dependencia externa. | `AudioAnalyzer`, `TrackRepository`, `SetlistExporter`. |
| **Adaptador** | Implementación concreta de un puerto con una tecnología. | Un analizador basado en una librería de audio concreta. |
| **Repositorio** | Puerto que abstrae el almacenamiento y la consulta de entidades. | `TrackRepository`, `SetlistRepository`. |
| **Determinismo** | Misma entrada, mismo resultado. | RNF-11. |
| **Idempotencia** | Repetir una operación no cambia el resultado tras la primera ejecución. | Importaciones repetidas (RNF-04). |
| **ADR** | *Architecture Decision Record*: documento que registra una decisión arquitectónica, sus alternativas y consecuencias. | `DECISIONS_LOG.md` y `docs/adr/`. |
| **MoSCoW** | Técnica de priorización: Must, Should, Could, Won't. | Prioridad de requisitos. |
| **Línea base** | Versión aprobada de un conjunto de documentos que solo cambia mediante control de cambios. | Hito H1. |

## 6. Referencias
Las referencias [1], [3], [4], [6] y [7] corresponden a la bibliografía del anteproyecto: Müller; McFee et al. (librosa); Bogdanov et al. (Essentia); Font, Serrà y Serra (Camelot Wheel); documentación de Rekordbox.
