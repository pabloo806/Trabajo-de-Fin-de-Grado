# ADR-010: Identificación Permanente de Pistas

## Estado

**Propuesto** (OD-03). Pendiente de validación por tutor y cotutor y de una prueba de concepto que mida coste y fiabilidad de cada técnica sobre ficheros reales. No cierra OD-03 por sí mismo: la deja formulada con una recomendación y con los datos que faltan para decidir.

## Fecha

2026-10-30

## Requisitos relacionados

| Requisito | Relación |
|---|---|
| RF-09 | Identificador único e independiente del nombre y de la ubicación |
| RF-09b | Analizar únicamente las pistas cuyo identificador no existe |
| RF-09c | Detección de pistas movidas, duplicadas y ausentes |
| RNF-04 | 0 pistas reanalizadas en una segunda importación; detección en ≤ 2 min para 5 000 pistas (P) |
| RNF-15 | Un fallo en una pista no interrumpe el lote |
| RNF-16, RNF-21 | Rutas con Unicode y espacios; el dominio no depende del formato de ruta |
| RNF-17 | Una interrupción no deja la base de datos inconsistente |
| RNF-19, RNF-20, RNF-25, RNF-26 | Instalación en Windows y macOS, procesamiento local y licencias de lo que se adopte |
| RNF-22, RNF-23 | Identificación tras un puerto sustituible (`TrackIdentifier`, ADR-002) |

Decisión abierta: OD-03. Hallazgos y asuntos relacionados: H-19 (pistas movidas o ausentes), OD-07 (entidades `Track` y `TrackLocation`) y el flujo alternativo A3 de CU-02 (fichero conocido cuyo contenido ha cambiado).

## Contexto

RF-09 exige que una pista conserve su identidad aunque cambie de nombre o de ubicación. La identidad no puede depender de la ruta, del nombre del fichero ni de la carpeta.

La identidad es la base de varias funciones:

- Evitar reanalizar material ya procesado (RF-09b, RNF-04).
- Conservar el histórico de setlists y los resultados de análisis cuando el DJ reorganiza su biblioteca (RF-09c).
- Asociar los valores de referencia de Rekordbox con las pistas (RF-29b).
- Detectar duplicados.

Un error de identificación tiene dos formas con consecuencias distintas:

- **Falso negativo:** una pista conocida se trata como nueva. Se reanaliza y puede duplicarse, pero no se pierde información.
- **Falso positivo:** dos pistas distintas se tratan como una. Se mezclan sus descriptores y su histórico, lo que corrompe los datos de forma difícil de detectar.

El requisito RNF-04 impone además un límite de tiempo muy estricto. Detectar las pistas nuevas de una biblioteca de 5 000 ficheros en 2 minutos deja unos 24 ms por pista. Esto condiciona qué técnicas pueden usarse sobre todos los ficheros.

### Orden de magnitud del coste (por medir)

Las cifras siguientes son estimaciones de orden de magnitud, basadas en supuestos de tamaño de fichero y de velocidad de disco. **No están medidas** y se sustituyen por mediciones en la prueba de concepto.

| Operación sobre 5 000 pistas | Coste estimado | Compatibilidad con 24 ms por pista |
|---|---|---|
| Leer tamaño y fecha de modificación | Segundos | Sí |
| Leer un único bloque contiguo pequeño de cada fichero | Segundos en SSD; decenas de segundos en disco mecánico | Probable |
| Leer y resumir cada fichero completo | Del orden de minutos en SSD con MP3; mayor con WAV, FLAC o AIFF y con disco mecánico | Dudosa |
| Descodificar el audio de cada pista | Del orden de un segundo o más por pista; horas en total | No |

La consecuencia es que ninguna técnica que lea o descodifique cada fichero completo puede aplicarse a toda la biblioteca en cada reescaneo.

## Problema

Definir cómo se identifica de forma permanente una pista y cómo se reconoce en importaciones posteriores, cumpliendo RF-09 y RNF-04, minimizando los falsos positivos y sin introducir dependencias que comprometan la instalación o las licencias.

