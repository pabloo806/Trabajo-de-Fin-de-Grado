# ADR-006: Exportación a Rekordbox

## Estado

**Propuesto — Ampliación opcional.** Se implementa únicamente si hay margen de tiempo tras completar el núcleo funcional: análisis de la biblioteca, generación y edición de setlists y guardado en SQLite.

## Fecha

2026-11-20 (reescritura completa tras el replanteamiento del alcance y la verificación directa en Rekordbox).

## Requisitos relacionados

| Requisito | Relación |
|---|---|
| RF-21 | Exportación del setlist en XML compatible con Rekordbox |
| RF-21b | Exportación complementaria en M3U8 |
| RF-22 | Rutas de las pistas resueltas, con aviso explícito si alguna no lo está |
| RF-23 | Verificación manual de que Rekordbox carga la lista con sus pistas resueltas |
| RF-09c | Aviso de pistas ausentes al exportar |
| RF-28 | Exportación de datos del panel (M3U), con relación indirecta |
| RF-29b | Lectura del XML de colección como fuente de referencia (puerto distinto) |
| RNF-16 | Rutas con espacios, tildes, Unicode y rutas largas en ambos sistemas |
| RNF-19 | Windows y macOS |
| RNF-21 | El dominio no depende del formato de rutas del sistema operativo |
| RNF-22, RNF-23 | Exportador accesible mediante un puerto sustituible |
| RNF-25 | El sistema no envía datos fuera del equipo |

Riesgo asociado: R-02 (el fichero exportado no se carga correctamente en Rekordbox). Hallazgos atendidos: N-02 (M3U8 sin requisito) y N-16 (decisiones aceptadas antes de la prueba de concepto).

## Contexto

Uno de los objetivos principales de SetlistGen es integrarse en el flujo de trabajo real de un DJ.

Para ello, los setlists generados deben poder utilizarse posteriormente en Rekordbox, que es la herramienta de referencia utilizada durante la actuación.

El anteproyecto establece que el setlist se exporta en un formato importable por Rekordbox, citando XML o M3U/M3U8.

El sistema no debe:

- Modificar la base de datos interna de Rekordbox.
- Depender de APIs privadas.
- Requerir acceso a Internet.
- Comprometer la portabilidad del sistema.

Por tanto, la integración debe realizarse mediante formatos de intercambio soportados por Rekordbox.

## Problema

Determinar el mecanismo de exportación de setlists para garantizar la integración con Rekordbox.

## Alternativas consideradas

### A1. Copia en carpeta local (`mkdir` + `copy`)

La aplicación crea una carpeta y copia en ella los ficheros de audio del setlist, en orden, a partir de las rutas guardadas en SQLite. El DJ abre la carpeta desde el explorador de Rekordbox sin importar ningún fichero especial.

#### Ventajas

- Resultado autocontenido: no depende de que las pistas permanezcan en su ubicación original.
- Sin formato intermedio ni importación.
- Implementación directa con la biblioteca estándar.
- Útil para llevar el setlist a otro equipo o memoria USB.

#### Inconvenientes

- Ocupa espacio en disco y la copia puede tardar con setlists largos o ficheros WAV y FLAC.
- Duplica ficheros de audio.
- El orden del setlist solo se refleja en el nombre de los ficheros.

---

### A2. Lista `.m3u` / `.m3u8`

Generación de una lista de reproducción estándar en UTF-8 que apunta a las rutas locales almacenadas en SQLite, importable de forma nativa en Rekordbox.

#### Ventajas

- Formato estándar y de texto plano, fácil de generar e inspeccionar.
- Importación nativa en Rekordbox, verificada.
- No copia ni duplica audio.
- Compatible con otros reproductores.

#### Inconvenientes

- Depende de que las rutas sigan siendo válidas en el momento de importar.
- No transporta atributos analíticos (BPM, tonalidad).
- Las rutas con tildes, espacios o diferencias entre Windows y macOS requieren cuidado.

---

### A3. XML de Rekordbox (descartada)

Exportación en el formato XML de colección de Rekordbox.

#### Ventajas

