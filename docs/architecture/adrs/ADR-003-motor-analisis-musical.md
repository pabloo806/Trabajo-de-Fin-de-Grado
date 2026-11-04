[ADR-003-motor-analisis-musical.md](https://github.com/user-attachments/files/34364334/ADR-003-motor-analisis-musical.md)
# ADR-003: Motor de Análisis Musical

## Estado

Aceptado (revisado el 2026-10-30). La decisión arquitectónica (puerto de análisis desacoplado) está aceptada. La **selección de la librería concreta queda condicionada a la prueba de concepto** (hito H2) y a ADR-007.

## Fecha

2026-10-28 (decisión original) · 2026-10-30 (revisión de alineación con la línea base documental)

## Requisitos relacionados

| Requisito | Relación |
|---|---|
| RF-03 | Lectura de etiquetas (puerto `MetadataReader`, fuera del motor de análisis) |
| RF-04, RF-05 | Estimación de BPM y tonalidad a partir de la señal |
| RF-06 | Derivación del código Camelot (implementación propia en el dominio) |
| RF-07 | Registro de origen, motor y versión; varios resultados por pista **[PROPUESTA · OD-04]** |
| RF-29, RF-29b | Comparación de cada motor con la referencia de Rekordbox |
| RNF-01, RNF-02 | Coste de análisis por pista y por lote |
| RNF-05 a RNF-09 | Exactitud y transparencia de errores |
| RNF-15 | Aislamiento de fallos por pista |
| RNF-19, RNF-20 | Instalación en Windows y macOS |
| RNF-22, RNF-23 | Regla de dependencia y sustituibilidad |
| RNF-26 | Licencias de las dependencias |

Hallazgos y riesgos atendidos: H-08 (soporte multi-motor), N-04 (licencias e instalación de las librerías), R-01, R-08 y R-10 del capítulo 4 de la memoria.

## Contexto

SetlistGen debe analizar automáticamente pistas de audio para obtener información musical utilizada posteriormente en la generación de setlists.

De acuerdo con los requisitos del sistema, el motor de análisis debe ser capaz de:

- Estimar BPM (RF-04).
- Estimar tonalidad (RF-05).
- Permitir derivar el código Camelot (RF-06).
- Procesar bibliotecas completas de audio (RNF-02).
- Ser sustituible por implementaciones alternativas (RNF-23).
- Permitir comparar diferentes librerías de análisis frente a la referencia de Rekordbox (RF-29).
- Registrar qué motor y qué versión produjo cada resultado (RF-07).

Los requisitos no funcionales relacionados con precisión, rendimiento y mantenibilidad hacen recomendable desacoplar el núcleo del sistema de cualquier librería concreta.

El plan del anteproyecto sitúa la prueba de concepto de las librerías antes de la arquitectura. Este ADR se aceptó antes de realizarla; por eso la decisión se limita al desacoplamiento y deja abierta la elección de la librería.

## Problema

Determinar cómo integrará SetlistGen el análisis musical.

## Características de las librerías evaluadas

### Librosa

Lenguaje principal:

- Python

Características relevantes:

- Carga y decodificación de audio.
- Beat tracking.
- Estimación de tempo.
- Cálculo de STFT.
- Espectrogramas Mel.
- MFCC.
- Cromagramas.
- HPSS (separación armónica y percusiva).
- Extracción de características espectrales.
- Segmentación musical.
- Herramientas de visualización.

Puntos fuertes:

- Amplia adopción académica.
- Excelente documentación.
- Ecosistema Python maduro.
- Integración sencilla.

Limitaciones:

- Menor cantidad de descriptores de alto nivel que Essentia.
- Menos orientada a aplicaciones industriales.
- Ofrece cromagramas, pero la estimación de tonalidad sobre ellos requeriría una implementación propia con perfiles de tonalidad. Debe confirmarse en la prueba de concepto.

---

### Essentia

Lenguaje principal:

- C++

Bindings:

- Python
- JavaScript

Características relevantes:

- Beat tracking.
- Estimación de BPM.
- Detección de tonalidad.
- Detección de acordes.
- Similitud musical.
- Segmentación automática.
- Clasificación musical.
- Recomendación basada en audio.
- Audio fingerprinting.
- Caracterización tímbrica.
- Extracción melódica.
- Inferencia mediante modelos TensorFlow.
- Amplia colección de descriptores musicales.

Puntos fuertes:

- Cobertura funcional muy amplia.
- Gran rendimiento.
- Diseñada específicamente para MIR.
- Uso académico e industrial.

Limitaciones:

- Curva de aprendizaje superior.
- Integración más compleja.
- Dependencias más pesadas.
- Posibles restricciones de licencia y de instalación en Windows (véase la sección siguiente).

---

### Madmom

Lenguaje principal:

- Python

Características relevantes:

- Beat tracking.
- Tempo estimation.
- Downbeat tracking.
- Detección de compás.
- Detección de onsets.
- Detección de tonalidad.
- Detección de acordes.
- Modelos basados en machine learning.
- Procesamiento en paralelo mediante Processors.

Puntos fuertes:

- Excelente rendimiento en tareas rítmicas.
- Algoritmos MIR de referencia.
- Muy orientada a investigación.

Limitaciones:

- Menor actividad reciente.
- Ecosistema menor que Librosa.
- Cobertura funcional inferior a Essentia.
- Compatibilidad con la versión de Python y de sus dependencias numéricas por verificar, y posibles restricciones de licencia en los modelos entrenados.

---

### Otras librerías consideradas

**Mutagen.** Librería de Python para leer las etiquetas de los ficheros de audio. Es la candidata para la implementación de `MetadataReader` (RF-03). No analiza la señal y queda fuera del puerto `AudioAnalyzer`.

**Music.py (musicpy).** Descartada como motor de análisis. Según su documentación, opera sobre representaciones simbólicas (notas, acordes, MIDI) y no sobre la señal de audio, por lo que no cubre la estimación de BPM y tonalidad de una grabación. Podría servir como apoyo en operaciones auxiliares de teoría musical, sin formar parte de este ADR.

### Licencias e instalación: hipótesis a verificar

Las siguientes afirmaciones proceden de conocimiento general del autor y **no están verificadas**. Se comprueban en la prueba de concepto y se registran en ADR-007.

| Librería | Cuestión a verificar | Requisitos afectados | Riesgo |
|---|---|---|---|
| Essentia | Licencia copyleft de red (AGPL) frente a la licencia MIT del repositorio; disponibilidad de instalación sencilla en Windows 10/11 | RNF-19, RNF-20, RNF-26 | Alto |
| Madmom | Restricciones de uso no comercial en los modelos entrenados; compatibilidad con la versión de Python elegida | RNF-20, RNF-26 | Medio |
| Librosa | Licencia permisiva; dependencias de decodificación de MP3 y de otros formatos en cada sistema | RF-02, RNF-20 | Bajo |
| Mutagen | Licencia copyleft frente a la licencia MIT del repositorio | RNF-26 | Medio |

Si alguna hipótesis se confirma, la sustituibilidad del puerto permite cambiar de motor sin afectar al dominio, que es el motivo principal de esta decisión.

## Alternativas consideradas

### A1. Acoplamiento directo a una única librería

El sistema utilizaría una única librería de análisis integrada directamente en la lógica de negocio.

#### Ventajas

- Menor complejidad inicial.
- Menor número de clases e interfaces.
- Desarrollo más rápido.

#### Inconvenientes

- Difícil sustitución de la librería.
- Dependencia tecnológica elevada.
- Menor facilidad para pruebas comparativas.

---

### A2. Puerto de análisis con implementaciones sustituibles

La lógica de negocio depende únicamente de una interfaz de análisis musical.

Las librerías concretas se implementan mediante adaptadores independientes.

#### Ventajas

- Desacoplamiento tecnológico.
- Comparación sencilla entre librerías.
- Mayor mantenibilidad.
- Compatible con Clean Architecture.

#### Inconvenientes

- Mayor complejidad inicial.
- Necesidad de diseñar contratos de integración.

---

### A3. Desarrollo de un motor propio completo

Implementación desde cero de los algoritmos de análisis.

#### Ventajas

- Control absoluto sobre los algoritmos.
- Independencia de terceros.

#### Inconvenientes

- Esfuerzo excesivo para el alcance del TFG.
- Riesgo elevado.
- Menor tiempo disponible para el resto del proyecto.

---

## Criterios de evaluación

| Criterio | Peso |
|-----------|------:|
| Exactitud potencial | 5 |
| Mantenibilidad | 5 |
| Sustituibilidad | 5 |
| Facilidad de pruebas | 4 |
| Complejidad de implementación | 3 |
| Riesgo técnico | 5 |

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

### Acoplamiento directo a una única librería

| Criterio | Peso | Valoración | Resultado |
|-----------|------:|-----------:|----------:|
| Exactitud potencial | 5 | 4 | 20 |
| Mantenibilidad | 5 | 2 | 10 |
| Sustituibilidad | 5 | 1 | 5 |
| Facilidad de pruebas | 4 | 2 | 8 |
| Complejidad de implementación | 3 | 5 | 15 |
| Riesgo técnico | 5 | 2 | 10 |

**Total: 68**

---

### Puerto de análisis con adaptadores sustituibles

| Criterio | Peso | Valoración | Resultado |
|-----------|------:|-----------:|----------:|
| Exactitud potencial | 5 | 5 | 25 |
| Mantenibilidad | 5 | 5 | 25 |
| Sustituibilidad | 5 | 5 | 25 |
| Facilidad de pruebas | 4 | 5 | 20 |
| Complejidad de implementación | 3 | 3 | 9 |
| Riesgo técnico | 5 | 5 | 25 |

**Total: 129**

---

### Motor propio completo

| Criterio | Peso | Valoración | Resultado |
|-----------|------:|-----------:|----------:|
| Exactitud potencial | 5 | 3 | 15 |
| Mantenibilidad | 5 | 3 | 15 |
| Sustituibilidad | 5 | 5 | 25 |
| Facilidad de pruebas | 4 | 3 | 12 |
| Complejidad de implementación | 3 | 1 | 3 |
| Riesgo técnico | 5 | 1 | 5 |

**Total: 75**

Los tres totales se han verificado y no se modifican en esta revisión.

---

## Asignación de responsabilidades

La comparación funcional muestra que ninguna librería domina absolutamente todas las tareas necesarias para el proyecto.

Por ello se considera la siguiente estrategia:

| Necesidad | Librería candidata | Requisito |
|------------|-------------------|---|
| Lectura de etiquetas | Mutagen, tras el puerto `MetadataReader` | RF-03 |
| Lectura y preprocesado de audio | Librosa | RF-04, RF-05 |
| STFT y espectrogramas | Librosa | RF-04, RF-05 |
| Cromagramas | Librosa / Essentia | RF-05 |
| Estimación de BPM | Essentia / Madmom | RF-04 |
| Beat tracking | Madmom | RF-04 |
| Estimación de tonalidad | Essentia | RF-05 |
| Derivación de código Camelot | Implementación propia, en el dominio | RF-06 |
| Evaluación comparativa frente a Rekordbox | Essentia + Librosa + Madmom | RF-29 |
| Extracción de características avanzadas | Essentia | Fuera del alcance de los requisitos actuales |

### Estrategia adoptada

La arquitectura desacoplará el análisis musical mediante un puerto común.

Inicialmente se priorizará Essentia como motor principal debido a su cobertura funcional, **sujeto al resultado de la prueba de concepto y de las comprobaciones de licencia e instalación**.

Librosa y Madmom permanecerán disponibles para:

- Pruebas comparativas.
- Validación experimental.
- Sustitución futura.
- Construcción de prototipos específicos.

## Decisión

SetlistGen utilizará un puerto de análisis musical desacoplado de cualquier librería concreta, denominado `AudioAnalyzer` (en la versión 1.0 de este ADR, `AnalysisEngine`).

Las implementaciones específicas se proporcionarán mediante adaptadores independientes.

La selección definitiva de la librería de análisis se realizará mediante una prueba de concepto posterior, con los criterios de la sección siguiente, y se registrará como revisión de este ADR.

**[PROPUESTA · OD-04]** Una pista podrá conservar resultados de varios motores y versiones. Existirá un **motor activo** configurable, cuyos resultados consume el generador, y los demás resultados permanecerán disponibles para la evaluación (RF-07, RF-29).

## Contrato del puerto `AudioAnalyzer`

Descripción conceptual. Los detalles de firma y de tipos se fijan en el diseño del modelo de dominio.

| Aspecto | Contrato |
|---|---|
| Entrada | Ubicación de un fichero de audio en un formato admitido (MP3, WAV, FLAC o AIFF) |
| Salida correcta | BPM, tónica y modo de la tonalidad y, si el motor la ofrece, una medida de confianza |
| Identidad del motor | Nombre y versión, para registrar el origen del resultado (RF-07) |
| Salida de fallo | Marca de fallo con su causa. El adaptador no propaga errores de la librería al dominio (RNF-15) |
| Código Camelot | No lo calcula el adaptador: se deriva en el dominio a partir de la tonalidad (RF-06) |
| Efectos secundarios | Ninguno. No escribe en la base de datos ni en el sistema de archivos |
| Medición | El tiempo de análisis puede medirse desde fuera del adaptador (RNF-01) |
| Concurrencia | El adaptador admite su uso en un análisis por lotes (RNF-02) |

Un adaptador que no ofrezca alguno de los dos descriptores lo indica como marca de fallo, no con un valor inventado.

## Criterios para la selección de la librería (prueba de concepto)

Los criterios proceden de la tabla 2.2 de la memoria y se aplican por cada candidata sobre el conjunto de evaluación de ADR-009.

| Criterio | Cuestión que debe responderse | Requisitos |
|---|---|---|
| Instalación y portabilidad | ¿Se instala de forma reproducible en Windows 10/11 y macOS? | RNF-19, RNF-20 |
| Licencia | ¿Es compatible con la licencia del repositorio y con su distribución? | RNF-26, ADR-007 |
| Formatos soportados | ¿Lee MP3, WAV, FLAC y AIFF? | RF-02 |
| Exactitud de tempo | ¿Qué proporción de pistas queda dentro de tolerancia, con y sin errores de octava? | RNF-05, RNF-06 |
| Exactitud de tonalidad | ¿Qué coincidencia exacta y de compatibilidad Camelot obtiene? | RNF-07, RNF-08 |
| Coste computacional | ¿Qué tiempo de análisis necesita por pista y por lote? | RNF-01, RNF-02 |
| Integración | ¿Se encapsula tras el puerto sin filtrar su API? | RNF-22, RNF-23 |
| Mantenimiento | ¿Tiene actividad, documentación y versiones estables? | — |

**Propuesta de uso:** los dos primeros criterios son eliminatorios; entre las candidatas restantes se comparan la exactitud y el coste. Los umbrales numéricos de RNF-05 a RNF-08 son provisionales (P) hasta esa prueba.

## Arquitectura prevista

```text
AudioAnalyzer (Puerto, en la capa de Aplicación)
│
├── EssentiaAdapter
├── LibrosaAdapter
├── MadmomAdapter
└── Otros adaptadores futuros

MetadataReader (Puerto, en la capa de Aplicación)
│
└── Adaptador de etiquetas (Mutagen, candidato)
```

La capa de aplicación y el dominio dependerán exclusivamente de las interfaces `AudioAnalyzer` y `MetadataReader`.

## Justificación

Esta estrategia permite:

- Comparar tecnologías de análisis durante el desarrollo.
- Sustituir una librería sin modificar la lógica de negocio.
- Realizar pruebas de concepto objetivas.
- Cumplir los requisitos de mantenibilidad y sustituibilidad.
- Reaccionar con bajo coste si una librería resulta incompatible por licencia o por instalación.

Además, encaja con la arquitectura definida en ADR-002.

## Consecuencias

### Positivas

- Independencia tecnológica.
- Mayor facilidad para pruebas.
- Comparación objetiva de librerías.
- Evolución sencilla del sistema.
- Varios motores pueden coexistir y compararse frente a la referencia (RF-07, RF-29).

### Negativas

- Mayor complejidad de diseño.
- Necesidad de desarrollar adaptadores.
- Incremento moderado del esfuerzo inicial.
- Cada adaptador debe normalizar las diferencias de salida entre librerías, como la representación de la tonalidad y la confianza.
- Si la prueba de concepto descarta la librería prevista, el trabajo previo sobre ese adaptador se pierde y puede retrasarse el cierre de la decisión (riesgo R-10).

## Trazabilidad

| Elemento | Referencias |
|---|---|
| Requisitos funcionales | RF-03 a RF-07, RF-29, RF-29b |
| Requisitos no funcionales | RNF-01, RNF-02, RNF-05 a RNF-09, RNF-15, RNF-19, RNF-20, RNF-22, RNF-23, RNF-26 |
| Componentes | CMP-02 (motor de análisis) y CMP-01 (para `MetadataReader`) |
| Casos de prueba | T-CU01-03, T-CU01-04, T-CU01-05, T-RNF-01, T-RNF-05, T-RNF-23, T-RNF-26 |
| Decisiones abiertas | OD-04 (multi-motor) |
| Riesgos | R-01, R-08, R-10 |

## Evidencias utilizadas

- Requisitos de estimación de BPM y tonalidad (RF-04, RF-05).
- Requisitos de mantenibilidad y sustituibilidad (RNF-22, RNF-23).
- Requisito de contrastar cada motor con la referencia de Rekordbox (RF-29).
- Necesidad de realizar una prueba de concepto tecnológica (plan del anteproyecto, tarea 2).
- Estado del arte de las librerías de análisis (capítulo 2 de la memoria, sección 2.3).
- Hallazgos H-08 y N-04.

## Impacto en el proyecto

- Obliga a definir el puerto `AudioAnalyzer` y su contrato antes de implementar cualquier adaptador.
- Hace de la prueba de concepto (hito H2) un requisito previo para cerrar la selección de librería, y obliga a ejecutarla pronto.
- Condiciona el modelo de datos: un resultado de análisis debe identificar motor y versión, y una pista puede tener varios (OD-04).
- Condiciona ADR-007 (licencias) y ADR-009 (conjunto de evaluación).
- Desvía el orden del plan del anteproyecto, que sitúa la prueba de concepto antes de la arquitectura.

## Impacto en la memoria

Guardar este contenido para la memoria del TFG.

- **Capítulo 2, sección 2.3.2:** coherente con las alternativas descritas. No requiere cambios, salvo el estado de Music.py, ya recogido.
- **Capítulo 4, secciones 4.4 y 4.6:** registrar como desviación del plan que las decisiones de arquitectura se aceptaron antes de la prueba de concepto, y que la elección de librería sigue abierta.
- **Capítulo 6, sección 6.4:** diseño del motor de análisis a partir del puerto, los adaptadores y su contrato.
- **Capítulo 8, sección 8.3:** la validación del análisis frente a Rekordbox compara cada motor.
- **Apéndice B, sección B.2:** incluir este ADR.

Bloque reutilizable:

- **Contexto:** el sistema necesita estimar BPM y tonalidad con librerías MIR cuya exactitud, licencia e instalación aún no están contrastadas.
- **Problema:** integrar el análisis sin ligar el sistema a una librería.
- **Alternativas:** acoplamiento directo, puerto con adaptadores sustituibles y motor propio.
- **Solución adoptada:** puerto `AudioAnalyzer` con adaptadores independientes, y selección de librería por prueba de concepto.
- **Justificación:** mayor puntuación (129 frente a 75 y 68) y reducción del riesgo tecnológico.
- **Ventajas:** comparación objetiva de motores, sustitución sin tocar el dominio y trazabilidad de qué motor produjo cada resultado.
- **Limitaciones:** más código de integración y una decisión de librería todavía abierta.
- **Impacto:** exige una prueba de concepto temprana y condiciona el modelo de datos y las licencias.

## Decisiones relacionadas

- ADR-001: Forma de Distribución del Sistema.
- ADR-002: Arquitectura General del Sistema.
- ADR-004: Persistencia.
- ADR-005: Algoritmo de Generación de Setlists.
- ADR-006: Exportación e Integración con Rekordbox.
- ADR-007: Licencias y compatibilidad legal (propuesto).
- ADR-008: Lenguaje, interfaz gráfica y empaquetado (propuesto).
- ADR-009: Dataset y protocolo de evaluación (propuesto).
- ADR-010: Identificación permanente de pistas (propuesto, OD-03).

## Cambios respecto a la versión original (2026-10-28)

| Cambio | Motivo |
|---|---|
| Puerto renombrado a `AudioAnalyzer`; `MetadataReader` añadido | Vocabulario canónico (ADR-002, SRS 7.0) y RF-03 |
| Estado aclarado: arquitectura aceptada, librería condicionada a la prueba de concepto | La elección ya estaba abierta en el texto original |
| Añadidas Mutagen y Music.py y la descarte de esta última como motor | Coherencia con la memoria (sección 2.3.2) |
| Tabla de hipótesis de licencia e instalación | Hallazgo N-04, riesgos R-08 y R-10 |
| Contrato conceptual del puerto y criterios de selección | Hacer verificable la prueba de concepto |
| Soporte multi-motor con motor activo **[PROPUESTA · OD-04]** | H-08 aceptado |
| Derivación de Camelot ubicada en el dominio | RF-06 y regla de dependencia |
| Requisitos, trazabilidad, impactos y decisiones ADR-007 a ADR-010 | Formato obligatorio de ADR |
| Desviación del plan de la prueba de concepto registrada | Hallazgo N-16 |

Las puntuaciones y los totales no se modifican.
