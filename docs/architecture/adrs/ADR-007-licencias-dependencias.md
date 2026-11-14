# ADR-007: Licencias y Compatibilidad Legal de Dependencias

## Estado

**Propuesto.** Pendiente de validación por tutor y cotutor (OD-08) y de la verificación del inventario de licencias durante la prueba de concepto. No cierra ninguna decisión abierta por sí mismo.

## Fecha

2026-10-30

## Requisitos relacionados

| Requisito | Relación |
|---|---|
| RNF-26 | Inventario de licencias de las dependencias y compatibilidad con la licencia del repositorio. Verificación indicada en el SRS: este ADR |
| RNF-25 | Procesamiento local: el audio del DJ no sale del equipo |
| RNF-19, RNF-20 | Distribución e instalación en Windows y macOS |
| RNF-22, RNF-23 | Dependencias externas tras puertos sustituibles |
| RF-03, RF-04, RF-05 | Librerías de etiquetas y de análisis candidatas |
| RF-29, RF-29b | Uso de datos de referencia procedentes de Rekordbox |

Riesgo asociado: R-08 (licencias de las dependencias incompatibles con la del repositorio). Hallazgo asociado: N-04 y N-05 (inconsistencia entre la licencia del repositorio y el texto del README).

## Contexto

SetlistGen es una aplicación de escritorio (ADR-001) que se apoyará en librerías de terceros para analizar audio, leer etiquetas, persistir datos y construir la interfaz.

El repositorio es público y contiene un fichero `LICENSE` con la **licencia MIT**. En cambio, el `README.md` principal declara que el proyecto se desarrolla «con fines exclusivamente académicos», lo que no coincide con una licencia que permite uso comercial.

Los ADR anteriores trasladan a este ADR varias cuestiones de licencia:

- ADR-001: la distribución de binarios activa las obligaciones de licencia de lo que se empaquete.
- ADR-003: las librerías de análisis candidatas pueden tener licencias con restricciones.
- ADR-008 (propuesto): la interfaz gráfica y el empaquetado añadirán dependencias.

Además existen dos cuestiones legales no relacionadas con las dependencias de software, que el apéndice C de la memoria exige tratar:

- **Propiedad intelectual del audio.** La biblioteca de pruebas es la del autor y se compone de obras con derechos de terceros.
- **Protección de datos en la validación.** La valoración por DJs (RNF-12) recoge opiniones de personas.

## Problema

Definir una política de licencias que permita:

1. Mantener la licencia del repositorio sin incoherencias.
2. Decidir qué dependencias se pueden adoptar y en qué condiciones.
3. Distribuir el sistema sin incumplir obligaciones de las dependencias empaquetadas.
4. Tratar el audio y los datos de validación sin infringir derechos.

## Hipótesis de partida sobre las dependencias candidatas

Las afirmaciones de esta tabla proceden de conocimiento general del autor y **no están verificadas**. Cada fila debe comprobarse leyendo la licencia vigente del proyecto, en la versión que se pretenda usar, antes de aceptar este ADR.

| Dependencia | Uso previsto | Licencia (hipótesis, por verificar) | Cuestión a comprobar | Requisitos |
|---|---|---|---|---|
| Essentia | Análisis de BPM y tonalidad (ADR-003) | Copyleft fuerte, con modalidad comercial aparte | Compatibilidad con un repositorio MIT y con la distribución de binarios | RNF-26, RNF-19 |
| Librosa | Análisis y preprocesado (ADR-003) | Permisiva | Dependencias de decodificación de audio | RNF-26, RNF-20 |
| Madmom | Beat tracking (ADR-003) | Código permisivo; modelos entrenados con posible restricción de uso no comercial | Licencia de los modelos | RNF-26 |
| Mutagen | Lectura de etiquetas (ADR-003) | Copyleft | Compatibilidad con un repositorio MIT; alternativas permisivas | RNF-26 |
| SQLite (`sqlite3`) | Persistencia (ADR-004) | Dominio público | Ninguna relevante | — |
| Marco de interfaz gráfica | Presentación (ADR-008) | Según la opción elegida, permisiva o copyleft | Depende de ADR-008 | RNF-26 |
| Herramientas de desarrollo (pytest, análisis estático) | Pruebas y CI | Permisivas | No se distribuyen con el sistema | — |