- Estructura rica de listas y metadatos asociados.

#### Inconvenientes

- **Descartada por incompatibilidad funcional:** Rekordbox no admite importar setlists en `.xml`.
- Formato complejo y dependiente de la versión de la aplicación.

---

### A4. Escritura directa en la base de datos interna de Rekordbox (descartada)

#### Ventajas

- Integración aparentemente completa.

#### Inconvenientes

- Estructura propietaria no documentada.
- Riesgo elevado de corromper la biblioteca del DJ y de incompatibilidades entre versiones.
- Fuera del alcance del proyecto.

---

## Criterios de evaluación

| Criterio | Peso |
|---|---:|
| Compatibilidad con Rekordbox | 5 |
| Robustez | 5 |
| Facilidad de implementación | 4 |
| Facilidad de uso para el DJ | 5 |
| Mantenibilidad | 4 |
| Portabilidad | 4 |
| Riesgo tecnológico | 5 |

Suma de pesos: 32. Puntuación máxima posible: 160.

### Escala de valoración

| Valor | Significado |
|---|---|
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

La valoración es **provisional**. En A1 se otorga un 4 en compatibilidad porque la apertura de la carpeta desde el explorador de Rekordbox aún no se ha probado con una biblioteca real.

### A1. Copia en carpeta local

| Criterio | Peso | Valoración | Resultado |
|---|---:|---:|---:|
| Compatibilidad con Rekordbox | 5 | 4 | 20 |
| Robustez | 5 | 4 | 20 |
| Facilidad de implementación | 4 | 5 | 20 |
| Facilidad de uso para el DJ | 5 | 5 | 25 |
| Mantenibilidad | 4 | 5 | 20 |
| Portabilidad | 4 | 5 | 20 |
| Riesgo tecnológico | 5 | 5 | 25 |

**Total: 150**

### A2. Lista `.m3u` / `.m3u8`

| Criterio | Peso | Valoración | Resultado |
|---|---:|---:|---:|
| Compatibilidad con Rekordbox | 5 | 5 | 25 |
| Robustez | 5 | 3 | 15 |
| Facilidad de implementación | 4 | 5 | 20 |
| Facilidad de uso para el DJ | 5 | 4 | 20 |
| Mantenibilidad | 4 | 5 | 20 |
| Portabilidad | 4 | 4 | 16 |
| Riesgo tecnológico | 5 | 4 | 20 |

**Total: 136**

### A3. XML de Rekordbox (descartada)

| Criterio | Peso | Valoración | Resultado |
|---|---:|---:|---:|
| Compatibilidad con Rekordbox | 5 | 1 | 5 |
| Robustez | 5 | 2 | 10 |
| Facilidad de implementación | 4 | 2 | 8 |
| Facilidad de uso para el DJ | 5 | 1 | 5 |
| Mantenibilidad | 4 | 3 | 12 |
| Portabilidad | 4 | 4 | 16 |
| Riesgo tecnológico | 5 | 1 | 5 |

**Total: 61**

### A4. Escritura directa en la base de datos de Rekordbox (descartada)

| Criterio | Peso | Valoración | Resultado |
|---|---:|---:|---:|
| Compatibilidad con Rekordbox | 5 | 2 | 10 |
| Robustez | 5 | 1 | 5 |
| Facilidad de implementación | 4 | 1 | 4 |
| Facilidad de uso para el DJ | 5 | 3 | 15 |
| Mantenibilidad | 4 | 1 | 4 |
| Portabilidad | 4 | 1 | 4 |
| Riesgo tecnológico | 5 | 1 | 5 |

**Total: 47**

### Resumen

| Alternativa | Total | Estado |
|---|---:|---|
| A1. Copia en carpeta local | 150 | Adoptada |
| A2. Lista `.m3u` / `.m3u8` | 136 | Adoptada |
| A3. XML de Rekordbox | 61 | Descartada |
| A4. Escritura en la base de Rekordbox | 47 | Descartada |

La diferencia entre A1 y A2 (150 frente a 136) es moderada y ambas son simples y complementarias, por lo que no se excluyen entre sí.

---

## Comparación funcional

