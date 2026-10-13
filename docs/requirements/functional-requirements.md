# Requisitos Funcionales

## Introducción

Los requisitos funcionales describen las funcionalidades que debe proporcionar el sistema de generación automática de setlists para DJs. Cada requisito se identifica mediante un código único para facilitar su trazabilidad durante el desarrollo.

---

## RF-001 Importar biblioteca musical

El sistema deberá permitir seleccionar una carpeta local que contenga archivos de audio para su procesamiento.

## RF-002 Detectar formatos compatibles

El sistema deberá reconocer y procesar los siguientes formatos de audio:

- MP3
- WAV
- FLAC
- AIFF

## RF-003 Extraer metadatos

El sistema deberá extraer automáticamente los metadatos disponibles de cada archivo de audio:

- Título
- Artista
- Álbum
- Género
- Año
- Duración

## RF-004 Analizar BPM

El sistema deberá calcular automáticamente el BPM (Beats Per Minute) de cada pista importada.

## RF-005 Analizar tonalidad

El sistema deberá identificar automáticamente la tonalidad musical de cada pista.

## RF-006 Calcular notación Camelot

El sistema deberá convertir la tonalidad detectada a la notación Camelot para permitir mezclas armónicamente compatibles.

## RF-007 Almacenar información musical

El sistema deberá almacenar toda la información analizada en una base de datos local.

## RF-008 Evitar reanálisis de pistas

El sistema deberá detectar pistas previamente analizadas para evitar procesamientos redundantes.

## RF-009 Crear setlist automáticamente

El sistema deberá generar automáticamente propuestas de setlists a partir de los criterios definidos por el usuario.

## RF-010 Configurar duración objetivo

El usuario deberá poder definir la duración deseada de la sesión.

## RF-011 Configurar rango de BPM

El usuario deberá poder especificar un rango de BPM permitido para la generación del setlist.

## RF-012 Configurar progresión de géneros

El usuario deberá poder establecer una evolución de géneros musicales durante la sesión.

## RF-013 Configurar compatibilidad armónica

El usuario deberá poder definir restricciones de compatibilidad armónica basadas en tonalidad y notación Camelot.

## RF-014 Definir canciones ancla

El usuario deberá poder fijar canciones concretas en posiciones determinadas del setlist.

## RF-015 Validar transiciones

El sistema deberá seleccionar canciones compatibles entre sí considerando:

- BPM
- Tonalidad
- Compatibilidad Camelot

## RF-016 Exportar a Rekordbox

El sistema deberá generar archivos compatibles con Rekordbox para su importación.

## RF-017 Exportar en formato M3U

El sistema deberá permitir exportar setlists en formato M3U.

## RF-018 Exportar en formato CSV

El sistema deberá permitir exportar setlists en formato CSV.

## RF-019 Exportar en formato TXT

El sistema deberá permitir exportar setlists en formato TXT.

## RF-020 Consultar histórico de sesiones

El sistema deberá almacenar los setlists generados para su posterior consulta.

## RF-021 Mostrar estadísticas de BPM

El sistema deberá generar estadísticas relacionadas con la distribución de BPM de la biblioteca musical.

## RF-022 Mostrar estadísticas de tonalidad

El sistema deberá mostrar estadísticas relacionadas con las tonalidades existentes en la biblioteca.

## RF-023 Mostrar estadísticas de géneros

El sistema deberá mostrar estadísticas sobre la distribución de géneros musicales.

## RF-024 Mostrar canciones más utilizadas

El sistema deberá mostrar un ranking de las canciones más utilizadas en setlists generados.

---

## Resumen

Total de requisitos funcionales: **24**
