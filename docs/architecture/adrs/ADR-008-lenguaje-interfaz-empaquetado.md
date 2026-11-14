# ADR-008: Lenguaje, Interfaz Gráfica y Empaquetado

## Estado

**Propuesto.** Pendiente de validación por tutor y cotutor (OD-08), de la verificación de licencias (ADR-007) y de una prueba de concepto de interfaz y empaquetado en Windows y macOS. No cierra ninguna decisión abierta por sí mismo.

## Fecha

2026-10-30

## Requisitos relacionados

| Requisito | Relación |
|---|---|
| RF-11b | Tablas de pistas ordenables por varios campos |
| RF-20, RF-20b | Visualización del setlist con su evaluación de transiciones y reordenación manual |
| RF-24 a RF-27 | Panel con historial, ranking y gráficos (incluida la Rueda Camelot) |
| RNF-13 | Un DJ nuevo genera y exporta su primer setlist en ≤ 10 min |
| RNF-14 | Progreso en operaciones de más de 5 s y mensajes de error con causa y acción |
| RNF-19 | Windows 10/11 y macOS vigente, con los mismos resultados funcionales |
| RNF-20 | Entorno completo desde cero en ≤ 30 min siguiendo el manual, con dependencias fijadas |
| RNF-22 | La interfaz no importa nada de infraestructura ni contiene reglas de negocio |
| RNF-24 | Tipado estático, análisis estático y cobertura |
| RNF-26 | Licencias de las dependencias (interfaz y empaquetado incluidos) |

Hallazgos y asuntos atendidos: OD-08 (ADR-008 potencial), incoherencia entre el stack del `README.md` principal y ADR-001, y estructura de directorios del repositorio.

## Contexto

ADR-001 adopta una aplicación de escritorio y ADR-002 una arquitectura limpia con puertos y adaptadores. Quedan sin decidir formalmente tres aspectos que el SRS (sección 2.3) y la memoria (sección 4.6) mantienen abiertos:

- El lenguaje de programación, que el proyecto ya utiliza como Python pero no está registrado en un ADR.
- La tecnología de interfaz gráfica.
- El empaquetado y la estructura de paquetes del código.

Hay además una incoherencia documental: el `README.md` principal lista FastAPI, React, TypeScript y PostgreSQL como stack, lo que corresponde a una aplicación web cliente-servidor. ADR-001 descartó la aplicación web local (113 puntos frente a 132 de la de escritorio) y ADR-004 adoptó SQLite. Este ADR fija el stack coherente con ambas decisiones.

## Problema

Elegir el lenguaje, el marco de interfaz gráfica, el sistema de empaquetado y la estructura de paquetes que mejor sostengan los requisitos de portabilidad, usabilidad, mantenibilidad y licencias.

## 1. Lenguaje de programación

### Decisión propuesta: Python

Python ya está adoptado en el proyecto. Este apartado lo formaliza y no vuelve a evaluar alternativas con puntuación.

| Motivo | Evidencia |
|---|---|
| Las librerías de análisis musical candidatas son de Python o ofrecen enlaces a Python | ADR-003 |
| Integración nativa con SQLite mediante el módulo `sqlite3` | ADR-004 |
| Pruebas con pytest, tipado estático y análisis estático | RNF-24 |
| Portabilidad entre Windows y macOS | RNF-19 |

Alternativas consideradas y no adoptadas: Java con JavaFX y C# con WPF, que ADR-001 citaba solo como ejemplos. La primera no tiene una integración comparable con las librerías MIR y la segunda no es multiplataforma en su variante de escritorio clásica.

La versión de Python, los tipos y las herramientas de calidad se fijan tras la prueba de concepto, porque dependen de qué versiones soporten las librerías de análisis y de interfaz elegidas. Todas las dependencias se fijan en un fichero de bloqueo (RNF-20).

## 2. Interfaz gráfica

### Alternativas consideradas

#### G1. Qt para Python (PySide6)

Marco de escritorio multiplataforma con tablas, gráficos y arrastrar y soltar.

**Ventajas:** tablas ordenables y modelos de datos para RF-11b; soporte de arrastrar y soltar para RF-20b; escena gráfica para dibujar la Rueda Camelot (RF-26); amplia madurez; soporte de hilos y señales para operaciones largas.

**Inconvenientes:** paquete grande; curva de aprendizaje; condiciones de licencia por verificar (ADR-007).

---

#### G2. Tkinter

Marco de interfaz incluido en la biblioteca estándar de Python.

**Ventajas:** sin dependencias adicionales; licencia permisiva; empaquetado ligero.