| Característica | A1. Carpeta | A2. `.m3u` / `.m3u8` |
|---|---|---|
| Acceso desde Rekordbox | Abrir la carpeta en el explorador | Importar la lista |
| Duplica ficheros de audio | Sí | No |
| Depende de que las rutas originales sigan existiendo | Solo en el momento de exportar | En el momento de exportar y de importar |
| Orden del setlist | Prefijo numérico en el nombre de fichero | Orden de las líneas |
| Portable a otro equipo | Sí | No (rutas absolutas locales) |
| Espacio en disco | Alto | Despreciable |
| Complejidad de implementación | Baja | Baja |
| Compatibilidad con otros reproductores | Parcial | Muy alta |

## Decisión

1. La exportación queda **fuera del núcleo mínimo viable** y se trata como ampliación opcional.
2. Si se implementa, se adoptan **A1 (copia en carpeta local)** y **A2 (lista `.m3u` / `.m3u8`)** como mecanismos complementarios, ofrecidos a través del puerto opcional `IExportacion`. En implementación se prioriza el que resulte más directo según el margen de tiempo disponible.
3. Se descartan definitivamente **A3 (XML)** y **A4 (escritura en la base de Rekordbox)**.
4. El exportador solo **lee** el setlist y las rutas guardadas. No modifica el setlist ni ningún otro dato de la aplicación.

## Diseño previsto

### Puerto

`IExportacion` pertenece a la capa de aplicación y recibe un setlist ya guardado y un destino elegido por el DJ. Devuelve un informe con las pistas exportadas y las no localizables. La infraestructura aporta dos adaptadores independientes: uno para la copia en carpeta y otro para la lista `.m3u` / `.m3u8`. Ambos viven en `src/setlistgen/infrastructure/export/`.

### Comportamiento común

| Aspecto | Diseño |
|---|---|
| Entrada | Setlist guardado: pistas en orden con su ruta local |
| Verificación previa | Se comprueba en disco que cada ruta existe y es legible antes de escribir nada |
| Rutas rotas o ausentes | Se avisa con la lista de pistas afectadas y el DJ elige entre cancelar y continuar. Si continúa, se exportan las localizables y el informe indica las omitidas |
| Setlist original | No se modifica. La exportación no tiene efectos sobre SQLite |
| Fallos de escritura | Se informa de la causa (permisos, disco lleno, destino inexistente) y no se deja un resultado incompleto sin avisar |

### A1. Adaptador de copia en carpeta local

1. Se crea la carpeta de destino con el nombre del setlist (se pide confirmación si ya existe).
2. Se comprueba que hay espacio libre suficiente estimado a partir del tamaño de los ficheros.
3. Se copian los ficheros en el orden del setlist con un prefijo numérico (`01 - nombre.mp3`, `02 - …`) para que el orden se conserve al listar.
4. Si dos pistas comparten nombre de fichero, el prefijo numérico evita colisiones.
5. La copia conserva el contenido y las fechas del fichero original.

### A2. Adaptador de lista `.m3u` / `.m3u8`

1. El fichero se escribe en **UTF-8**. Es la variante `.m3u8`, necesaria para tildes, espacios y caracteres Unicode.
2. Cada línea es la ruta absoluta de una pista, en el orden del setlist. Opcionalmente se añade la cabecera estándar y, por pista, una línea con la duración y el título.
3. Las rutas se escriben con el separador propio del sistema operativo en el que se ejecuta la aplicación. La conversión es responsabilidad exclusiva del adaptador y no del dominio.
4. Si se ofrece la extensión `.m3u`, se documenta que puede perder caracteres no ASCII. Se recomienda `.m3u8`.

### Pruebas previstas

- Setlist con pistas cuyas rutas contienen espacios, tildes y caracteres Unicode.
- Setlist con una pista movida o eliminada tras guardarlo.
- Destino sin permisos de escritura y disco con espacio insuficiente.
- Importación manual de la lista en Rekordbox y apertura de la carpeta copiada, registrando la versión de Rekordbox usada y el sistema operativo.

## Justificación