## Alternativas consideradas

### E1. Hash del fichero completo como identidad (OD-03, A1)

**Ventajas:** implementación sencilla con la biblioteca estándar; sin falsos positivos prácticos; determinista; sin dependencias.

**Inconvenientes:** cambia al modificar las etiquetas, que los DJ editan con frecuencia, de modo que la pista pierde su identidad; requiere leer cada fichero completo, lo que compromete RNF-04.

---

### E2. Hash del contenido de audio descodificado (OD-03, A2)

**Ventajas:** independiente de las etiquetas; sigue siendo exacto; identifica el mismo audio en contenedores sin pérdida distintos si las muestras coinciden.

**Inconvenientes:** exige descodificar cada pista, con un coste elevado que impide RNF-04 aplicado a toda la biblioteca; depende de un descodificador por formato; no tolera la recodificación con pérdida.

---

### E3. Fingerprint acústico como identidad única (OD-03, A3)

Huella compacta derivada del contenido sonoro, diseñada para identificación musical.

**Ventajas:** diseñada para identificar música; tolera determinadas modificaciones, como la recodificación; independiente de las etiquetas.

**Inconvenientes:** requiere descodificar el audio, con el mismo problema de coste que E2; comparación probabilística con umbrales, lo que introduce riesgo de falsos positivos y de falsos negativos; mayor complejidad; dependencia de una librería con licencia e instalación por verificar (ADR-007); los servicios de identificación en línea quedan excluidos por RNF-25.

---

### E4. Identificación en dos niveles

Un primer nivel barato reconoce las pistas ya conocidas sin descodificar el audio, y un segundo nivel, más caro, se aplica solo a lo que el primero no reconoce o a los casos ambiguos.

**Ventajas:** compatible con RNF-04, porque el caso mayoritario (reescaneo sin cambios) se resuelve con datos del sistema de archivos; el coste elevado solo se paga por los ficheros nuevos, que ya se descodifican para analizarse; mantiene la identidad cuando se editan las etiquetas, según la técnica del segundo nivel.

**Inconvenientes:** mayor complejidad de diseño y de pruebas; la técnica del segundo nivel sigue por decidir; hay que gestionar varios tipos de dato de identificación.

---

## Criterios de evaluación

| Criterio | Peso |
|-----------|------:|
| Cumplimiento de RNF-04 (tiempo de reescaneo) | 5 |
| Estabilidad ante la edición de etiquetas (RF-09) | 4 |
| Tolerancia a la recodificación | 3 |
| Riesgo de falsos positivos y negativos | 5 |
| Complejidad de implementación y de instalación | 4 |
| Dependencias y licencia (ADR-007) | 4 |
| Testabilidad y determinismo | 3 |

Escala de valoración: 1 (muy deficiente) a 5 (excelente). Total = Σ (Valoración × Peso).

## Evaluación de alternativas (inicial y provisional)

| Criterio | Peso | E1 Hash completo | E2 Hash de audio | E3 Fingerprint | E4 Dos niveles |
|---|---:|---:|---:|---:|---:|
| Cumplimiento de RNF-04 | 5 | 2 (10) | 1 (5) | 1 (5) | 5 (25) |
| Estabilidad ante etiquetas | 4 | 1 (4) | 5 (20) | 5 (20) | 4 (16) |
| Tolerancia a la recodificación | 3 | 1 (3) | 3 (9) | 5 (15) | 4 (12) |
| Falsos positivos y negativos | 5 | 4 (20) | 4 (20) | 3 (15) | 4 (20) |
| Complejidad e instalación | 4 | 5 (20) | 3 (12) | 2 (8) | 3 (12) |
| Dependencias y licencia | 4 | 5 (20) | 3 (12) | 2 (8) | 3 (12) |
| Testabilidad y determinismo | 3 | 5 (15) | 4 (12) | 2 (6) | 4 (12) |
| **Total** | | **92** | **90** | **77** | **109** |

