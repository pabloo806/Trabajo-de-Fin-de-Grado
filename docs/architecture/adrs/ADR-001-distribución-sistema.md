# ADR-001: Forma de Distribución del Sistema

## Estado

Aceptado (revisado el 2026-10-30)

## Fecha

2026-10-28 (decisión original) · 2026-10-30 (revisión de alineación con la línea base documental)

## Requisitos relacionados

| Requisito | Relación |
|---|---|
| RF-01 | Acceso directo a carpetas locales con miles de ficheros |
| RF-23 | La importación en Rekordbox la realiza el DJ sobre el fichero exportado |
| RNF-19 | Windows 10/11 y macOS vigente |
| RNF-20 | Instalación reproducible en un tiempo acotado |
| RNF-25 | Procesamiento local: ningún dato sale del equipo del DJ |

Restricciones del SRS v4.0 (sección 2.3) y objetivos O1 a O7 del anteproyecto.

## Contexto

SetlistGen tiene como objetivo asistir al DJ en la preparación de setlists a partir de una biblioteca musical local.

El sistema debe:

- Acceder a carpetas locales con miles de archivos de audio (RF-01).
- Analizar automáticamente BPM, tonalidad y compatibilidad armónica.
- Mantener una base de datos local con la información procesada.
- Generar setlists parametrizados.
- Exportar resultados compatibles con Rekordbox.
- Funcionar sin depender de servicios externos o almacenamiento en la nube (RNF-25).
- Funcionar en Windows y macOS (RNF-19).
- Integrarse de forma natural en el flujo de trabajo habitual de un DJ.

El anteproyecto deja la forma de distribución como decisión abierta de la fase de arquitectura y propone una implementación del análisis en Python. La forma de distribución condiciona la arquitectura, el acceso a los archivos locales, la persistencia, la interfaz de usuario y la experiencia de uso.

## Problema

Determinar cómo se distribuirá y ejecutará SetlistGen.

## Alternativas consideradas

### A1. Aplicación de escritorio

Aplicación instalada localmente en el equipo del usuario.

Ejemplos de implementación:

- Python + Qt
- Java + JavaFX
- C# + WPF
- Electron

#### Ventajas

- Acceso directo al sistema de archivos.
- Integración sencilla con librerías de análisis musical.
- Experiencia de usuario adecuada para una herramienta de uso individual.
- Funcionamiento completamente local.
- Despliegue sencillo para un único usuario.

#### Inconvenientes

- Requiere distribución e instalación.
- Menor accesibilidad remota.

---

### A2. Aplicación web local

Aplicación accesible desde navegador, ejecutándose localmente en el equipo del usuario.

#### Ventajas

- Interfaz moderna.
- Separación clara entre frontend y backend.
- Posibilidad de reutilizar componentes web.

#### Inconvenientes

- Mayor complejidad técnica.
- Gestión más compleja del acceso a archivos locales.
- Infraestructura adicional sin aportar ventajas claras para el alcance actual del proyecto.

---

### A3. Complemento o integración directa con Rekordbox

Extensión ejecutada dentro de Rekordbox o fuertemente acoplada al software.

#### Ventajas

- Integración máxima con el flujo de trabajo del usuario.

#### Inconvenientes

- Dependencia de software propietario.
- Menor control sobre la plataforma.
- Riesgo elevado de incompatibilidades futuras.
- Dificulta la evaluación independiente del sistema.
- Incompatible con la exclusión de escritura directa sobre Rekordbox (SRS 2.5).

---

## Criterios de evaluación

| Criterio | Peso |
|-----------|------:|
| Acceso a archivos locales | 5 |
| Integración con análisis musical | 5 |
| Facilidad de desarrollo | 4 |
| Facilidad de despliegue | 4 |
| Independencia tecnológica | 5 |
| Compatibilidad con los requisitos | 5 |

### Escala de valoración

| Valor | Significado |
|--------|-------------|
| 1 | Muy deficiente |
| 2 | Deficiente |
| 3 | Aceptable |
| 4 | Bueno |
| 5 | Excelente |

### Método de cálculo

Puntuación ponderada:

```text
Puntuación ponderada = Valoración × Peso
```

Puntuación total:

```text
Total = Σ (Valoración × Peso)
```

---

## Evaluación de alternativas

### Aplicación de escritorio

| Criterio | Peso | Valoración | Resultado |
|-----------|------:|-----------:|----------:|
| Acceso a archivos locales | 5 | 5 | 25 |
| Integración con análisis musical | 5 | 5 | 25 |
| Facilidad de desarrollo | 4 | 4 | 16 |
| Facilidad de despliegue | 4 | 4 | 16 |
| Independencia tecnológica | 5 | 5 | 25 |
| Compatibilidad con los requisitos | 5 | 5 | 25 |

**Total: 132**

### Aplicación web local

| Criterio | Peso | Valoración | Resultado |
|-----------|------:|-----------:|----------:|
| Acceso a archivos locales | 5 | 4 | 20 |
| Integración con análisis musical | 5 | 4 | 20 |
| Facilidad de desarrollo | 4 | 3 | 12 |
| Facilidad de despliegue | 4 | 4 | 16 |
| Independencia tecnológica | 5 | 5 | 25 |
| Compatibilidad con los requisitos | 5 | 4 | 20 |