Si alguna hipótesis resulta errónea, la valoración de las alternativas se recalcula. La sustituibilidad de las dependencias (ADR-002, ADR-003) reduce el coste de cambiar de librería.

## Alternativas consideradas

### A1. Repositorio MIT con dependencias exclusivamente permisivas

El repositorio mantiene su licencia MIT y solo se aceptan dependencias con licencias permisivas.

#### Ventajas

- Máxima claridad legal.
- Distribución de binarios sin obligaciones de copyleft.
- Código reutilizable por terceros sin restricciones adicionales.

#### Inconvenientes

- Puede excluir librerías de análisis de mayor cobertura o exactitud (por ejemplo, si Essentia resultara incompatible).
- Reduce las opciones de comparación experimental (RF-29).

---

### A2. Repositorio MIT con núcleo permisivo y adaptadores opcionales con dependencias restrictivas

El núcleo del sistema solo usa dependencias permisivas. Una dependencia con copyleft o con restricciones de uso solo se admite dentro de un adaptador **opcional**, que el usuario instala por separado y que **no se redistribuye** con la distribución por defecto.

#### Ventajas

- Mantiene la licencia MIT del repositorio.
- Permite evaluar librerías restrictivas en la prueba de concepto y en la validación experimental.
- Aprovecha los puertos y adaptadores ya decididos (ADR-002, ADR-003).
- El binario por defecto queda libre de obligaciones de copyleft.

#### Inconvenientes

- Si la mejor librería es restrictiva, la distribución por defecto no la incluye y puede ofrecer menor exactitud.
- Exige distinguir con claridad en la documentación qué adaptadores forman parte de la distribución.
- Hay que comprobar que el uso por separado no incumple la licencia en cada caso.

---

### A3. Repositorio con licencia copyleft

Cambiar la licencia del repositorio a una licencia copyleft compatible con las dependencias elegidas.

#### Ventajas

- Compatible con las librerías de análisis de mayor cobertura.
- Evita conflictos de licencia con dependencias copyleft.

#### Inconvenientes

- Obliga a cambiar la licencia ya publicada.
- Impone restricciones a quien reutilice el código.
- Aumenta el coste de cumplimiento y el riesgo legal.

---

### A4. Mantener el estado actual sin política

Conservar la licencia MIT y adoptar dependencias sin criterio explícito.

#### Ventajas

- Ningún esfuerzo adicional.

#### Inconvenientes

- Riesgo legal alto al distribuir binarios.
- Incumple RNF-26, que exige un inventario y una comprobación de compatibilidad.
- Mantiene la incoherencia entre `LICENSE` y `README.md`.

---

## Criterios de evaluación

| Criterio | Peso |
|-----------|------:|
| Compatibilidad con las librerías candidatas | 5 |
| Claridad y bajo riesgo legal | 5 |
| Facilidad de distribución de binarios | 4 |
| Libertad de reutilización del código | 3 |
| Coste de cumplimiento | 3 |
| Sustituibilidad de dependencias | 4 |

### Escala de valoración

| Valor | Significado |
|--------|-------------|
| 1 | Muy deficiente |
| 2 | Deficiente |
| 3 | Aceptable |
| 4 | Bueno |
| 5 | Excelente |

### Método de cálculo

```text
Puntuación ponderada = Valoración × Peso
Total = Σ (Valoración × Peso)
```

---

## Evaluación de alternativas

La valoración es **inicial y provisional**: depende de las hipótesis de la tabla anterior y se recalcula cuando se verifiquen.

### A1. MIT con dependencias permisivas

| Criterio | Peso | Valoración | Resultado |
|-----------|------:|-----------:|----------:|
| Compatibilidad con las librerías candidatas | 5 | 2 | 10 |
| Claridad y bajo riesgo legal | 5 | 5 | 25 |
| Facilidad de distribución de binarios | 4 | 5 | 20 |
| Libertad de reutilización del código | 3 | 5 | 15 |
| Coste de cumplimiento | 3 | 4 | 12 |
| Sustituibilidad de dependencias | 4 | 4 | 16 |

**Total: 98**

### A2. MIT con núcleo permisivo y adaptadores opcionales