Las valoraciones son estimaciones previas a la medición. La ventaja de E4 viene sobre todo de RNF-04: E1, E2 y E3 podrían combinarse con un primer nivel barato y convertirse en variantes de E4.

## Decisión propuesta

Se propone adoptar **E4 (identificación en dos niveles)**.

### Niveles

| Nivel | Datos usados | Función | Coste |
|---|---|---|---|
| 1a | Ubicación, tamaño y fecha de modificación | Reconocer pistas sin cambios | Mínimo, sin leer contenido |
| 1b | Huella rápida: resumen de un bloque contiguo del contenido del fichero, relativo al inicio de los datos de audio y no del fichero | Reconocer pistas movidas o renombradas y resolver pistas con ubicación nueva | Bajo, una lectura pequeña por fichero |
| 2 | Huella de contenido del audio descodificado (técnica por decidir: hash de audio o fingerprint acústico) | Resolver ambigüedades y detectar duplicados de contenido | Alto; se aplica solo a pistas no reconocidas por el nivel 1 |

El nivel 2 se calcula con el audio que el motor de análisis ya descodifica para las pistas nuevas, de modo que su coste adicional es bajo en el caso habitual.

### Técnica del nivel 2: pendiente de la prueba de concepto

La elección entre hash del audio descodificado y fingerprint acústico se decide con medidas, no a priori. Criterios:

- Cero falsos positivos sobre el conjunto de prueba, incluidas versiones distintas de una misma obra (por ejemplo, radio y extendida), que no deben coincidir.
- Cero falsos negativos ante renombrado, movimiento y edición de etiquetas.
- Comportamiento ante conversión sin pérdida y recodificación: deseable, no exigido.
- Coste, instalación en Windows y macOS y licencia (ADR-007).

### Principio de decisión: preferir el falso negativo

Ante la duda, una pista se trata como nueva y se señala como posible duplicado, y no se fusiona con otra. Un duplicado se puede informar al DJ (RF-09c); una fusión indebida corrompe datos de forma silenciosa.

### Reglas de reconocimiento

| Situación | Resultado |
|---|---|
| La ubicación existe y tamaño y fecha coinciden | Pista conocida, sin cambios |
| La ubicación es nueva y la huella rápida coincide con una pista cuya ubicación anterior ya no existe | Pista movida: se actualiza su ubicación y se conservan identificador, descriptores y setlists |
| La ubicación es nueva y la huella rápida coincide con una pista cuya ubicación anterior sigue existiendo | Pista duplicada: una pista con dos ubicaciones |
| La huella rápida coincide con varias pistas | Ambigüedad: se resuelve con el nivel 2 |
| La ubicación es nueva y no hay coincidencia | Pista nueva: se asigna un identificador nuevo y se analiza |
| Una ubicación conocida ya no existe y su pista no aparece en otra | Pista ausente: se marca, no se elimina |
| El fichero no se puede leer | Marca de fallo con su causa; el lote continúa (RNF-15) |
| La ubicación existe pero tamaño o fecha han cambiado | **Fichero modificado** (véase más abajo) |

### Fichero modificado en la misma ubicación (CU-02, A3)

Se propone tratar la ubicación como continuidad de la misma pista por defecto, y recalcular la huella para comprobarlo. Si la huella rápida, que no depende de las etiquetas, sigue coincidiendo, se conserva la identidad y solo se actualizan los metadatos. Si ya no coincide, el audio puede haber sido sustituido: se trata como pista nueva en esa ubicación y la anterior queda marcada como ausente. Esta política **debe validarse con los tutores** como parte de OD-03.

### Alcance de la identidad: pregunta abierta

La identidad propuesta distingue ficheros con distinto contenido de audio. Una misma grabación en dos codificaciones distintas (por ejemplo, un WAV y un MP3) se trataría como dos pistas, salvo que el nivel 2 sea un fingerprint tolerante y se decida fusionarlas. Que el DJ pueda querer mantener ambas versiones como pistas separadas favorece la opción conservadora. La decisión final es un criterio de dominio que debe confirmarse con los tutores.

## Diseño del puerto

