# Requisitos de SetlistGen

**Versión:** 1.0 · **Estado:** pendiente de revisión por el tutor

## 1. Propósito y alcance

Este documento especifica los requisitos funcionales (RF) y no funcionales (RNF) de SetlistGen: una aplicación local que analiza una biblioteca musical, genera setlists para DJs según parámetros musicales y los guarda en SQLite.

**Dentro del alcance**

- Perfil de DJ con datos privados.
- Análisis de una carpeta local (metadatos, BPM, tonalidad y código Camelot).
- Generación de setlists por restricciones.
- Edición flexible y guardado de setlists.
- Exportación opcional (ampliación, ADR-006).

**Fuera del alcance**

- Reproducción o mezcla de audio.
- Servicios en la nube, streaming y funciones sociales.
- Clasificación automática de género (se lee de las etiquetas).
- Importación de XML de Rekordbox y escritura en su base de datos.
- Almacenamiento de audio en la base de datos.

## 2. Actor y convenciones

**Actor único: el DJ.** Los procesos internos (cálculo del setlist, detección de duplicados) son pasos de los casos de uso, no actores.

- **Prioridad (MoSCoW):** Must, Should, Could.
- **(P):** umbral provisional, que se ratifica tras una prueba con datos reales.
- Los identificadores no se reutilizan.

## 3. Requisitos funcionales

### 3.1 Perfil de DJ

| ID | Requisito | Prioridad | Criterio de aceptación |
|---|---|---|---|
| RF-01 | El sistema permitirá crear y seleccionar un perfil de DJ. Cada perfil tiene sus propias bibliotecas, pistas y setlists, inaccesibles desde otro perfil | Must | Con dos perfiles, ninguno ve los datos del otro |

### 3.2 Bloque 1: Selección y análisis de biblioteca

| ID | Requisito | Prioridad | Criterio de aceptación |
|---|---|---|---|
| RF-02 | El DJ seleccionará una carpeta local y, antes de analizar, el sistema mostrará tamaño total, número de archivos de audio, número de subcarpetas y tiempo estimado de análisis (por muestreo de pistas) | Must | Los valores coinciden con la carpeta. La estimación se muestra antes de lanzar el análisis y se desvía ≤ 30 % del tiempo real (P) |
| RF-03 | El sistema recorrerá la carpeta de forma recursiva y reconocerá los formatos MP3, WAV, FLAC y AIFF, informando de los ficheros descartados y su motivo | Must | Se detectan todas las pistas de las subcarpetas. Cada descarte aparece en el informe |
| RF-04 | El sistema extraerá de cada pista título, artista, duración y género | Must | Un campo ausente queda como nulo y no interrumpe el análisis |
| RF-05 | El sistema estimará el BPM y la tonalidad de cada pista mediante el motor MIR y derivará su código Camelot | Must | Cada pista analizada tiene BPM y tonalidad, o una marca de fallo con su causa. Las 24 tonalidades se corresponden con su código Camelot |
| RF-06 | Antes de analizar cada pista, el sistema comprobará en SQLite si ya fue analizada (por ruta local, tamaño y fecha de modificación) y no la analizará ni la duplicará. Si el tamaño o la fecha han cambiado, la reanalizará y actualizará su registro | Must | Un segundo análisis de la misma carpeta no reanaliza ninguna pista y no crea registros duplicados |
| RF-07 | El sistema mostrará el progreso del análisis y, al terminar, un informe con pistas analizadas, omitidas y fallidas. El fallo de una pista no interrumpe el análisis del resto | Must | Con un fichero corrupto, el análisis termina y el fallo figura en el informe con su causa |
| RF-08 | El sistema permitirá consultar las pistas de la biblioteca filtrando por BPM, tonalidad, género y título, y ordenarlas por BPM, tonalidad, título o duración, de forma ascendente o descendente | Must | Los resultados cumplen los filtros y respetan el orden elegido |

