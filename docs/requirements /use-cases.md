# Casos de Uso

## Introducción

Este documento describe los principales casos de uso del sistema de generación automática de setlists para DJs.

Cada caso de uso representa una interacción entre los actores identificados y el sistema, permitiendo definir el comportamiento esperado de la aplicación.

---

# CU-01 Importar Biblioteca Musical

## Objetivo

Permitir al DJ importar una colección de archivos musicales para su posterior análisis.

## Actor Principal

DJ

## Actores Secundarios

- Sistema de Archivos Local

## Precondiciones

- La aplicación está ejecutándose.
- Existe una carpeta con archivos de audio compatibles.

## Flujo Principal

1. El DJ selecciona la opción "Importar Biblioteca".
2. El sistema solicita una carpeta local.
3. El DJ selecciona la carpeta.
4. El sistema localiza todos los archivos compatibles.
5. El sistema registra las pistas encontradas.
6. El sistema muestra un resumen de la importación.

## Flujos Alternativos

### A1: Carpeta vacía

1. El sistema no encuentra archivos compatibles.
2. El sistema muestra un mensaje informativo.

### A2: Acceso denegado

1. No es posible acceder a la carpeta seleccionada.
2. El sistema muestra un error.

## Postcondiciones

- Las pistas quedan registradas para su análisis.

---

# CU-02 Analizar Biblioteca Musical

## Objetivo

Analizar automáticamente las características musicales de las pistas importadas.

## Actor Principal

DJ

## Actores Secundarios

- Motor de Análisis Musical

## Precondiciones

- Existen canciones importadas.

## Flujo Principal

1. El DJ inicia el análisis.
2. El sistema procesa cada pista.
3. Se calcula el BPM.
4. Se detecta la tonalidad.
5. Se calcula la notación Camelot.
6. Se almacenan los resultados.
7. Se muestra el progreso del análisis.

## Flujos Alternativos

### A1: Archivo corrupto

1. El sistema detecta un archivo inválido.
2. El archivo se omite.
3. Se registra la incidencia.

## Postcondiciones

- Todas las pistas válidas disponen de información musical analizada.

---

# CU-03 Configurar Sesión

## Objetivo

Definir los parámetros para la generación del setlist.

## Actor Principal

DJ

## Precondiciones

- La biblioteca ha sido analizada.

## Flujo Principal

1. El DJ accede al configurador.
2. Introduce la duración deseada.
3. Define un rango BPM.
4. Define restricciones armónicas.
5. Establece géneros prioritarios.
6. Guarda la configuración.

## Flujos Alternativos

### A1: Parámetros inválidos

1. El usuario introduce valores incorrectos.
2. El sistema solicita su corrección.

## Postcondiciones

- Los parámetros quedan almacenados para la generación.

---

# CU-04 Generar Setlist

## Objetivo

Crear automáticamente una propuesta de sesión musical.

## Actor Principal

DJ

## Precondiciones

- Existe una biblioteca analizada.
- La sesión ha sido configurada.

## Flujo Principal

1. El DJ solicita generar un setlist.
2. El sistema recupera las pistas disponibles.
3. Evalúa compatibilidad BPM.
4. Evalúa compatibilidad armónica.
5. Calcula las mejores transiciones.
6. Construye la lista ordenada.
7. Presenta el resultado.

## Flujos Alternativos

### A1: No existen suficientes canciones compatibles

1. El sistema identifica incompatibilidades.
2. Genera una propuesta parcial.
3. Notifica la incidencia.

## Postcondiciones

- Se genera un nuevo setlist.

---

# CU-05 Gestionar Canciones Ancla

## Objetivo

Permitir al DJ fijar canciones obligatorias en posiciones concretas.

## Actor Principal

DJ

## Precondiciones

- Existen canciones analizadas.

## Flujo Principal

1. El DJ selecciona una canción.
2. Indica una posición dentro del setlist.
3. El sistema registra la restricción.
4. La canción queda marcada como ancla.

## Flujos Alternativos

### A1: Posición no válida

1. La posición introducida es incorrecta.
2. El sistema muestra un aviso.

## Postcondiciones

- Las canciones ancla se utilizarán durante la generación.

---

# CU-06 Consultar Estadísticas

## Objetivo

Visualizar estadísticas de la biblioteca musical.

## Actor Principal

DJ

## Precondiciones

- Existe información analizada.

## Flujo Principal

1. El DJ accede al panel de estadísticas.
2. El sistema consulta la base de datos.
3. Se generan gráficos y métricas.
4. Se muestran los resultados.

## Información Disponible

- Distribución de BPM.
- Distribución de tonalidades.
- Distribución de géneros.
- Canciones más utilizadas.

## Postcondiciones

- El usuario obtiene información sobre su biblioteca.

---

# CU-07 Exportar Setlist

## Objetivo

Exportar el setlist generado para su uso externo.

## Actor Principal

DJ

## Actores Secundarios

- Rekordbox

## Precondiciones

- Existe un setlist generado.

## Flujo Principal

1. El DJ selecciona la opción Exportar.
2. Elige el formato.
3. El sistema genera el archivo.
4. El sistema guarda el resultado.
5. El usuario recibe confirmación.

## Formatos Disponibles

- Rekordbox
- CSV
- TXT
- M3U

## Flujos Alternativos

### A1: Error de escritura

1. El sistema no puede guardar el archivo.
2. Se muestra un mensaje de error.

## Postcondiciones

- El setlist queda exportado.

---

# CU-08 Consultar Histórico

## Objetivo

Permitir la consulta de sesiones generadas anteriormente.

## Actor Principal

DJ

## Precondiciones

- Existen sesiones almacenadas.

## Flujo Principal

1. El DJ accede al histórico.
2. El sistema recupera los registros.
3. Se muestran las sesiones disponibles.
4. El usuario selecciona una sesión.
5. El sistema muestra el detalle.

## Flujos Alternativos

### A1: Histórico vacío

1. No existen registros previos.
2. El sistema informa al usuario.

## Postcondiciones

- El usuario puede revisar sesiones anteriores.

---

# Resumen de Casos de Uso

| Código | Caso de Uso |
|----------|------------|
| CU-01 | Importar Biblioteca Musical |
| CU-02 | Analizar Biblioteca Musical |
| CU-03 | Configurar Sesión |
| CU-04 | Generar Setlist |
| CU-05 | Gestionar Canciones Ancla |
| CU-06 | Consultar Estadísticas |
| CU-07 | Exportar Setlist |
| CU-08 | Consultar Histórico |