**Inconvenientes:** widgets más limitados; apariencia menos uniforme entre sistemas; los gráficos del panel requieren una librería adicional.

---

#### G3. wxPython

Enlace de Python a wxWidgets, con apariencia nativa.

**Ventajas:** apariencia nativa en cada sistema; buena cobertura de widgets.

**Inconvenientes:** menor comunidad que Qt; disponibilidad de instaladores por versión de Python por verificar; menos recursos de aprendizaje.

---

#### G4. Interfaz web embebida con servidor local

Interfaz construida con tecnologías web sobre un servidor local, empaquetada como aplicación de escritorio.

**Ventajas:** gráficos y componentes abundantes.

**Inconvenientes:** dos pilas tecnológicas; empaquetado más complejo; reintroduce la complejidad que ADR-001 descartó en la aplicación web local.

---

### Criterios de evaluación

| Criterio | Peso |
|-----------|------:|
| Licencia y compatibilidad con ADR-007 | 5 |
| Cobertura funcional de la interfaz (RF-11b, RF-20b, RF-26) | 5 |
| Portabilidad en Windows y macOS | 5 |
| Facilidad de empaquetado | 4 |
| Testabilidad y separación de la lógica | 4 |
| Productividad y curva de aprendizaje | 3 |
| Madurez y mantenimiento | 3 |

Escala de valoración: 1 (muy deficiente) a 5 (excelente). Total = Σ (Valoración × Peso).

### Evaluación (inicial y provisional)

| Criterio | Peso | G1 PySide6 | G2 Tkinter | G3 wxPython | G4 Web embebida |
|---|---:|---:|---:|---:|---:|
| Licencia y compatibilidad | 5 | 4 (20) | 5 (25) | 4 (20) | 4 (20) |
| Cobertura funcional | 5 | 5 (25) | 3 (15) | 4 (20) | 5 (25) |
| Portabilidad | 5 | 5 (25) | 4 (20) | 4 (20) | 4 (20) |
| Empaquetado | 4 | 3 (12) | 4 (16) | 3 (12) | 2 (8) |
| Testabilidad | 4 | 4 (16) | 3 (12) | 3 (12) | 3 (12) |
| Productividad | 3 | 3 (9) | 4 (12) | 3 (9) | 2 (6) |
| Madurez | 3 | 5 (15) | 4 (12) | 4 (12) | 5 (15) |
| **Total** | | **122** | **112** | **105** | **106** |

Las valoraciones dependen de hipótesis sobre licencias y empaquetado sin verificar. La diferencia entre G1 y G2 (122 frente a 112) no es concluyente.

### Decisión propuesta: G1 (PySide6)

Sujeta a una prueba de concepto de interfaz que compruebe tres cosas: una tabla ordenable con varios miles de filas (RF-11b), la reordenación por arrastre (RF-20b) y el dibujo de la Rueda Camelot (RF-26). Si la verificación de licencias (ADR-007) descarta G1, se adopta G2 como alternativa.

### Reglas de diseño de la interfaz

- La capa de presentación solo depende de la capa de aplicación (ADR-002, RNF-22).
- La interfaz no contiene reglas de negocio: la compatibilidad armónica, la validación de setlists y la evaluación de transiciones residen en el dominio.
- El análisis, la generación y la exportación se ejecutan fuera del hilo de la interfaz y notifican su progreso (RNF-14).
- Los errores se muestran con su causa y una acción sugerida (RNF-14).
- El patrón de presentación (por ejemplo, presentador o modelo de vista) se fija en el diseño de la interfaz.

## 3. Empaquetado y distribución

### Alternativas consideradas

#### P1. Ejecutable empaquetado con PyInstaller

**Ventajas:** genera ejecutables autónomos; amplia comunidad.

**Inconvenientes:** las dependencias nativas (librerías de análisis, plugins de la interfaz) exigen ajustes; el tamaño es grande; licencia y avisos por verificar (ADR-007).

---

#### P2. Instaladores nativos con Briefcase

**Ventajas:** genera instaladores propios de cada sistema.

**Inconvenientes:** menor cobertura de dependencias nativas complejas; menos documentación para casos como el análisis de audio.

---

#### P3. Compilación con Nuitka

**Ventajas:** puede mejorar el rendimiento y ocultar el código.

**Inconvenientes:** mayor complejidad de mantenimiento; el beneficio no es relevante para este proyecto; condiciones de licencia por verificar.

---

#### P4. Entorno reproducible desde el código fuente

El usuario instala el sistema siguiendo un manual, con un entorno virtual y las dependencias fijadas.