El puerto `TrackIdentifier` (ADR-002) **calcula** los datos de identificación de un fichero: huella rápida y, si se solicita, huella de contenido. No consulta la base de datos.

La **decisión de reconocimiento**, que compara esos datos con los almacenados y aplica la tabla de reglas, es lógica de aplicación y de dominio. De ese modo se puede probar con dobles, sin necesidad de audio real (RNF-23).

| Aspecto | Contrato |
|---|---|
| Entrada | Ubicación de un fichero y, opcionalmente, el nivel solicitado |
| Salida | Datos de identificación calculados, con la versión del algoritmo |
| Fallo | Marca de fallo con su causa, sin propagar errores de la librería |
| Efectos secundarios | Ninguno |
| Servicios externos | Ninguno: no se usa ningún servicio de identificación en línea (RNF-25) |

Los hashes se calculan con funciones de la biblioteca estándar y un tamaño suficiente para que las colisiones sean despreciables. La técnica del nivel 2, si requiere una librería, se somete a ADR-007.

## Datos que debe almacenar la persistencia

| Dato | Pertenece a | Uso |
|---|---|---|
| Identificador interno de la pista | Pista | Identidad permanente, independiente de la ruta (RF-09) |
| Ubicación, tamaño y fecha de modificación | Ubicación | Nivel 1a |
| Huella rápida | Pista o ubicación | Nivel 1b |
| Huella de contenido (opcional) | Pista | Nivel 2 |
| Versión del algoritmo de identificación | Cada huella | Permite recalcular o migrar si el algoritmo cambia (RNF-27) |
| Estado de la ubicación | Ubicación | Activa, movida o ausente (RF-09c) |

Impacto en OD-07: la entidad propuesta `Track` tiene un único campo `fingerprint`. Con identificación en dos niveles harían falta, al menos, una huella rápida y una huella de contenido opcional, y debe decidirse a qué entidad pertenece cada una.

## Casos de prueba previstos

Casos para la prueba de concepto de identificación. Los identificadores son provisionales y deberán incorporarse al catálogo de pruebas de la matriz de trazabilidad.

| ID | Descripción | Resultado esperado |
|---|---|---|
| T-ID-01 | Renombrar y mover una pista | Misma pista, ubicación actualizada, sin reanálisis |
| T-ID-02 | Editar las etiquetas de una pista | Misma pista, sin reanálisis |
| T-ID-03 | Convertir una pista a otro formato sin pérdida | Resultado según el alcance de identidad decidido |
| T-ID-04 | Recodificar una pista con otra tasa de bits | Resultado según el alcance de identidad decidido |
| T-ID-05 | Dos versiones distintas de una misma obra | Pistas distintas, sin fusión |
| T-ID-06 | Dos ubicaciones del mismo fichero | Una pista duplicada |
| T-ID-07 | Fichero ilegible | Marca de fallo y el lote continúa |
| T-ID-08 | Reescaneo de 5 000 pistas sin cambios y tras mover la carpeta completa | Tiempo dentro del objetivo de RNF-04 y 0 reanálisis |

## Justificación

La propuesta de OD-03 era evaluar un fingerprint acústico. Se apartó de ella porque el fingerprint exige descodificar el audio de cada pista, y RNF-04 deja unos 24 ms por pista en cada reescaneo. Ninguna técnica que lea o descodifique el fichero completo puede cumplir ese límite sin un primer nivel barato.

La identificación en dos niveles reserva el coste elevado a las pistas nuevas, que de todas formas se descodifican para analizarse, y mantiene el criterio conservador de preferir un duplicado a una fusión indebida.

## Consecuencias

### Positivas

- Compatible con RNF-04 en el caso mayoritario.
- La identidad sobrevive al renombrado, al movimiento y, según la técnica elegida, a la edición de etiquetas.
- El riesgo principal, la fusión indebida de pistas, se evita por diseño.
- La lógica de reconocimiento se puede probar sin audio.

### Negativas