| Criterio | Peso | Valoración | Resultado |
|-----------|------:|-----------:|----------:|
| Compatibilidad con las librerías candidatas | 5 | 5 | 25 |
| Claridad y bajo riesgo legal | 5 | 4 | 20 |
| Facilidad de distribución de binarios | 4 | 4 | 16 |
| Libertad de reutilización del código | 3 | 5 | 15 |
| Coste de cumplimiento | 3 | 3 | 9 |
| Sustituibilidad de dependencias | 4 | 5 | 20 |

**Total: 105**

### A3. Repositorio con licencia copyleft

| Criterio | Peso | Valoración | Resultado |
|-----------|------:|-----------:|----------:|
| Compatibilidad con las librerías candidatas | 5 | 5 | 25 |
| Claridad y bajo riesgo legal | 5 | 3 | 15 |
| Facilidad de distribución de binarios | 4 | 3 | 12 |
| Libertad de reutilización del código | 3 | 2 | 6 |
| Coste de cumplimiento | 3 | 2 | 6 |
| Sustituibilidad de dependencias | 4 | 3 | 12 |

**Total: 76**

### A4. Estado actual sin política

| Criterio | Peso | Valoración | Resultado |
|-----------|------:|-----------:|----------:|
| Compatibilidad con las librerías candidatas | 5 | 3 | 15 |
| Claridad y bajo riesgo legal | 5 | 1 | 5 |
| Facilidad de distribución de binarios | 4 | 2 | 8 |
| Libertad de reutilización del código | 3 | 5 | 15 |
| Coste de cumplimiento | 3 | 5 | 15 |
| Sustituibilidad de dependencias | 4 | 2 | 8 |

**Total: 66**

La diferencia entre A2 y A1 (105 frente a 98) es reducida. Si la prueba de concepto demuestra que una librería permisiva alcanza la exactitud requerida (RNF-05 a RNF-08), A1 pasa a ser la opción más sencilla.

---

## Decisión propuesta

Se propone adoptar la alternativa **A2**, con una política de clasificación de dependencias y un inventario verificable.

### Política de clasificación

| Clase | Ejemplos de licencia | Regla propuesta |
|---|---|---|
| Permisiva | MIT, BSD, ISC, Apache-2.0, PSF, dominio público | Permitida en el núcleo y en los adaptadores |
| Copyleft débil | LGPL, MPL | Permitida si es sustituible y se cumplen sus avisos; se revisa caso a caso |
| Copyleft fuerte | GPL, AGPL | Prohibida en el núcleo. Solo en adaptadores opcionales no redistribuidos con la distribución por defecto |
| Uso restringido | Licencias no comerciales o modelos entrenados con restricciones | Solo en adaptadores opcionales, con aviso explícito |
| Desconocida o sin licencia | — | Prohibida |

### Medidas asociadas

1. **Inventario.** Un fichero versionado con cada dependencia, su versión, su licencia, su clase y su uso (RNF-26).
2. **Avisos de terceros.** Un fichero de avisos generado a partir del inventario y distribuido con los binarios.
3. **Verificación automática.** Comprobación en integración continua de que ninguna dependencia del núcleo pertenece a una clase prohibida (RNF-26).
4. **Coherencia del repositorio.** El `README.md` debe declarar la licencia MIT y dejar de describir el proyecto como de uso exclusivamente académico, o la licencia debe cambiarse. La opción elegida la decide el autor.
5. **Audio.** El repositorio no contiene ficheros de audio. Para el conjunto de evaluación (ADR-009) solo se publican datos derivados (identificadores, BPM, tonalidad y, en su caso, huellas), nunca las obras.
6. **Datos de validación.** La valoración por DJs es anónima, con consentimiento informado y sin recogida de datos personales (RNF-12).
7. **Rekordbox.** El sistema solo utiliza formatos de intercambio documentados (XML y M3U8) y no realiza ingeniería inversa del software ni de su base de datos. «Rekordbox» es una marca de su titular y se menciona únicamente para identificar la compatibilidad.

### Condiciones para pasar a «Aceptado»

- Inventario de licencias verificado contra las licencias vigentes, con las versiones elegidas.
- Resultado de la prueba de concepto de ADR-003.
- Validación de tutor y cotutor (OD-08).
- Revisión de la normativa de la universidad sobre propiedad intelectual y licencias de los TFG, que no se ha contrastado en esta revisión.

## Justificación