**Ventajas:** compatible con RNF-20, que ya define la instalación desde cero siguiendo el manual; sin redistribución de dependencias, lo que evita obligaciones de licencia (ADR-007); sin esfuerzo de empaquetado.

**Inconvenientes:** exige un paso de instalación por línea de comandos, poco amigable para el DJ; peor valor frente a RNF-13 para un usuario no técnico.

---

### Criterios de evaluación

| Criterio | Peso |
|-----------|------:|
| Portabilidad en Windows y macOS | 5 |
| Facilidad de uso para el DJ | 5 |
| Mantenimiento | 4 |
| Compatibilidad con dependencias nativas | 4 |
| Licencia y compatibilidad con ADR-007 | 4 |
| Reproducibilidad (RNF-20) | 4 |

### Evaluación (inicial y provisional)

| Criterio | Peso | P1 PyInstaller | P2 Briefcase | P3 Nuitka | P4 Desde código fuente |
|---|---:|---:|---:|---:|---:|
| Portabilidad | 5 | 4 (20) | 4 (20) | 4 (20) | 5 (25) |
| Facilidad de uso para el DJ | 5 | 4 (20) | 5 (25) | 4 (20) | 1 (5) |
| Mantenimiento | 4 | 4 (16) | 3 (12) | 2 (8) | 5 (20) |
| Dependencias nativas | 4 | 4 (16) | 3 (12) | 3 (12) | 5 (20) |
| Licencia | 4 | 4 (16) | 5 (20) | 3 (12) | 5 (20) |
| Reproducibilidad | 4 | 4 (16) | 4 (16) | 3 (12) | 4 (16) |
| **Total** | | **104** | **105** | **84** | **106** |

Las cuatro primeras puntuaciones son muy próximas y no permiten una elección concluyente.

### Decisión propuesta: distribución en dos niveles

1. **Obligatorio (P4):** entorno reproducible desde el código fuente, con manual de instalación y dependencias fijadas (RNF-20). Es el nivel que cubre el requisito.
2. **Deseable (P1 o P2):** ejecutable o instalador para el DJ, valorado después de consolidar el núcleo. La elección entre ambos se decide tras una prueba de empaquetado en Windows y macOS que incluya las dependencias nativas, y con los resultados de ADR-007.

Esta decisión no modifica ADR-001, que asume la generación de paquetes «para las plataformas soportadas», pero acota cuándo se hace.

## 4. Estructura de paquetes

### Propuesta

La estructura sigue las capas de ADR-002 y las reglas de dependencia (RNF-22).

```text
src/setlistgen/
├── domain/                 Entidades, objetos de valor y servicios de dominio
├── application/
│   ├── use_cases/          Casos de uso CU-01 a CU-11
│   └── ports/              Puertos (ADR-002)
├── infrastructure/
│   ├── analysis/           Adaptadores de AudioAnalyzer
│   ├── metadata/           Adaptador de MetadataReader
│   ├── scanning/           Adaptador de LibraryScanner
│   ├── identification/     Adaptador de TrackIdentifier (ADR-010)
│   ├── persistence/        Repositorios SQLite y migraciones
│   ├── export/             Exportadores de SetlistExporter
│   └── reference/          Adaptadores de ReferenceDataProvider
├── presentation/           Interfaz gráfica
└── bootstrap/              Composición de dependencias y punto de entrada
tests/                      Reflejan la estructura de src
docs/                       Documentación del proyecto
scripts/                    Utilidades de desarrollo
```

Los adaptadores con dependencias restrictivas (ADR-007) se ubican en un subpaquete opcional dentro de `infrastructure`.

### Discrepancia con la estructura actual del repositorio

El repositorio actual contiene directorios `backend`, `frontend` y `database`, propios de una arquitectura cliente-servidor. Son coherentes con el stack del `README.md` principal, pero no con una aplicación de escritorio con arquitectura limpia (ADR-001 y ADR-002). Se recomienda reorganizarlos al adoptar esta estructura y actualizar el `README.md`.

## Decisión propuesta (resumen)

| Aspecto | Propuesta | Condición |
|---|---|---|
| Lenguaje | Python | Versión por fijar tras la prueba de concepto |
| Interfaz gráfica | PySide6 (alternativa: Tkinter) | Prueba de concepto de interfaz y verificación de licencias |
| Empaquetado | Entorno reproducible desde el código fuente, con ejecutable o instalador como segundo nivel | Prueba de empaquetado en Windows y macOS |
| Estructura de paquetes | Capas de ADR-002 bajo `src/setlistgen` | Validación y reorganización del repositorio |

## Justificación