**Total: 113**

### Complemento para Rekordbox

| Criterio | Peso | Valoración | Resultado |
|-----------|------:|-----------:|----------:|
| Acceso a archivos locales | 5 | 2 | 10 |
| Integración con análisis musical | 5 | 2 | 10 |
| Facilidad de desarrollo | 4 | 2 | 8 |
| Facilidad de despliegue | 4 | 3 | 12 |
| Independencia tecnológica | 5 | 1 | 5 |
| Compatibilidad con los requisitos | 5 | 3 | 15 |

**Total: 60**

---

## Decisión

Se adopta una **aplicación de escritorio** como forma de distribución de SetlistGen.

Python es el lenguaje principal del proyecto, de acuerdo con el anteproyecto y el README de arquitectura. Su registro formal, junto con el framework de interfaz de usuario y el sistema de empaquetado, se realizará en ADR-008 (propuesto). Esa decisión posterior no modifica la presente.

## Justificación

La aplicación de escritorio es la alternativa que mejor satisface los requisitos actuales del proyecto.

Permite acceder directamente a bibliotecas musicales locales, facilita la integración con librerías de análisis de audio y mantiene independencia respecto a plataformas y servicios externos.

Además, encaja con el caso de uso previsto, en el que un DJ prepara sesiones desde su propio equipo antes de exportarlas a Rekordbox.

La evaluación multicriterio muestra que esta alternativa obtiene la puntuación total más alta y presenta el mejor equilibrio entre simplicidad, funcionalidad y viabilidad técnica.

## Consecuencias

### Positivas

- Acceso sencillo a bibliotecas musicales locales.
- Funcionamiento completamente offline (RNF-25).
- Integración natural con herramientas de análisis musical.
- Menor complejidad técnica que una solución web o un complemento.
- Independencia respecto a software propietario.
- Mayor facilidad para realizar pruebas de concepto.

### Negativas

- Requiere instalación local.
- Menor accesibilidad remota.
- Necesidad de generar paquetes o binarios para Windows 10/11 y macOS (RNF-19, RNF-20).
- Las librerías de análisis candidatas pueden imponer restricciones de instalación o de licencia en alguna plataforma. Se comprueban en la prueba de concepto (ADR-003, ADR-007).

## Impacto en el proyecto

- Fija la forma de entrega del sistema y descarta una arquitectura cliente-servidor.
- Condiciona ADR-008: el framework de interfaz y el empaquetado deben ser compatibles con una aplicación de escritorio en Windows y macOS.
- Refuerza la persistencia local (ADR-004) y la exclusión de servicios en la nube (RNF-25).
- Obliga a incluir la instalación limpia en ambos sistemas entre las pruebas (RNF-19, RNF-20).

## Impacto en la memoria

Aparece en el capítulo 6 (diseño, sección 6.1 Arquitectura del sistema), en el capítulo 7 (entorno y tecnologías) y en el apéndice B (registro de decisiones). El capítulo 4 (sección 4.6) debe actualizarse: esta decisión ya no figura como abierta.

**Guardar este contenido para la memoria del TFG.**

- **Contexto:** el sistema opera sobre bibliotecas locales de miles de ficheros, sin servicios externos, en Windows y macOS.
- **Problema:** elegir cómo se distribuye y ejecuta.
- **Alternativas:** aplicación de escritorio, aplicación web local y complemento de Rekordbox.
- **Solución adoptada:** aplicación de escritorio.
- **Justificación:** evaluación multicriterio (132, 113 y 60 puntos) y acceso directo a los ficheros.
- **Ventajas:** funcionamiento local, integración con el análisis y despliegue sencillo.
- **Limitaciones:** necesita instalación y empaquetado por plataforma.
- **Impacto:** condiciona el framework de interfaz y el empaquetado.

## Evidencias utilizadas

- RF-01: importación de bibliotecas locales.
- RF-04, RF-05 y RF-06: análisis musical.
- RF-21 a RF-23: exportación a Rekordbox.
- RNF-19, RNF-20 y RNF-25: portabilidad, instalación y procesamiento local.
- Restricción de funcionamiento local sin dependencia de servicios cloud.
- Alternativas de distribución planteadas en el anteproyecto.

## Decisiones relacionadas

- ADR-002: Arquitectura General del Sistema.
- ADR-003: Motor de Análisis Musical.
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
| Añadida la sección «Requisitos relacionados» y IDs en «Evidencias» | Los ADR no citaban requisitos |
| Añadido «Impacto en el proyecto» e «Impacto en la memoria» con bloque reutilizable | Formato obligatorio de ADR |
| La decisión registra Python como lenguaje y remite a ADR-008 para interfaz y empaquetado | El texto original dejaba el lenguaje pendiente, aunque ya estaba aceptado |
| Windows 10/11 y macOS citados en contexto y consecuencias | RNF-19 |
| Añadido un inconveniente de A3 por la exclusión de escritura en Rekordbox | SRS 2.5 |
| Añadidas las decisiones relacionadas ADR-007 a ADR-010 | Nuevos ADR |
| Nombre de fichero sin tilde | El nombre con tilde variaba entre el repositorio y el proyecto |

La decisión, las puntuaciones y los totales no se modifican (se ha verificado que los tres totales son correctos).
