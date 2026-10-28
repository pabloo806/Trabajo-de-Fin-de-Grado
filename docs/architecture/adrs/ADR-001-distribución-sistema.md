# ADR-001: Forma de Distribución del Sistema

## Estado

Aceptado

## Fecha

2026-10-28

## Contexto

SetlistGen tiene como objetivo asistir al DJ en la preparación de setlists a partir de una biblioteca musical local.

El sistema debe:

- Acceder a carpetas locales con miles de archivos de audio.
- Analizar automáticamente BPM, tonalidad y compatibilidad armónica.
- Mantener una base de datos local con la información procesada.
- Generar setlists parametrizados.
- Exportar resultados compatibles con Rekordbox.
- Funcionar sin depender de servicios externos o almacenamiento en la nube.
- Integrarse de forma natural en el flujo de trabajo habitual de un DJ.

La forma de distribución del sistema condiciona la arquitectura, el acceso a los archivos locales, la persistencia, la interfaz de usuario y la experiencia de uso.

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

La elección concreta del lenguaje de programación, framework de interfaz de usuario y arquitectura de implementación queda pendiente de decisiones posteriores.

## Justificación

La aplicación de escritorio es la alternativa que mejor satisface los requisitos actuales del proyecto.

Permite acceder directamente a bibliotecas musicales locales, facilita la integración con librerías de análisis de audio y mantiene independencia respecto a plataformas y servicios externos.

Además, encaja con el caso de uso previsto, en el que un DJ prepara sesiones desde su propio equipo antes de exportarlas a Rekordbox.

La evaluación multicriterio muestra que esta alternativa obtiene la puntuación total más alta y presenta el mejor equilibrio entre simplicidad, funcionalidad y viabilidad técnica.

## Consecuencias

### Positivas

- Acceso sencillo a bibliotecas musicales locales.
- Funcionamiento completamente offline.
- Integración natural con herramientas de análisis musical.
- Menor complejidad técnica que una solución web o un complemento.
- Independencia respecto a software propietario.
- Mayor facilidad para realizar pruebas de concepto.

### Negativas

- Requiere instalación local.
- Menor accesibilidad remota.
- Necesidad de generar paquetes o binarios para las plataformas soportadas.

## Evidencias utilizadas

- Requisitos funcionales de importación de bibliotecas locales.
- Requisitos funcionales de análisis musical.
- Requisitos funcionales de exportación a Rekordbox.
- Requisitos no funcionales de portabilidad y mantenibilidad.
- Restricción explícita de funcionamiento local sin dependencia de servicios cloud.

## Decisiones relacionadas

- ADR-002: Arquitectura General del Sistema.
- ADR-003: Motor de Análisis Musical.
- ADR-004: Persistencia.
- ADR-005: Algoritmo de Generación de Setlists.
- ADR-006: Exportación e Integración con Rekordbox.