Las dos vías aprovechan el hecho de que SQLite ya guarda las rutas locales, de modo que no necesitan nuevos datos ni dependencias. La copia en carpeta es la más robusta, porque el resultado es independiente de las rutas originales. La lista `.m3u8` es la más ligera y la única que Rekordbox importa de forma nativa. Ambas evitan formatos propietarios y cualquier acoplamiento con la base de datos de Rekordbox.

## Consecuencias

### Positivas

- Base de datos ligera: solo rutas y descriptores, sin binarios de audio.
- Cero dependencia de formatos propietarios o complejos.
- Flujo natural para el DJ: abrir una carpeta o importar una lista estándar.
- Coste de implementación bajo para una funcionalidad opcional.
- Nunca se pone en riesgo la biblioteca de Rekordbox del DJ.

### Negativas

- **Rutas rotas:** si el DJ mueve o renombra canciones en disco antes de exportar, las pistas no se localizan. Se mitiga con la verificación previa y el aviso.
- La copia en carpeta duplica ficheros y puede tardar con setlists largos.
- La lista `.m3u8` no transporta BPM ni tonalidad: Rekordbox usa su propio análisis.
- El comportamiento de Rekordbox puede variar entre versiones y solo se comprueba de forma manual.
- Al ser una ampliación, puede quedar sin implementar si el tiempo no alcanza. En ese caso el DJ debe llevar el setlist a mano.

## Evidencias utilizadas

- Verificación directa en Rekordbox: solo se admiten listas `.m3u` y `.m3u8`; no se admite la importación de setlists en `.xml`.
- Decisión de guardar únicamente la ruta local y los descriptores básicos de cada pista en SQLite.
- Estado del arte sobre la integración con Rekordbox y formatos de lista (memoria, capítulos 2 y 3).
- ADR-002: aislamiento de la exportación tras un puerto de la capa de aplicación.
- ADR-004: persistencia en SQLite sin ficheros de audio.

## Impacto en el proyecto

- El componente `Exportación` aparece como opcional en el diagrama de componentes.
- Sus requisitos se marcan con la prioridad más baja en la Fase 2 y no condicionan la entrega del núcleo.
- Elimina del alcance el generador y el lector de XML de Rekordbox, que reducían el esfuerzo disponible para el resto.
- La estructura `src/setlistgen/infrastructure/export/` se mantiene vacía hasta decidir su implementación.

## Impacto en la memoria

Guardar este contenido para la memoria del TFG.

- **Capítulo 4, secciones 4.4 y 4.6:** registrar como desviación justificada que la verificación empírica invalidó el XML como formato principal.
- **Capítulo 6, sección 6.6:** diseño de la exportación opcional a partir de este ADR.
- **Capítulo 7, sección 7.7:** implementación, si se lleva a cabo.
- **Capítulo 8, sección 8.5:** verificación manual con Rekordbox, si se implementa.
- **Apéndice B, sección B.2:** incluir este ADR.

Bloque reutilizable:

- **Contexto:** el setlist debe llegar a Rekordbox partiendo solo de rutas locales almacenadas en SQLite.
- **Problema:** elegir un mecanismo que Rekordbox admita sin tocar su base de datos.
- **Alternativas:** copia en carpeta local, lista `.m3u`/`.m3u8`, XML de Rekordbox y escritura directa en su base de datos.
- **Solución adoptada:** copia en carpeta y lista `.m3u8` como ampliación opcional tras el puerto `IExportacion`.
- **Justificación:** mayor puntuación (150 y 136 frente a 61 y 47) y comprobación empírica de que Rekordbox no importa XML.
- **Ventajas:** base de datos ligera, ausencia de formatos propietarios y flujo natural para el DJ.
- **Limitaciones:** rutas rotas si el DJ mueve los ficheros, duplicación de audio en la copia y dependencia de la versión de Rekordbox.
- **Impacto:** exportación fuera del núcleo mínimo y estructura de `src/` sin carga adicional.

## Decisiones relacionadas

- ADR-002: Arquitectura General del Sistema.
- ADR-004: Persistencia.
- ADR-005: Algoritmo de Generación de Setlists.
