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
5. Calcula
