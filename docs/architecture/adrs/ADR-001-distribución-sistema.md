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

Puntuación ponderada:

```text
Puntuación = Valoración × Peso
