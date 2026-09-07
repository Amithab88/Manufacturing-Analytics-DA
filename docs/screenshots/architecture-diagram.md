# Architecture

```mermaid
flowchart TD
    A["generators/<br/>Synthetic CSV data (Python + Faker)"] --> B["database/schema.sql<br/>MySQL — 8 normalized tables"]
    B --> C["database/db_connection.py<br/>Connection layer (env-based credentials)"]
    C --> D["analytics/*.py<br/>SQL query layer, one module per domain"]
    D --> E["dashboard_service.py<br/>Facade — UI never touches SQL directly"]
    E --> F["app.py (Streamlit)<br/>Filters, KPIs, Plotly charts, tables"]

    style A fill:#F1EFE8,stroke:#888780
    style B fill:#F1EFE8,stroke:#888780
    style C fill:#E6F1FB,stroke:#378ADD
    style D fill:#E1F5EE,stroke:#1D9E75
    style E fill:#EEEDFE,stroke:#7F77DD
    style F fill:#FAECE7,stroke:#D85A30
```

## Analytics module map

```mermaid
flowchart LR
    S["dashboard_service.py"] --> P["ProductionAnalytics"]
    S --> Fa["FactoryAnalytics"]
    S --> M["MachineAnalytics"]
    S --> Q["QualityAnalytics"]
    S --> Em["EmployeeAnalytics"]
    S --> T["TrendAnalytics"]
```

Each `*Analytics` class owns its own SQL and returns a pandas `DataFrame`. `app.py` only ever calls `DashboardService` — it never imports `analytics/*` directly — which keeps the query logic swappable (e.g. to a different DB, or to cached/precomputed data) without touching the UI.
