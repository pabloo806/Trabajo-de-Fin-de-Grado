[ADR-004-persistencia.md](https://github.com/user-attachments/files/34364365/ADR-004-persistencia.md)
# ADR-004: Persistencia

## Estado

Aceptado (revisado el 2026-10-30). La **tecnología** (SQLite) está aceptada. El **esquema** no está cerrado: depende de OD-03 a OD-07 y se define en `data-model.md`.

## Fecha

2026-10-28 (decisión original) · 2026-10-30 (revisión de alineación con la línea base documental)

## Requisitos relacionados

| Requisito | Relación |
|---|---|
| RF-07 | Origen, motor y versión de cada descriptor; varios resultados por pista **[PROPUESTA · OD-04]** |
| RF-08 | Persistencia de pistas y descriptores entre reinicios |
| RF-09, RF-09b, RF-09c | Identificador permanente, detección de pistas nuevas, movidas, duplicadas y ausentes **[PROPUESTA · OD-03]** |
| RF-10 | Setlists, parámetros, semilla e histórico |
| RF-11, RF-11b | Consulta y ordenación de la biblioteca |
| RF-24 a RF-27 | Historial y estadísticas del panel |
| RF-29, RF-29b | Valores de referencia e informes de evaluación |
| RNF-03, RNF-18 | Lectura rápida de las pistas candidatas para la generación |
| RNF-04 | Reconocimiento rápido de pistas ya conocidas (5 000 pistas en ≤ 2 min) |
| RNF-16, RNF-21 | Rutas con Unicode y espacios; el dominio no depende del formato de ruta |
| RNF-17 | Integridad: una interrupción no deja la base de datos inconsistente |
| RNF-19, RNF-20 | Portabilidad e instalación mínima |
| RNF-25 | Datos exclusivamente locales |
| RNF-27 | Migraciones versionadas del esquema |

Hallazgos atendidos: H-08 (multi-motor), H-19 (pistas movidas o ausentes) y H-35 (modelo de dominio completo).

## Contexto

SetlistGen necesita almacenar de forma persistente la información generada durante el análisis y la planificación de sesiones.

La solución debe permitir almacenar:

- Bibliotecas musicales importadas.
- Metadatos de las pistas.
- Ubicaciones de cada pista y su estado (activa, movida, ausente).
- Resultados del análisis musical (BPM, tonalidad y código Camelot), con el motor y la versión que los produjo, y posiblemente de varios motores sobre la misma pista.
- Setlists generados, con sus parámetros y su semilla.
- Historial de generación.
- Valores de referencia de Rekordbox e informes de evaluación.
- Configuración de usuario, incluido el motor de análisis activo.
- Información necesaria para evitar reprocesar pistas ya analizadas.

De acuerdo con ADR-001, SetlistGen se distribuirá como una aplicación de escritorio destinada a un único usuario que trabaja localmente sobre su propia biblioteca musical.

Además, la solución debe:

- Funcionar sin servicios externos.
- Requerir una instalación mínima.
- Mantener una complejidad operativa reducida.
- Ser portable entre Windows y macOS.
- Integrarse fácilmente con Python.
- Permitir consultas eficientes sobre miles de pistas.
- Garantizar la integridad ante interrupciones y permitir la evolución del esquema.

## Problema

Determinar la tecnología de persistencia utilizada por SetlistGen y los principios que debe cumplir el diseño del esquema.

## Alternativas consideradas

### A1. SQLite

Motor de base de datos relacional embebido que almacena toda la información en un único fichero local.

#### Ventajas

- No requiere instalación adicional.
- Integrado en Python mediante el módulo `sqlite3`.
- Excelente portabilidad.
- Administración prácticamente inexistente.
- Rendimiento más que suficiente para el volumen esperado de datos.
- Fácil respaldo mediante copia del fichero de base de datos.
- Amplia documentación.
- Transacciones atómicas, que sustentan RNF-17.

#### Inconvenientes

- Menor capacidad de escalado para escenarios multiusuario.
- Menor capacidad de concurrencia que bases de datos servidor, en particular con un único escritor simultáneo.

---

### A2. PostgreSQL

Sistema gestor de bases de datos relacional cliente-servidor.

#### Ventajas

- Muy potente y escalable.
- Excelente soporte para consultas complejas.
- Amplias capacidades de administración.

#### Inconvenientes

- Requiere instalación y configuración.
- Introduce complejidad operativa innecesaria.
- Dependencia de un servicio en ejecución.
- Sobredimensionado para el alcance del proyecto.
- Incompatible con una instalación mínima y reproducible (RNF-20).

---

### A3. Almacenamiento basado en ficheros

Persistencia mediante JSON, CSV o estructuras similares.

#### Ventajas

- Implementación sencilla.
- Fácil inspección manual.

#### Inconvenientes

- Gestión compleja de relaciones.
- Consultas ineficientes.
- Escalabilidad limitada.
- Mayor riesgo de inconsistencia.
- Más difícil evolucionar el modelo de datos.

---

## Criterios de evaluación

| Criterio | Peso |
|-----------|------:|
| Facilidad de despliegue | 5 |
| Rendimiento | 4 |
| Complejidad operativa | 5 |
| Portabilidad | 5 |
| Escalabilidad | 3 |
| Soporte para consultas | 4 |
| Integración con Python | 5 |
| Mantenibilidad | 4 |

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

### SQLite

| Criterio | Peso | Valoración | Resultado |
|-----------|------:|-----------:|----------:|
| Facilidad de despliegue | 5 | 5 | 25 |
| Rendimiento | 4 | 4 | 16 |
| Complejidad operativa | 5 | 5 | 25 |
| Portabilidad | 5 | 5 | 25 |
| Escalabilidad | 3 | 3 | 9 |
| Soporte para consultas | 4 | 5 | 20 |
| Integración con Python | 5 | 5 | 25 |
| Mantenibilidad | 4 | 5 | 20 |

**Total: 165**

---

### PostgreSQL

| Criterio | Peso | Valoración | Resultado |
|-----------|------:|-----------:|----------:|
| Facilidad de despliegue | 5 | 2 | 10 |
| Rendimiento | 4 | 5 | 20 |
| Complejidad operativa | 5 | 2 | 10 |
| Portabilidad | 5 | 4 | 20 |
| Escalabilidad | 3 | 5 | 15 |
| Soporte para consultas | 4 | 5 | 20 |
| Integración con Python | 5 | 4 | 20 |
| Mantenibilidad | 4 | 4 | 16 |

**Total: 131**

---

### Ficheros JSON / CSV

| Criterio | Peso | Valoración | Resultado |
|-----------|------:|-----------:|----------:|
| Facilidad de despliegue | 5 | 5 | 25 |
| Rendimiento | 4 | 2 | 8 |
| Complejidad operativa | 5 | 4 | 20 |
| Portabilidad | 5 | 5 | 25 |
| Escalabilidad | 3 | 1 | 3 |
| Soporte para consultas | 4 | 1 | 4 |
| Integración con Python | 5 | 5 | 25 |
| Mantenibilidad | 4 | 2 | 8 |

**Total: 118**

Los tres totales se han verificado y no se modifican en esta revisión.

---

## Grupos de datos que debe cubrir la persistencia

La estructura de la versión 1.0 de este ADR guardaba BPM, tonalidad y Camelot directamente en la pista y asociaba las pistas a una biblioteca. Eso es incompatible con varios motores por pista (OD-04), con pistas movidas o ausentes (RF-09c) y con la identidad independiente de la ubicación (RF-09). Se sustituye por una relación de grupos de datos. Los nombres de entidad son los del glosario (sección 6) y **no cierran ninguna decisión abierta**.

| Grupo de datos | Contenido | Requisitos | Dependencia |
|---|---|---|---|
| Pistas | Identidad permanente y estado de la pista | RF-09, RF-09b | OD-03, OD-07 |
| Ubicaciones | Ruta, última vez vista y estado de cada ubicación de una pista | RF-09c, RF-22 | OD-07 |
| Metadatos | Título, artista, género, año y duración | RF-03 | OD-07 |
| Ejecuciones de análisis | Motor, versión y fecha de cada ejecución | RF-07 | OD-04, OD-07 |
| Resultados de análisis | BPM, tónica, modo, Camelot, confianza y estado, por pista y por ejecución | RF-04 a RF-07 | OD-04 |
| Solicitudes de generación | Parámetros, política armónica, salto máximo de BPM y semilla | RF-10, RF-12 a RF-16, RF-13b | OD-07 |
| Segmentos de género y anclas | Progresión de géneros y pistas ancladas de una solicitud | RF-15, RF-16 | OD-07 |
| Setlists y su composición | Orden de las pistas, fecha, estado y marca de editado | RF-10, RF-20b | OD-07 |
| Transiciones | Evaluación de cada transición | RF-17, RF-20 | **OD-06** |
| Referencias de evaluación | Valores de BPM y tonalidad de Rekordbox por pista | RF-29b | OD-07 |
| Informes de evaluación | Métricas por motor | RF-29 | OD-07 |
| Biblioteca | Agrupación de pistas e histórico de importaciones | RF-24 a RF-27 | **OD-05** |
| Configuración | Motor activo y preferencias | RF-07 | OD-04 |
| Versión del esquema | Versión aplicada de las migraciones | RNF-27 | — |

### Supuestos de trabajo

Hasta que tutor y cotutor validen OD-03 a OD-07, el diseño del modelo de datos avanza con estos supuestos explícitos, que pueden cambiar:

| OD | Supuesto de trabajo |
|---|---|
| OD-03 | La identidad permanente de una pista no depende de su ruta; el mecanismo concreto se define en ADR-010 |
| OD-04 | Una pista puede tener varios resultados de análisis, identificados por motor y versión |
| OD-05 | Existe la entidad `Library` |
| OD-06 | Las transiciones se pueden persistir; si el setlist se edita (RF-20b), deben recalcularse |
| OD-07 | Se adoptan las entidades propuestas en `open-decisions.md` |

## Principios para el diseño del esquema

Estos principios forman parte de la decisión y orientan el diseño físico de `data-model.md`.

| Principio | Requisito |
|---|---|
| La clave de una pista es un identificador interno independiente de la ruta y del nombre del fichero | RF-09 |
| Las ubicaciones se almacenan aparte de la pista, con su estado; una ubicación ausente se marca, no se borra | RF-09c |
| Un resultado de análisis identifica siempre el motor y la versión que lo produjo | RF-07 |
| Los datos usados para reconocer una pista ya conocida disponen de índice, para cumplir 5 000 pistas en ≤ 2 min | RNF-04 |
| Las consultas por BPM, tonalidad, género, año y duración, y su ordenación, disponen de índices adecuados y consultan los resultados del motor activo | RF-11, RF-11b |
| Un setlist se guarda con su solicitud de generación, incluida la semilla, para poder reproducirlo | RF-10, RNF-11 |
| Las operaciones de escritura se confirman de forma atómica por pista y por lote; las claves foráneas están activadas | RNF-17 |
| Las rutas se almacenan como texto Unicode; su conversión al formato del sistema operativo o de Rekordbox se hace en infraestructura, no en el dominio | RNF-16, RNF-21 |
| Los cambios de esquema se aplican mediante migraciones versionadas, comprobables sobre una base de datos de versión anterior | RNF-27 |
| La base de datos es un único fichero local y su copia constituye la copia de seguridad | RNF-20, RNF-25 |
| El sistema no accede nunca a la base de datos interna de Rekordbox | SRS 2.5 |

### Concurrencia

SQLite admite un único escritor simultáneo. El análisis por lotes se puede paralelizar entre núcleos (RNF-01, RNF-02), por lo que los adaptadores de análisis calculan resultados en paralelo y un único coordinador los persiste. El análisis no escribe en la base de datos desde varios procesos a la vez.

### Acceso mediante puertos

La persistencia se accede mediante los puertos de repositorio definidos en ADR-002 (`TrackRepository`, `SetlistRepository`, `StatisticsRepository`). El dominio y la aplicación no importan el módulo `sqlite3` (RNF-22).

Las referencias y los informes de evaluación no tienen hoy un puerto de repositorio propio en ADR-002. Se propone `EvaluationRepository` **[PROPUESTA]** y se incorporará en la segunda auditoría de consistencia.

## Decisión

Se adopta **SQLite** como tecnología de persistencia principal del sistema.

El esquema, las claves, los índices y las migraciones se definen en `data-model.md`, siguiendo los principios de este ADR. Hasta que ese documento exista y esté validado, la persistencia se considera **no cerrada**.

## Justificación

SQLite es la solución que mejor se adapta al contexto del proyecto.

El sistema:

- Es una aplicación de escritorio.
- Está orientado a un único usuario.
- Trabaja sobre datos locales.
- No requiere concurrencia elevada.
- Debe ser sencillo de instalar y distribuir.

SQLite permite almacenar toda la información en un único fichero, elimina la necesidad de administrar servicios adicionales y se integra de forma nativa con Python.

La evaluación multicriterio muestra además que es la alternativa con la puntuación total más alta y el mejor equilibrio entre simplicidad, rendimiento y mantenibilidad.

## Consecuencias

### Positivas

- Instalación extremadamente sencilla.
- Sin dependencias externas.
- Integración nativa con Python.
- Excelente portabilidad.
- Copias de seguridad simples.
- Rendimiento suficiente para el volumen previsto.
- Transacciones atómicas que permiten cumplir RNF-17.

### Negativas

- Limitaciones en escenarios multiusuario.
- Menor capacidad de escalado que PostgreSQL.
- Menor capacidad de concurrencia: obliga a centralizar las escrituras del análisis paralelo.
- Los tipos y las restricciones de SQLite son más permisivos que los de otros motores, por lo que parte de la integridad debe garantizarse en el dominio y en las pruebas.
- Un esquema con varios motores, ubicaciones y transiciones es más complejo que el de la versión 1.0 y depende de decisiones aún abiertas.

## Trazabilidad

| Elemento | Referencias |
|---|---|
| Requisitos funcionales | RF-07 a RF-11b, RF-24 a RF-27, RF-29, RF-29b |
| Requisitos no funcionales | RNF-03, RNF-04, RNF-16, RNF-17, RNF-18, RNF-19, RNF-20, RNF-21, RNF-25, RNF-27 |
| Componentes | CMP-03 (base de datos local) y CMP-09 (migraciones) |
| Casos de prueba | T-CU01-05, T-CU02-01, T-CU02-02, T-CU03-01, T-CU06-01, T-RNF-04, T-RNF-17, T-RNF-27 |
| Decisiones abiertas | OD-03, OD-04, OD-05, OD-06, OD-07 |

## Evidencias utilizadas

- ADR-001: Aplicación de escritorio.
- Requisitos de funcionamiento local (RNF-25).
- Requisitos de mantenibilidad y evolución del esquema (RNF-27).
- Requisitos de portabilidad y de instalación mínima (RNF-19, RNF-20).
- Requisitos de persistencia de bibliotecas, resultados, setlists y referencias (RF-08, RF-10, RF-29b).
- Requisitos de integridad y de reanálisis nulo (RNF-17, RNF-04).
- Necesidad de procesar bibliotecas de tamaño medio sin infraestructura adicional.

## Impacto en el proyecto

- Cierra la tecnología de persistencia, pero no el esquema: `data-model.md` es el siguiente entregable y no puede congelarse hasta validar OD-03 a OD-07.
- Obliga a diseñar un mecanismo de migraciones desde el primer esquema (RNF-27).
- Condiciona el análisis por lotes: un único coordinador persiste los resultados.
- Requiere un puerto de repositorio para las referencias y los informes de evaluación.

## Impacto en la memoria

Guardar este contenido para la memoria del TFG.

- **Capítulo 4, sección 4.6:** la tecnología de persistencia deja de figurar como decisión abierta.
- **Capítulo 6, sección 6.3:** modelo de datos, a partir de los grupos de datos y los principios de este ADR.
- **Capítulo 7, sección 7.5:** implementación de la persistencia, migraciones y gestión de concurrencia.
- **Apéndice B, sección B.2:** incluir este ADR.

Bloque reutilizable:

- **Contexto:** una aplicación de escritorio para un único usuario debe guardar pistas, resultados de varios motores, ubicaciones, setlists y evaluaciones sin infraestructura adicional.
- **Problema:** elegir la tecnología de persistencia y los principios del esquema.
- **Alternativas:** SQLite, PostgreSQL y ficheros JSON o CSV.
- **Solución adoptada:** SQLite como única tecnología, accesible mediante puertos de repositorio.
- **Justificación:** mayor puntuación (165 frente a 131 y 118) y encaje con una instalación mínima y portable.
- **Ventajas:** instalación sencilla, transacciones atómicas y copia de seguridad trivial.
- **Limitaciones:** un único escritor simultáneo y un esquema aún dependiente de decisiones abiertas.
- **Impacto:** condiciona el análisis por lotes, las migraciones y el diseño del modelo de datos.

## Decisiones relacionadas

- ADR-001: Forma de Distribución del Sistema.
- ADR-002: Arquitectura General del Sistema.
- ADR-003: Motor de Análisis Musical.
- ADR-005: Algoritmo de Generación de Setlists.
- ADR-006: Exportación e Integración con Rekordbox.
- ADR-007: Licencias y compatibilidad legal (propuesto).
- ADR-008: Lenguaje, interfaz gráfica y empaquetado (propuesto).
- ADR-009: Dataset y protocolo de evaluación (propuesto).
- ADR-010: Identificación permanente de pistas (propuesto, OD-03).

## Cambios respecto a la versión original (2026-10-28)

| Cambio | Motivo |
|---|---|
| El «modelo de datos previsto» de la versión 1.0 se sustituye por grupos de datos y supuestos de trabajo | El esquema original (BPM y tonalidad dentro de la pista, pistas dentro de una biblioteca) era incompatible con OD-03, OD-04, RF-09c y H-08 |
| Principios para el diseño del esquema | Hacer verificables RF-09, RF-09c, RNF-04, RNF-16, RNF-17 y RNF-27 |
| Gestión de la concurrencia del análisis por lotes | SQLite admite un único escritor |
| Estado aclarado: tecnología aceptada, esquema no cerrado | Regla de que la persistencia no se cierra hasta validar `data-model.md` |
| Propuesta de puerto `EvaluationRepository` | Las referencias y los informes no tenían puerto en ADR-002 |
| Requisitos, trazabilidad, impactos y decisiones ADR-007 a ADR-010 | Formato obligatorio de ADR |

Las puntuaciones y los totales no se modifican.
