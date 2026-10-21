flowchart TB

    DJ((DJ))

    subgraph Sistema
        SG((SetlistGen))
    end

    FS((Sistema de<br/>Archivos Local))
    RB((Rekordbox))

    DJ -->|Configura<br/>generación| SG
    DJ -->|Consulta<br/>resultados| SG

    FS -->|Biblioteca<br/>musical| SG
    SG -->|Setlists<br/>exportados| FS

    SG -->|XML<br/>generado| RB
    RB -->|Datos de<br/>referencia| SG

    %% Colores
    classDef dj fill:#DBEAFE,stroke:#2563EB,stroke-width:3px,color:#000;
    classDef sistema fill:#DCFCE7,stroke:#16A34A,stroke-width:3px,color:#000;
    classDef archivos fill:#FED7AA,stroke:#EA580C,stroke-width:3px,color:#000;
    classDef rekordbox fill:#FECACA,stroke:#DC2626,stroke-width:3px,color:#000;

    class DJ dj;
    class SG sistema;
    class FS archivos;
    class RB rekordbox;

    %% Estilo enlaces
    linkStyle 0 stroke:#4B5563,stroke-width:2px;
    linkStyle 1 stroke:#4B5563,stroke-width:2px;
    linkStyle 2 stroke:#4B5563,stroke-width:2px;
    linkStyle 3 stroke:#4B5563,stroke-width:2px;
    linkStyle 4 stroke:#4B5563,stroke-width:2px;
    linkStyle 5 stroke:#4B5563,stroke-width:2px;
