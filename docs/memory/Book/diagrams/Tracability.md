```mermaid
flowchart LR

    OBJ([Objetivos])

    RF([Requisitos<br/>Funcionales])

    CU([Casos<br/>de Uso])

    CMP([Componentes<br/>Software])

    GH([Issues<br/>GitHub])

    TEST([Casos<br/>de Prueba])

    OBJ --> RF
    RF --> CU
    CU --> CMP
    CMP --> GH
    GH --> TEST

    classDef blue fill:#dbeafe,stroke:#2563eb,stroke-width:2px;
    classDef green fill:#ecfccb,stroke:#65a30d,stroke-width:2px;

    class OBJ,RF,CU blue;
    class CMP,GH,TEST green;
```
