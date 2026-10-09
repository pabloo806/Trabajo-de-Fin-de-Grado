# Trabajo-de-Fin-de-Grado
Sistema automatizado que genera setlists para DJs analizando bibliotecas de audio locales. Extrae BPM y tonalidad mediante Python, creando sesiones armónicas basadas en la Camelot Wheel. Exporta los resultados directamente a Rekordbox. TFG de Ingeniería en Sistemas de Información (UAH).

# 🎛️ AutoSetlist Generator para DJs (TFG)

Este repositorio contiene el código fuente del Trabajo Fin de Grado (TFG) en Ingeniería en Sistemas de Información por la Universidad de Alcalá.

## 📖 Sobre el proyecto
Preparar un setlist adecuado exige horas de revisión manual para encajar tempos (BPM) y tonalidades. Este sistema automatiza la fase de planificación del DJ: partiendo de una carpeta local de audio en bruto (MP3, WAV, FLAC, AIFF), el sistema analiza cada pista, estima sus descriptores musicales y genera un setlist ordenado que respeta las reglas del *harmonic mixing* (Camelot Wheel). El resultado se exporta directamente a formatos compatibles con **Rekordbox** (.xml / .m3u8).

## ✨ Características principales
- **Extracción de Metadatos:** Lectura de etiquetas ID3 y catalogación de la biblioteca local.
- **Análisis de Audio (MIR):** Estimación precisa de BPM y tonalidad usando librerías de Python.
- **Generación Inteligente:** Creación de listas basadas en progresión de BPM y reglas de la rueda Camelot.
- **Integración con Rekordbox:** Exportación directa al ecosistema de Pioneer DJ.

## 🛠️ Stack Tecnológico (Propuesto)
- **Lenguaje:** Python
- **Análisis de Audio:** `librosa` / `Essentia` / `Music.py` (En evaluación)
- **Base de Datos:** SQLite / PostgreSQL

## Estado

Fase 1 - Análisis y requisitos.

## Estructura del proyecto

docs/
backend/
frontend/
database/
tests/

## Gestión

- GitHub Projects
- Microsoft Teams
- Claude Sonnet
