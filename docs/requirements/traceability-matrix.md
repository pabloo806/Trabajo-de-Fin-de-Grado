# Matriz de Trazabilidad

## Introducción

La matriz de trazabilidad permite establecer la relación entre los requisitos funcionales, los casos de uso, los módulos del sistema, las tareas de desarrollo y las futuras pruebas de validación.

Este documento garantiza que todos los requisitos definidos durante la fase de análisis estén cubiertos por la solución propuesta y puedan verificarse mediante pruebas.

---

# Componentes del Sistema

| Código | Componente |
|----------|----------|
| CMP-01 | Módulo de Importación |

---

# Relación Requisitos → Casos de Uso → Componentes

| Requisito | Descripción | Caso de Uso | Componentes |
|------------|------------|------------|-------------|
| RF-001 | Importar biblioteca musical |  |  |

---

# Relación Casos de Uso → Issues GitHub

| Caso de Uso | Issue Principal |
|-------------|----------------|

---

# Relación Requisitos → Casos de Prueba

| Requisito | Test |
|------------|-------|

---

# Cobertura de Requisitos

## Resumen

| Elemento | Cantidad |
|-----------|----------|
| Requisitos Funcionales |  |
| Casos de Uso |  |
| Componentes |  |
| Casos de Prueba |  |

---

# Diagrama General de Trazabilidad

```mermaid
flowchart LR

    RF[Requisitos Funcionales]

    CU[Casos de Uso]

    CMP[Componentes Software]

    DEV[Issues GitHub]

    TEST[Casos de Prueba]

    RF --> CU
    CU --> CMP
    CMP --> DEV
    DEV --> TEST
```

---

# Cobertura por Módulo

```mermaid
graph TD

```

---

# Conclusión

Todos los requisitos funcionales definidos durante la fase de análisis se encuentran trazados hacia:

- Casos de uso asociados.
- Componentes de la arquitectura.
- Issues de desarrollo del proyecto.
- Casos de prueba de validación.

Esta matriz garantiza la cobertura completa de requisitos y facilitará la verificación y validación del sistema durante las fases posteriores del proyecto.
