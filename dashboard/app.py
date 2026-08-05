import streamlit as st
import sys
from pathlib import Path

from styles import load_css

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from dashboard_service import DashboardService
from components import metric_card
from charts import (
    factory_production_chart,
    machine_status_chart,
    monthly_production_chart,
    monthly_defect_chart
)

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------

st.set_page_config(
    page_title="Manufacturing Analytics Dashboard",
    page_icon="🏭",
    layout="wide"
)

# Load CSS before rendering anything
st.markdown(load_css(), unsafe_allow_html=True)

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------

st.sidebar.title("🏭 Manufacturing Analytics")

st.sidebar.markdown("---")

st.sidebar.header("Filters")

factory_options = [
    "All",
    "Chennai",
    "Hosur",
    "Bengaluru",
    "Pune",
    "Ahmedabad"
]

selected_factory = st.sidebar.selectbox(
    "Select Factory",
    factory_options
)

shift_options = [
    "All",
    "Morning",
    "Evening",
    "Night"
]

selected_shift = st.sidebar.selectbox(
    "Select Shift",
    shift_options
)

selected_status = st.sidebar.multiselect(
    "Machine Status",
    [
        "Running",
        "Idle",
        "Under Maintenance",
        "Retired"
    ],
    default=[
        "Running",
        "Idle",
        "Under Maintenance",
        "Retired"
    ]
)

# -------------------------------------------------
# HEADER
# -------------------------------------------------

st.title("🏭 Manufacturing Analytics Dashboard")

st.caption(
    "Executive overview of production, quality, machines, factories, and workforce performance."
)

st.markdown("---")

# -------------------------------------------------
# KPI CARDS
# -------------------------------------------------

summary = DashboardService.production_summary().iloc[0]

col1, col2, col3, col4 = st.columns(4)

with col1:
    metric_card(
        "Total Batches",
        f"{int(summary['total_batches']):,}"
    )

with col2:
    metric_card(
        "Units Produced",
        f"{int(summary['total_units_produced']):,}"
    )

with col3:
    metric_card(
        "Defect Rate",
        f"{summary['defect_rate_percentage']} %"
    )

with col4:
    metric_card(
        "Avg Production Hours",
        f"{summary['avg_production_hours']:.2f}"
    )

# -------------------------------------------------
# FACTORY & MACHINE CHARTS
# -------------------------------------------------

st.markdown("---")

col1, col2 = st.columns(2)

with col1:

    st.subheader("🏭 Factory Production")

    factory_df = DashboardService.factory_summary()

    factory_fig = factory_production_chart(factory_df)

    st.plotly_chart(factory_fig, use_container_width=True)

with col2:

    st.subheader("⚙ Machine Status")

    machine_df = DashboardService.machine_status()

    machine_fig = machine_status_chart(machine_df)

    st.plotly_chart(machine_fig, use_container_width=True)

# -------------------------------------------------
# MONTHLY TRENDS
# -------------------------------------------------

st.markdown("---")

col3, col4 = st.columns(2)

with col3:

    st.subheader("📈 Monthly Production")

    trend_df = DashboardService.monthly_production()

    trend_fig = monthly_production_chart(trend_df)

    st.plotly_chart(trend_fig, use_container_width=True)

with col4:

    st.subheader("📉 Monthly Defect Trend")

    defect_df = DashboardService.monthly_defects()

    defect_fig = monthly_defect_chart(defect_df)

    st.plotly_chart(defect_fig, use_container_width=True)

# -------------------------------------------------
# TOP EMPLOYEES
# -------------------------------------------------

st.markdown("---")

st.subheader("🏆 Top Performing Employees")

employee_df = DashboardService.top_employees()

st.dataframe(
    employee_df,
    use_container_width=True,
    hide_index=True
)
