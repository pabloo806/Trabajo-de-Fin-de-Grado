```mermaid
flowchart TB

    DJ[DJ]

    subgraph Sistema
        SG[SetlistGen]
    end

    FS[Sistema de<br/>Archivos Local]
    RB[Rekordbox]

    DJ -->|Configura<br/>generacion| SG
    DJ -->|Consulta<br/>resultados| SG

    FS -->|Biblioteca<br/>musical| SG
    SG -->|Setlists<br/>exportados| FS

    SG -->|XML<br/>generado| RB
    RB -->|Datos de<br/>referencia| SG
```