### 3.3 Bloque 2: Parametrización y generación

| ID | Requisito | Prioridad | Criterio de aceptación |
|---|---|---|---|
| RF-09 | El DJ fijará la duración objetivo del setlist (por ejemplo, 2 h 30 min) con una tolerancia configurable (5 % por defecto) | Must | La duración resultante está dentro de la tolerancia |
| RF-10 | El DJ fijará el rango de BPM admisible (por ejemplo, 85–110) | Must | Ninguna pista queda fuera del rango |
| RF-11 | El DJ elegirá la política de compatibilidad armónica Camelot. Por defecto: mismo código, ±1 con la misma letra, o mismo número con letra opuesta. Podrá activar movimientos adicionales (por ejemplo, +2 posiciones para subir la energía) | Must | Todas las transiciones respetan la política elegida |
| RF-12 | El sistema generará una propuesta de setlist ordenada a partir de las pistas candidatas (analizadas correctamente, con fichero existente), sin repetir pistas, que cumpla RF-09 a RF-11 y minimice los saltos de BPM y la disonancia armónica. Aceptará una semilla opcional | Must | Ninguna pista aparece dos veces. Con la misma biblioteca, parámetros y semilla se obtiene el mismo setlist |
| RF-13 | Si no existe una combinación válida, el sistema lo indicará, señalará al menos un conjunto de restricciones en conflicto y no generará un setlist inválido. Si la búsqueda se agota por límite de esfuerzo sin demostrar la inviabilidad, lo informará de forma distinta | Must | Con parámetros contradictorios (por ejemplo, rango de BPM sin pistas) se muestra el conflicto. El mensaje distingue «inviable» de «límite agotado» |

### 3.4 Bloque 3: Edición, guardado y exportación

| ID | Requisito | Prioridad | Criterio de aceptación |
|---|---|---|---|
| RF-14 | El DJ podrá reordenar manualmente las pistas del setlist. El sistema recalculará las transiciones y señalará las que incumplan los parámetros | Must | Tras mover una pista, las transiciones mostradas corresponden al orden actual |
| RF-15 | El DJ podrá ordenar el setlist por BPM ascendente | Should | El setlist queda ordenado por BPM de menor a mayor |
| RF-16 | El DJ podrá fijar una pista concreta como canción inicial | Should | La pista elegida ocupa la primera posición |
| RF-17 | El DJ podrá eliminar pistas del setlist | Must | La pista desaparece y las transiciones se recalculan |
| RF-18 | El DJ podrá añadir manualmente cualquier pista de la biblioteca, aunque incumpla los parámetros. El sistema mostrará un aviso visual no bloqueante y no admitirá una pista ya incluida | Must | Se añade una pista fuera del rango de BPM con aviso y sin impedirlo. Una pista repetida se rechaza |
| RF-19 | El DJ guardará el setlist en SQLite con su nombre, fecha, parámetros, semilla y pistas en orden. Solo se almacenan rutas y descriptores | Must | Un setlist guardado se recupera con el mismo orden y los mismos parámetros |
| RF-20 | El DJ podrá consultar, abrir y eliminar sus setlists guardados. Al abrir uno, el sistema avisará de las pistas cuyo fichero ya no exista | Must | La lista muestra solo los setlists del DJ activo. Una pista movida en disco se señala al abrir |
| RF-21 | El DJ podrá exportar un setlist guardado copiando sus pistas, en orden, a una carpeta local (ADR-006) | Could | La carpeta contiene los ficheros con un prefijo numérico que conserva el orden |
| RF-22 | El DJ podrá exportar un setlist guardado como lista `.m3u8` (UTF-8) con las rutas locales (ADR-006) | Could | La lista se importa en Rekordbox con las pistas resueltas. Las rutas con tildes y espacios funcionan |

## 4. Requisitos no funcionales

