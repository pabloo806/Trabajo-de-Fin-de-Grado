# Casos de Uso

## Introducción

Este documento describe los casos de uso del Sistema de Generación Automática de Setlists para DJs.

Cada caso de uso representa una interacción entre los actores identificados y el sistema, permitiendo definir el comportamiento esperado y establecer la trazabilidad con los requisitos funcionales.

---

# CU-01 Importar Biblioteca Musical

## Objetivo

Permitir al usuario seleccionar una carpeta musical para importar las canciones disponibles.

## Actor Principal

DJ

## Actores Secundarios

- Sistema de Archivos Local

## Requisitos Relacionados

- 
- 

## Precondiciones

- La aplicación está ejecutándose.
- El usuario dispone de una carpeta con archivos musicales.

## Flujo Principal

1. El DJ selecciona la opción "Importar Biblioteca".
2. El sistema solicita una carpeta de origen.
3. El DJ selecciona una carpeta.
4. El sistema busca archivos compatibles.
5. El sistema valida los formatos encontrados.
6. El sistema importa la carpeta en el sistema
7. El sistema muestra un resumen de la importación con un botón que permite acceder al proyecto.

## Flujos Alternativos

### A1. No existen archivos compatibles

1. El sistema no encuentra archivos válidos.
2. Se informa al usuario.

### A2. Error de acceso

1. El sistema no puede acceder a la carpeta.
2. Se muestra un mensaje de error.

## Postcondiciones

- 

---

# Diagrama General de Casos de Uso

```mermaid
flowchart TD

```

---

# Resumen

| Código | Caso de Uso |
|----------|------------|
| CU-01 | Importar Biblioteca Musical |
