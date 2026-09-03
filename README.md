# 🏭 Manufacturing Analytics Dashboard

An end-to-end analytics platform for a multi-factory manufacturing operation — from a normalized MySQL schema and synthetic data generators, through a Python analytics layer, to an interactive Streamlit dashboard covering production, quality, machines, and workforce performance.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📸 Screenshots

> _Add screenshots here once the app is running locally — see [Adding Screenshots](#adding-screenshots) below._

| Overview | Quality & Trends |
|---|---|
| `docs/screenshots/overview.png` | `docs/screenshots/quality.png` |

---

## 🧭 Overview

This project simulates a manufacturing analytics stack for **5 factories** across India (Chennai, Hosur, Bengaluru, Pune, Ahmedabad), tracking:

- **Production** — batches, units produced, defective units, production hours
- **Quality** — inspection results and factory-level defect rates
- **Machines** — status (Running / Idle / Under Maintenance / Retired), type, age
- **Workforce** — employees, shifts, top performers
- **Maintenance** — preventive/corrective/emergency service history

The dashboard lets a plant manager filter all of the above by **factory**, **shift**, **machine status**, and **date range**, and see KPIs, trends, and rankings update live.

---

## 🏗️ Architecture

```
generators/         → synthetic data generation (CSV) for factories, machines,
                       employees, products, shifts, production batches, maintenance
        │
        ▼
data/raw/*.csv       → CSV → imported into MySQL (see database/schema.sql)
        │
        ▼
database/            → schema definition + connection layer (db_connection.py)
        │
        ▼
analytics/           → SQL query layer, one module per domain:
                       production.py · quality.py · factories.py ·
                       machines.py · employees.py · trends.py
        │
        ▼
dashboard/
  dashboard_service.py → thin facade exposing analytics to the UI
  app.py                → Streamlit page: filters, KPIs, charts, tables
  charts.py              → Plotly chart builders
  components.py           → reusable UI widgets (metric cards)
  styles.py                → custom CSS
```

See [`docs/architecture-diagram.md`](docs/architecture-diagram.md) for a rendered diagram.

**Design pattern:** the dashboard never talks to SQL directly. `app.py` calls `DashboardService`, which calls the relevant `*Analytics` class, which owns the SQL and returns a pandas `DataFrame`. This keeps the UI, business logic, and data access cleanly separated and easy to test independently.

---

## 🗄️ Database Schema

MySQL schema (`database/schema.sql`) with 8 tables:

`Factories`, `Shifts`, `Employees`, `Machines`, `Products`, `Production_Batches`, `Maintenance`, `Defects`, `Quality_Inspection`

Referential integrity is enforced via foreign keys, and business rules (e.g. `defective_units <= units_produced`, `selling_price >= unit_cost`) are enforced with `CHECK` constraints. Indexes are added on the columns most used for filtering (`production_date`, `maintenance_date`, `inspection_date`, `inspection_result`).

---

## ⚙️ Tech Stack

| Layer | Tools |
|---|---|
| Data generation | Python, pandas, Faker |
| Database | MySQL |
| Analytics layer | Python, pandas, `mysql-connector-python` |
| Dashboard | Streamlit, Plotly |

---

## 🚀 Getting Started

### 1. Clone and install

```bash
git clone https://github.com/<your-username>/manufacturing-analytics.git
cd manufacturing-analytics
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Set up the database

```bash
mysql -u root -p < database/schema.sql
```

### 3. Configure credentials

Copy `.env.example` to `.env` and fill in your MySQL credentials (never commit real credentials):

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=manufacturing_analytics
```

### 4. Generate & load sample data

```bash
python generators/generate_factories.py
python generators/generate_shifts.py
python generators/generate_employees.py
python generators/generate_machines.py
python generators/generate_products.py
python generators/generate_production_batches.py
python generators/generate_maintenance.py
```

> ⚠️ The generator scripts currently write to a hardcoded local path — update `BASE_DATA_PATH` in each script to your own `data/raw/` directory before running. Then import the resulting CSVs into MySQL with `LOAD DATA INFILE` or a tool like MySQL Workbench.

### 5. Run the dashboard

```bash
cd dashboard
streamlit run app.py
```

---

## ✅ Testing Filters

The dashboard supports four independent filters — factory, shift, machine status, and date range — which can combine in many ways. Before deploying, verify at minimum:

- [ ] Each filter alone (factory only, shift only, status only, date range only)
- [ ] All filters combined
- [ ] A factory/shift/date combination with **zero matching rows** (dashboard should show 0s, not crash — `COALESCE`/`NULLIF` in the SQL are there for this)
- [ ] Selecting only one machine status vs. all four
- [ ] A date range narrower than any data (empty result set)
- [ ] Reverse date range (start > end) — the UI now blocks this with a validation message

---

## 📁 Project Structure

```
manufacturing-analytics/
├── analytics/          # SQL query layer
├── dashboard/           # Streamlit app
├── database/             # schema + connection
├── generators/             # synthetic data generation scripts
├── docs/
│   ├── architecture-diagram.md
│   └── screenshots/
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🗺️ Roadmap

- [ ] Parameterize generator scripts (env vars instead of hardcoded paths)
- [ ] Add a Maintenance & Defects tab
- [ ] Add automated tests for the analytics layer (mocked DB)
- [ ] Cache expensive queries with `st.cache_data`

---

## 📄 License

MIT
