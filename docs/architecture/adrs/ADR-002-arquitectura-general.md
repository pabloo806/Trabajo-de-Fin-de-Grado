# ADR-002: Arquitectura General del Sistema

## Estado

Aceptado

## Fecha

2026-10-28

## Contexto

SetlistGen se distribuirá como una aplicación de escritorio que debe:

- Importar bibliotecas musicales locales.
- Analizar archivos de audio mediante librerías especializadas.
- Almacenar resultados de análisis y setlists.
- Generar secuencias de reproducción bajo restricciones.
- Exportar resultados compatibles con Rekordbox.
- Mantener independencia respecto a librerías concretas de análisis, persistencia o exportación.

Los requisitos no funcionales exigen mantenibilidad, facilidad de pruebas y capacidad de sustituir componentes tecnológicos sin afectar a la lógica de negocio.

## Problema

Determinar la arquitectura de software que permita desacoplar la lógica del dominio de las tecnologías concretas utilizadas para:

- Interfaz de usuario.
- Persistencia.
- Análisis musical.
- Exportación.

## Alternativas consideradas

### A1. Arquitectura en capas tradicional

Capas organizadas de forma jerárquica:

- Presentación
- Negocio
- Persistencia

#### Ventajas

- Fácil de comprender.
- Amplia documentación.
- Baja complejidad inicial.

#### Inconvenientes

- Dependencia fuerte de la persistencia.
- Dificulta sustituir adaptadores.
- Menor facilidad para pruebas aisladas.

---

### A2. Arquitectura Limpia (Clean Architecture)

Organización basada en:

- Dominio
- Casos de uso
- Puertos
- Adaptadores
- Interfaz

#### Ventajas

- Independencia tecnológica.
- Alta mantenibilidad.
- Alta testabilidad.
- Facilita sustituir motores MIR, bases de datos y exportadores.
- Encaja con la naturaleza experimental del proyecto.

#### Inconvenientes

- Mayor complejidad inicial.
- Más clases e interfaces.

---

### A3. Arquitectura Hexagonal

Modelo basado en puertos y adaptadores.

#### Ventajas

- Muy desacoplada.
- Excelente para pruebas.

#### Inconvenientes

- Mayor esfuerzo de diseño.
- Diferencias conceptuales reducidas respecto a Clean Architecture para este proyecto.

---

### A4. Monolito sin separación formal

Organización libre del código.

#### Ventajas

- Desarrollo inicial rápido.

#### Inconvenientes

- Alto acoplamiento.
- Baja mantenibilidad.
- Difícil evolución.

---

## Criterios de evaluación

| Criterio | Peso |
|-----------|------:|
| Separación de responsabilidades | 5 |
| Testabilidad | 5 |
| Mantenibilidad | 5 |
| Independencia tecnológica | 5 |
| Escalabilidad | 3 |
| Complejidad de implementación | 2 |

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

### Arquitectura en capas

| Criterio | Peso | Valoración | Resultado |
|-----------|------:|-----------:|----------:|
| Separación | 5 | 3 | 15 |
| Testabilidad | 5 | 3 | 15 |
| Mantenibilidad | 5 | 3 | 15 |
| Independencia tecnológica | 5 | 2 | 10 |
| Escalabilidad | 3 | 3 | 9 |
| Complejidad | 2 | 5 | 10 |

**Total: 74**

### Clean Architecture

| Criterio | Peso | Valoración | Resultado |
|-----------|------:|-----------:|----------:|
| Separación | 5 | 5 | 25 |
| Testabilidad | 5 | 5 | 25 |
| Mantenibilidad | 5 | 5 | 25 |
| Independencia tecnológica | 5 | 5 | 25 |
| Escalabilidad | 3 | 4 | 12 |
| Complejidad | 2 | 3 | 6 |

**Total: 118**

### Arquitectura Hexagonal

| Criterio | Peso | Valoración | Resultado |
|-----------|------:|-----------:|----------:|
| Separación | 5 | 5 | 25 |
| Testabilidad | 5 | 5 | 25 |
| Mantenibilidad | 5 | 4 | 20 |
| Independencia tecnológica | 5 | 5 | 25 |
| Escalabilidad | 3 | 4 | 12 |
| Complejidad | 2 | 2 | 4 |

**Total: 111**

### Monolito tradicional

| Criterio | Peso | Valoración | Resultado |
|-----------|------:|-----------:|----------:|
| Separación | 5 | 1 | 5 |
| Testabilidad | 5 | 1 | 5 |
| Mantenibilidad | 5 | 1 | 5 |
| Independencia tecnológica | 5 | 1 | 5 |
| Escalabilidad | 3 | 2 | 6 |
| Complejidad | 2 | 5 | 10 |

**Total: 36**

---

## Decisión

Se adopta una arquitectura basada en los principios de **Clean Architecture**.

## Justificación

La solución permite separar de forma clara:

- La lógica de negocio.
- Los casos de uso.
- La persistencia.
- El análisis musical.
- La exportación.
- La interfaz de usuario.

Esta decisión facilita sustituir tecnologías concretas sin modificar las reglas de negocio del sistema.

Resulta especialmente adecuada para un proyecto en el que varias decisiones técnicas siguen abiertas y deberán validarse mediante pruebas de concepto.

## Arquitectura prevista

```text
UI
│
├── Interfaz de usuario
│
Application
│
├── Casos de uso
│
Domain
│
├── Track
├── Library
├── Setlist
├── AnalysisResult
└── CamelotKey
│
Ports
│
├── AnalysisEngine
├── TrackRepository
├── SetlistRepository
└── Exporter
│
Adapters
│
├── LibrosaAdapter
├── EssentiaAdapter
├── SQLiteAdapter
├── PostgreSQLAdapter
└── RekordboxExporter
```

## Consecuencias

### Positivas

- Alta mantenibilidad.
- Alta testabilidad.
- Independencia tecnológica.
- Sustitución sencilla de componentes.
- Evolución controlada del sistema.

### Negativas

- Mayor complejidad inicial.
- Mayor número de clases e interfaces.
- Necesidad de definir contratos explícitos entre capas.

## Evidencias utilizadas

- Requisitos de mantenibilidad.
- Requisitos de sustituibilidad.
- Necesidad de evaluar distintas librerías MIR.
- Necesidad de mantener abiertas decisiones tecnológicas posteriores.

## Decisiones relacionadas

- ADR-001: Forma de Distribución del Sistema.
- ADR-003: Motor de Análisis Musical.
- ADR-004: Persistencia.
- ADR-005: Algoritmo de Generación de Setlists.
- ADR-006: Exportación e Integración con Rekordbox.