Python ya sostiene las decisiones de análisis y persistencia. Elegir un marco de interfaz maduro y multiplataforma cubre los requisitos del panel y de la edición de setlists. Posponer el empaquetado a un segundo nivel evita invertir esfuerzo y riesgo de licencias antes de consolidar el núcleo, y es coherente con RNF-20, que ya admite la instalación guiada.

## Consecuencias

### Positivas

- Elimina la incoherencia entre el stack del README y las decisiones aceptadas.
- Una estructura de paquetes que refleja la arquitectura y permite comprobar la regla de dependencia.
- Un camino incremental para el empaquetado.

### Negativas

- La interfaz y el empaquetado dependen de hipótesis de licencia sin verificar.
- Hay que reorganizar el repositorio.
- Si solo se entrega el nivel obligatorio, la usabilidad para un DJ no técnico queda por debajo de lo deseable (RNF-13).
- La prueba de concepto de interfaz y de empaquetado añade trabajo antes de cerrar la decisión.

## Trazabilidad

| Elemento | Referencias |
|---|---|
| Requisitos funcionales | RF-11b, RF-20, RF-20b, RF-24 a RF-27 |
| Requisitos no funcionales | RNF-13, RNF-14, RNF-19, RNF-20, RNF-22, RNF-24, RNF-26 |
| Componentes | CMP-08 (interfaz de usuario) y CMP-09 (infraestructura transversal) |
| Casos de prueba | T-USO-01, T-USO-03, T-ARQ-01, T-ARQ-03, T-ARQ-05, T-ARQ-07, T-ARQ-08, T-CU03-02, T-CU05-10, T-CU08-01, T-CU06-01, T-CU09-01 a T-CU09-03 |
| Decisiones abiertas | OD-08 |

## Evidencias utilizadas

- ADR-001 (aplicación de escritorio), ADR-002 (capas y puertos), ADR-003 y ADR-004 (librerías y persistencia en Python).
- Requisitos de portabilidad, instalación, usabilidad y mantenibilidad.
- Estructura actual del repositorio y stack del `README.md` principal.
- Estado del arte de las librerías de análisis (capítulo 2 de la memoria).

## Impacto en el proyecto

- Obliga a reorganizar el repositorio según la estructura de paquetes y a actualizar el `README.md`.
- Introduce dos pruebas de concepto: interfaz (tabla, arrastre y Rueda Camelot) y empaquetado en Windows y macOS.
- Condiciona ADR-007, que debe verificar la licencia de la interfaz y del empaquetador.
- Fija el nivel mínimo de distribución exigido: entorno reproducible desde el código fuente.

## Impacto en la memoria

Guardar este contenido para la memoria del TFG.

- **Capítulo 4, sección 4.6:** lenguaje, interfaz y estructura de paquetes dejan de figurar como decisiones abiertas cuando se acepte este ADR.
- **Capítulo 6, sección 6.7:** diseño de la interfaz.
- **Capítulo 7, secciones 7.1, 7.2 y 7.8:** entorno y tecnologías, estructura del código e interfaz.
- **Apéndice A:** manual de instalación y de usuario, derivado del nivel obligatorio de distribución.
- **Apéndice B, sección B.2:** incluir este ADR.

Bloque reutilizable:

- **Contexto:** una aplicación de escritorio en Python, con arquitectura limpia, que debe funcionar en Windows y macOS.
- **Problema:** elegir interfaz, empaquetado y estructura de código coherentes con las decisiones previas.
- **Alternativas:** cuatro marcos de interfaz y cuatro sistemas de distribución.
- **Solución propuesta:** Python, PySide6, entorno reproducible como nivel obligatorio y ejecutable como nivel deseable, con estructura de paquetes por capas.
- **Justificación:** mejor puntuación inicial de la interfaz (122) y coherencia con RNF-20, que admite instalación guiada.
- **Ventajas:** cobertura funcional del panel y de la edición, y reducción del riesgo de licencias.
- **Limitaciones:** valoraciones provisionales y usabilidad inferior para un DJ no técnico en el nivel obligatorio.
- **Impacto:** reorganización del repositorio y dos pruebas de concepto.

## Decisiones relacionadas

- ADR-001: Forma de Distribución del Sistema.
- ADR-002: Arquitectura General del Sistema.
- ADR-003: Motor de Análisis Musical.
- ADR-004: Persistencia.
- ADR-006: Exportación e Integración con Rekordbox.
- ADR-007: Licencias y compatibilidad legal (propuesto).
- ADR-009: Dataset y protocolo de evaluación (propuesto).
- ADR-010: Identificación permanente de pistas (propuesto, OD-03).
