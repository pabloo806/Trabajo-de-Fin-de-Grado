flowchart TB

    DJ([DJ])

    FS["(Biblioteca Musical Local)"]
    RB([Rekordbox])

    subgraph O1["O1 - Importación"]
        RF1["RF-01 · RF-02 · RF-03"]
    end

    subgraph O2["O2 - Análisis Musical"]
        RF2["RF-04 · RF-05 · RF-06 · RF-07"]
    end

    subgraph O3["O3 - Base de Datos"]
        RF3["RF-08 · RF-09 · RF-09b · RF-10 · RF-11 · RF-11b"]
    end

    subgraph O4["O4 - Generador de Setlists"]
        RF4["RF-12 · RF-13 · RF-14 · RF-15 · RF-16 · RF-17 · RF-18 · RF-19 · RF-20 · RF-20b"]
    end

    subgraph O5["O5 - Exportación"]
        RF5["RF-21 · RF-22 · RF-23"]
    end

    subgraph O6["O6 - Panel y Estadísticas"]
        RF6["RF-24 · RF-25 · RF-26 · RF-27 · RF-28"]
    end

    subgraph O7["O7 - Evaluación"]
        RF7["RF-29"]
    end

    DJ --> O1
    DJ --> O4
    DJ --> O6

    FS --> O1

    O1 --> O2
    O2 --> O3

    O3 --> O4
    O3 --> O6

    O4 --> O5
    O5 --> RB

    RB --> O7
    O3 --> O7

    subgraph CA["Clean Architecture"]

        P["Presentación"]

        A["Aplicación<br/>Casos de Uso<br/>Puertos"]

        D["Dominio<br/>Reglas de negocio<br/>Camelot<br/>Generación"]

        I["Infraestructura<br/>Audio<br/>BBDD<br/>XML"]

        P --> A
        A --> D
        I --> A

    end

    O1 -.-> I
    O2 -.-> I
    O3 -.-> I

    O4 -.-> D
    O4 -.-> A

    O5 -.-> I

    O6 -.-> A

    O7 -.-> A

    RNF["RNF-01 a RNF-26"]

    RNF --> O1
    RNF --> O2
    RNF --> O3
    RNF --> O4
    RNF --> O5
    RNF --> O6
    RNF --> O7

    %% OBJETIVOS
    style O1 fill:#FEF3C7,stroke:#D97706,stroke-width:3px
    style O2 fill:#DCFCE7,stroke:#16A34A,stroke-width:3px
    style O3 fill:#DBEAFE,stroke:#2563EB,stroke-width:3px
    style O4 fill:#F3E8FF,stroke:#9333EA,stroke-width:3px
    style O5 fill:#FED7AA,stroke:#EA580C,stroke-width:3px
    style O6 fill:#FCE7F3,stroke:#DB2777,stroke-width:3px
    style O7 fill:#E5E7EB,stroke:#4B5563,stroke-width:3px

    %% ACTORES
    style DJ fill:#DBEAFE,stroke:#2563EB,stroke-width:3px
    style FS fill:#FFEDD5,stroke:#EA580C,stroke-width:3px
    style RB fill:#FECACA,stroke:#DC2626,stroke-width:3px

    %% CLEAN ARCHITECTURE
    style CA fill:#F8FAFC,stroke:#0F172A,stroke-width:3px

    style P fill:#E0F2FE,stroke:#0284C7,stroke-width:2px
    style A fill:#DCFCE7,stroke:#16A34A,stroke-width:2px
    style D fill:#F3E8FF,stroke:#9333EA,stroke-width:2px
    style I fill:#FFEDD5,stroke:#EA580C,stroke-width:2px

    %% RNF
    style RNF fill:#F3F4F6,stroke:#111827,stroke-width:3px