A2 es la alternativa que permite mantener la licencia ya publicada, evaluar libremente las librerías de análisis y distribuir un binario sin obligaciones de copyleft, apoyándose en la sustituibilidad ya decidida en ADR-002 y ADR-003.

La política evita decidir a priori una librería y traslada la decisión de licencia a los datos de la prueba de concepto.

## Consecuencias

### Positivas

- Cumple RNF-26 con un procedimiento verificable.
- Mantiene la licencia MIT sin cambios.
- No condiciona la selección de la librería de análisis (ADR-003).
- Reduce el riesgo R-08.
- Documenta el tratamiento legal del audio y de los datos para el apéndice C de la memoria.

### Negativas

- Si la mejor librería es restrictiva, la distribución por defecto puede no incluirla y ofrecer menor exactitud.
- Mantener un inventario y una verificación automática añade trabajo continuo.
- Se pueden necesitar dos configuraciones de empaquetado (con y sin adaptadores opcionales), lo que afecta a ADR-008.
- La valoración depende de hipótesis aún sin verificar.

## Trazabilidad

| Elemento | Referencias |
|---|---|
| Requisitos no funcionales | RNF-19, RNF-20, RNF-22, RNF-23, RNF-25, RNF-26 |
| Componentes | CMP-09 (infraestructura transversal), CMP-02 (adaptadores de análisis) |
| Casos de prueba | T-ARQ-05 (inventario de licencias), T-ARQ-03 (comprobaciones en integración continua), T-ARQ-01, T-ARQ-02, T-ARQ-04, T-ARQ-07, T-ARQ-08 |
| Decisiones abiertas | OD-08 |
| Riesgos | R-08 |

## Evidencias utilizadas

- Requisito RNF-26 y su verificación asociada a este ADR.
- Riesgo R-08 del capítulo 4 de la memoria.
- Fichero `LICENSE` del repositorio (MIT) y texto del `README.md`.
- Consecuencias de distribución de binarios señaladas en ADR-001.
- Limitaciones de las librerías señaladas en ADR-003.
- Estructura del apéndice C de la memoria (licencias, propiedad intelectual del audio y protección de datos).

## Impacto en el proyecto

- Condiciona la selección de la librería de análisis y la configuración de empaquetado (ADR-008).
- Introduce un inventario de licencias y una comprobación en integración continua.
- Obliga a alinear el `README.md` con la licencia del repositorio.
- Fija que el conjunto de evaluación se publica sin audio.

## Impacto en la memoria

Guardar este contenido para la memoria del TFG.

- **Capítulo 4, sección 4.5:** riesgo R-08 y su mitigación.
- **Capítulo 4, sección 4.6:** esta decisión permanece abierta hasta su validación.
- **Apéndice C:** C.1 (licencias de las dependencias), C.2 (propiedad intelectual del audio) y C.3 (protección de datos en la validación).
- **Apéndice B, sección B.2:** incluir este ADR.

Bloque reutilizable:

- **Contexto:** un repositorio público con licencia MIT que se apoya en librerías de terceros y distribuirá binarios.
- **Problema:** definir qué dependencias se pueden adoptar y cómo cumplir sus licencias.
- **Alternativas:** núcleo permisivo, núcleo permisivo con adaptadores opcionales restrictivos, repositorio copyleft y sin política.
- **Solución propuesta:** núcleo permisivo con adaptadores opcionales para dependencias restrictivas.
- **Justificación:** mejor puntuación inicial (105 frente a 98, 76 y 66) y aprovechamiento de la sustituibilidad por puertos.
- **Ventajas:** mantiene la licencia, permite evaluar cualquier librería y simplifica la distribución.
- **Limitaciones:** la distribución por defecto puede quedar sin la mejor librería y la valoración depende de hipótesis por verificar.
- **Impacto:** exige un inventario verificado, comprobaciones automáticas y alinear la documentación del repositorio.

## Decisiones relacionadas

- ADR-001: Forma de Distribución del Sistema.
- ADR-002: Arquitectura General del Sistema.
- ADR-003: Motor de Análisis Musical.
- ADR-004: Persistencia.
- ADR-006: Exportación e Integración con Rekordbox.
- ADR-008: Lenguaje, interfaz gráfica y empaquetado (propuesto).
- ADR-009: Dataset y protocolo de evaluación (propuesto).
- ADR-010: Identificación permanente de pistas (propuesto, OD-03).
