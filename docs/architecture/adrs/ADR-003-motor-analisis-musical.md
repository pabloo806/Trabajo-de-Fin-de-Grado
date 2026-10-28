# ADR-003: Motor de Análisis Musical

## Estado

Aceptado

## Fecha

2026-10-28

## Contexto

SetlistGen debe analizar automáticamente pistas de audio para obtener información musical utilizada posteriormente en la generación de setlists.

De acuerdo con los requisitos del sistema, el motor de análisis debe ser capaz de:

- Estimar BPM.
- Estimar tonalidad.
- Derivar el código Camelot.
- Procesar bibliotecas completas de audio.
- Ser sustituible por implementaciones alternativas.
- Permitir comparar diferentes librerías de análisis durante el desarrollo.

Los requisitos no funcionales relacionados con precisión, rendimiento y mantenibilidad hacen recomendable desacoplar el núcleo del sistema de cualquier librería concreta.

## Problema

Determinar cómo integrará SetlistGen el análisis musical.

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

---

## Decisión

SetlistGen utilizará un puerto de análisis musical desacoplado de cualquier librería concreta.

Las implementaciones específicas se proporcionarán mediante adaptadores independientes.

La selección definitiva de la librería de análisis se realizará mediante una prueba de concepto posterior.

## Arquitectura prevista

```text
AnalysisEngine (Puerto)
│
├── LibrosaAdapter
├── EssentiaAdapter
├── MadmomAdapter
└── Otros adaptadores futuros
```

La capa de aplicación y el dominio dependerán exclusivamente de la interfaz `AnalysisEngine`.

## Justificación

Esta estrategia permite:

- Comparar tecnologías de análisis durante el desarrollo.
- Sustituir una librería sin modificar la lógica de negocio.
- Realizar pruebas de concepto objetivas.
- Cumplir los requisitos de mantenibilidad y sustituibilidad.

Además, encaja con la arquitectura definida en ADR-002.

## Consecuencias

### Positivas

- Independencia tecnológica.
- Mayor facilidad para pruebas.
- Comparación objetiva de librerías.
- Evolución sencilla del sistema.

### Negativas

- Mayor complejidad de diseño.
- Necesidad de desarrollar adaptadores.
- Incremento moderado del esfuerzo inicial.

## Evidencias utilizadas

- Requisitos de estimación de BPM.
- Requisitos de estimación de tonalidad.
- Requisitos de mantenibilidad.
- Requisitos de sustituibilidad.
- Necesidad de realizar una prueba de concepto tecnológica.

## Decisiones relacionadas

- ADR-001: Forma de Distribución del Sistema.
- ADR-002: Arquitectura General del Sistema.
- ADR-004: Persistencia.
- ADR-005: Algoritmo de Generación de Setlists.
- ADR-006: Exportación e Integración con Rekordbox.