| ID | Requisito | Métrica y umbral | Verificación | Prioridad |
|---|---|---|---|---|
| RNF-01 | **Procesamiento local.** Ningún fichero de audio ni dato de la biblioteca sale del equipo | 0 conexiones de red en el análisis, la generación y el guardado | Revisión de diseño y de dependencias | Must |
| RNF-02 | **Exactitud de BPM.** Frente a los valores de Rekordbox sobre una muestra de la biblioteca | ≥ 85 % dentro de ±4 %, y ≥ 92 % admitiendo errores de octava (factores 2, 1/2, 3, 1/3) (P) | Comparación sobre muestra con desglose de errores | Must |
| RNF-03 | **Exactitud de tonalidad.** Misma muestra | ≥ 65 % de coincidencia exacta y ≥ 80 % de compatibilidad Camelot con la referencia (P) | Comparación sobre muestra | Must |
| RNF-04 | **Tiempo de análisis** | Media ≤ 10 % de la duración de la pista por núcleo (P) | Benchmark sobre la biblioteca de prueba | Should |
| RNF-05 | **Tiempo de generación** | Setlist de 2 h sobre 5 000 pistas en ≤ 60 s, percentil 95 (P) | Benchmark | Should |
| RNF-06 | **Determinismo** | Misma biblioteca, parámetros y semilla producen el mismo setlist | Test automatizado | Must |
| RNF-07 | **Cumplimiento de restricciones** | 100 % de las transiciones de un setlist generado y no editado cumplen el rango de BPM y la política armónica | Tests de propiedades | Must |
| RNF-08 | **Persistencia ligera.** SQLite en un único fichero, solo rutas y descriptores, sin audio | 0 binarios de audio en la base. 0 pistas reanalizadas en un segundo análisis | Test de integración | Must |
| RNF-09 | **Integridad.** Una interrupción no deja la base inconsistente | Las escrituras de cada pista y de cada setlist son atómicas | Test de interrupción | Must |
| RNF-10 | **Arquitectura desacoplada.** El dominio y la aplicación no importan librerías de audio, de base de datos ni de interfaz. El motor MIR y el almacenamiento se acceden por interfaces sustituibles. Calidad de código | Comprobación automática de dependencias. Cobertura ≥ 80 % en dominio y aplicación | Integración continua | Must |
| RNF-11 | **Compatibilidad.** Windows 10/11 y macOS vigente, con rutas con espacios, tildes y caracteres Unicode | Mismos resultados funcionales en ambos sistemas | Pruebas en ambos sistemas | Must |
| RNF-12 | **Retroalimentación al DJ.** Progreso en operaciones de más de 5 s y mensajes de error con causa y acción sugerida | Revisión de todas las pantallas de análisis, generación y guardado | Pruebas funcionales y revisión | Should |

## 5. Resumen MoSCoW

| | Must | Should | Could | Total |
|---|---:|---:|---:|---:|
| RF | 18 | 2 (RF-15, RF-16) | 2 (RF-21, RF-22) | 22 |
| RNF | 9 | 3 (RNF-04, RNF-05, RNF-12) | 0 | 12 |

## 6. Supuestos y límites

- Los valores de Rekordbox son una referencia práctica y no una verdad absoluta. Las discrepancias son diferencias entre dos estimadores.
- Una pista se identifica por su ruta, tamaño y fecha. Un fichero movido o renombrado se trata como pista nueva y se reanaliza.
- Un perfil de DJ es un perfil local sin autenticación. Aísla los datos, pero no sustituye a la seguridad del sistema operativo.
- El formato de la interfaz (escritorio o web local) está pendiente de decisión y no condiciona estos requisitos.
- Los umbrales (P) se ratifican tras una prueba con datos reales.

## 7. Control de cambios

| Versión | Cambio |
|---|---|
| 1.0 | Requisitos reescritos desde cero tras el replanteamiento del alcance: actor único, tres bloques funcionales, 22 RF y 12 RNF |