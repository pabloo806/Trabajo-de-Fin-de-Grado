# Requisitos No Funcionales

## Introducción

Los requisitos no funcionales definen las restricciones, características de calidad y criterios técnicos que debe cumplir el sistema de generación automática de setlists para DJs.

---

# RNF-001 Usabilidad

La interfaz de usuario deberá ser intuitiva y permitir que un usuario con conocimientos básicos de informática pueda utilizar todas las funcionalidades principales sin necesidad de formación específica.

---

# RNF-002 Facilidad de aprendizaje

Un nuevo usuario deberá ser capaz de generar su primer setlist en menos de 10 minutos desde la instalación del sistema.

---

# RNF-003 Tiempo de respuesta

El sistema deberá responder a las acciones de navegación e interacción del usuario en menos de 2 segundos en condiciones normales de funcionamiento.

---

# RNF-004 Rendimiento de análisis

El sistema deberá ser capaz de analizar bibliotecas musicales de al menos 1.000 canciones sin degradaciones críticas del rendimiento.

---

# RNF-005 Escalabilidad

La arquitectura deberá permitir ampliar la capacidad del sistema para soportar bibliotecas musicales de mayor tamaño sin necesidad de rediseño completo.

---

# RNF-006 Disponibilidad

El sistema deberá estar disponible durante toda la sesión de trabajo del usuario sin interrupciones provocadas por errores internos.

---

# RNF-007 Persistencia de datos

Toda la información analizada deberá almacenarse de manera persistente para evitar la pérdida de información entre ejecuciones.

---

# RNF-008 Integridad de los datos

El sistema deberá garantizar la coherencia de la información almacenada en la base de datos evitando duplicidades y registros corruptos.

---

# RNF-009 Fiabilidad

La generación de setlists deberá producir resultados consistentes a partir de los mismos datos y parámetros de entrada.

---

# RNF-010 Seguridad de acceso

El sistema deberá ejecutar únicamente operaciones autorizadas por el usuario sobre los archivos musicales seleccionados.

---

# RNF-011 Privacidad

Toda la información procesada deberá mantenerse localmente en el equipo del usuario sin necesidad de transferir datos a servicios externos.

---

# RNF-012 Compatibilidad multiplataforma

El sistema deberá poder ejecutarse en sistemas operativos Windows, principal plataforma objetivo del proyecto.

---

# RNF-013 Compatibilidad con formatos de audio

El sistema deberá ser compatible con los formatos:

- MP3
- WAV
- FLAC
- AIFF

---

# RNF-014 Compatibilidad con Rekordbox

Los setlists exportados deberán ser compatibles con el proceso de importación de Rekordbox.

---

# RNF-015 Mantenibilidad

La arquitectura deberá seguir principios de modularidad para facilitar futuras ampliaciones y modificaciones.

---

# RNF-016 Reutilización

Los componentes software deberán desarrollarse de forma desacoplada para favorecer su reutilización.

---

# RNF-017 Legibilidad del código

El código fuente deberá seguir estándares de nomenclatura y documentación definidos para el proyecto.

---

# RNF-018 Documentación técnica

El proyecto deberá incluir documentación técnica suficiente para facilitar su mantenimiento y evolución.

---

# RNF-019 Trazabilidad

Todos los requisitos funcionales deberán estar vinculados a casos de uso, componentes de arquitectura e implementaciones correspondientes.

---

# RNF-020 Testabilidad

La arquitectura deberá permitir la realización de pruebas unitarias e integración de forma independiente.

---

# RNF-021 Tecnologías abiertas

Se utilizarán tecnologías de código abierto siempre que sea posible para evitar dependencias de software propietario.

---

# RNF-022 Arquitectura cliente-servidor

La solución deberá implementarse siguiendo una arquitectura basada en frontend, backend y base de datos claramente diferenciados.

---

# RNF-023 API REST

La comunicación entre frontend y backend deberá realizarse mediante una API REST.

---

# RNF-024 Portabilidad

La aplicación deberá poder desplegarse en diferentes entornos sin cambios significativos en el código fuente.

---

# RNF-025 Recuperación ante errores

El sistema deberá registrar los errores producidos durante la ejecución y proporcionar mensajes informativos al usuario.

---

# RNF-026 Eficiencia de almacenamiento

La base de datos deberá evitar duplicidades innecesarias para optimizar el espacio utilizado.

---

# RNF-027 Experiencia de usuario

La interfaz deberá mantener una apariencia uniforme y coherente en todas las pantallas de la aplicación.

---

# RNF-028 Auditoría y registro

El sistema deberá registrar las operaciones relevantes de análisis, generación y exportación para facilitar la supervisión y depuración.

---

# Resumen

Total de requisitos no funcionales: **28**

## Clasificación

| Categoría | Cantidad |
|------------|----------|
| Usabilidad | 2 |
| Rendimiento | 3 |
| Fiabilidad | 3 |
| Seguridad | 2 |
| Compatibilidad | 3 |
| Mantenibilidad | 4 |
| Arquitectura | 4 |
| Calidad | 4 |
| Operación | 3 |