- Mayor complejidad que una técnica única.
- La técnica del nivel 2 sigue por decidir y puede introducir una dependencia con licencia por verificar.
- Tratar una misma grabación en dos formatos como dos pistas puede producir duplicados que el DJ debe gestionar.
- El modelo de datos necesita más campos de los previstos en OD-07.

## Trazabilidad

| Elemento | Referencias |
|---|---|
| Requisitos funcionales | RF-09, RF-09b, RF-09c, RF-29b |
| Requisitos no funcionales | RNF-04, RNF-15, RNF-16, RNF-17, RNF-21, RNF-22, RNF-23, RNF-25, RNF-26, RNF-27 |
| Componentes | CMP-01 (importación) y CMP-03 (base de datos) |
| Casos de uso | CU-01 y CU-02 |
| Casos de prueba | T-CU01-05, T-CU02-01, T-CU02-02, T-RNF-04, T-ID-01 a T-ID-08 |
| Decisiones abiertas | OD-03, OD-07 |
| Riesgos | R-08, R-10 |

## Evidencias utilizadas

- RF-09, RF-09b, RF-09c y RNF-04 del SRS v4.0.
- OD-03 y sus tres alternativas, y la propuesta inicial de evaluar un fingerprint acústico.
- CU-02, incluido su flujo alternativo A3 sobre ficheros modificados.
- Entidades propuestas en OD-07 (`Track`, `TrackLocation`).
- ADR-002 (puerto `TrackIdentifier`), ADR-003 (el motor descodifica el audio), ADR-004 (almacenamiento) y ADR-007 (licencias).

## Impacto en el proyecto

- Condiciona el modelo de datos: identificador interno, ubicaciones con tamaño y fecha, y huellas con versión de algoritmo.
- Introduce una prueba de concepto de identificación con medición real de coste y fiabilidad.
- Obliga a revisar la entidad `Track` de OD-07 antes de congelar el modelo.
- Define el comportamiento de CU-02 para ficheros modificados, que debe validarse con los tutores.

## Impacto en la memoria

Guardar este contenido para la memoria del TFG.

- **Capítulo 4, sección 4.6:** decisión abierta que se cierra al aceptar este ADR.
- **Capítulo 6, secciones 6.2 y 6.3:** modelo de dominio y de datos, con la identidad de pista y las ubicaciones.
- **Capítulo 7, sección 7.3:** implementación de la importación y de la identificación.
- **Capítulo 8, secciones 8.2:** pruebas T-ID.
- **Apéndice B, sección B.2:** incluir este ADR.

Bloque reutilizable:

- **Contexto:** una pista debe conservar su identidad al cambiar de nombre o ubicación, y un reescaneo de 5 000 pistas debe completarse en minutos.
- **Problema:** elegir cómo se identifica una pista sin que el coste impida los reescaneos y sin fusionar pistas distintas.
- **Alternativas:** hash del fichero, hash del audio, fingerprint acústico e identificación en dos niveles.
- **Solución propuesta:** dos niveles, uno barato con datos del sistema de archivos y una huella rápida, y otro caro con huella de contenido solo para lo no reconocido.
- **Justificación:** mejor puntuación (109 frente a 92, 90 y 77) y compatibilidad con el límite de tiempo de reescaneo.
- **Ventajas:** identidad estable ante renombrados y cambios de etiquetas, y prioridad del duplicado sobre la fusión indebida.
- **Limitaciones:** técnica del segundo nivel por decidir y mayor complejidad.
- **Impacto:** condiciona el modelo de datos y exige una prueba de concepto de identificación.

## Decisiones relacionadas

- ADR-001: Forma de Distribución del Sistema.
- ADR-002: Arquitectura General del Sistema.
- ADR-003: Motor de Análisis Musical.
- ADR-004: Persistencia.
- ADR-005: Algoritmo de Generación de Setlists.
- ADR-006: Exportación e Integración con Rekordbox.
- ADR-007: Licencias y compatibilidad legal (propuesto).
- ADR-008: Lenguaje, interfaz gráfica y empaquetado (propuesto).
- ADR-009: Dataset y protocolo de evaluación (propuesto).
