import streamlit as st
import sys
from pathlib import Path
from datetime import date
from styles import load_css


# -------------------------------------------------
# PROJECT PATH
# -------------------------------------------------

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))


# -------------------------------------------------
# IMPORTS
# -------------------------------------------------

from dashboard_service import DashboardService
from components import metric_card
from charts import (
    factory_production_chart,
    machine_status_chart,
    monthly_production_chart,
    monthly_defect_chart,
    top_employees_chart
)


# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------

st.set_page_config(
    page_title="Manufacturing Analytics Dashboard",
    page_icon="🏭",
    layout="wide"
)


# -------------------------------------------------
# LOAD CSS
# -------------------------------------------------

st.markdown(
    load_css(),
    unsafe_allow_html=True
)


# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------

st.sidebar.title("🏭 Manufacturing Analytics")

st.sidebar.markdown("---")

st.sidebar.header("Filters")

# -------------------------------------------------

# Factory Filter

factory_options = [
    "All"
] + DashboardService.get_factory_names()

selected_factory = st.sidebar.selectbox(
    "Select Factory",
    factory_options
)

# -------------------------------------------------

# Shift Filter

shift_options = [
    "All",
    "Morning",
    "Afternoon",
    "Night"
]

selected_shift = st.sidebar.selectbox(
    "Select Shift",
    shift_options
)

# -------------------------------------------------

# Machine Status Filter

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

# DATE RANGE FILTER

st.sidebar.markdown("---")

st.sidebar.subheader("📅 Date Range")

start_date = st.sidebar.date_input(
    "Start Date",
    value=date(2023, 1, 1)
)

end_date = st.sidebar.date_input(
    "End Date",
    value=date(2026, 6, 30)
)

# -------------------------------------------------
# HEADER
# -------------------------------------------------

st.title("🏭 Manufacturing Analytics Dashboard")

st.caption(
    "Executive overview of production, quality, machines, "
    "factories, and workforce performance."
)

st.markdown("---")


# -------------------------------------------------
# KPI CARDS
# -------------------------------------------------

summary = DashboardService.production_summary(
    selected_factory,
    selected_shift,
    selected_status,
    start_date,
    end_date
).iloc[0]

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
# SHIFT PERFORMANCE
# -------------------------------------------------

st.markdown("---")

st.subheader("🕐 Shift Performance")

shift_df = DashboardService.shift_performance(
    selected_shift,
    selected_factory,
    start_date,
    end_date
)

st.dataframe(
    shift_df,
    width="stretch",
    hide_index=True
)


# -------------------------------------------------
# FACTORY & MACHINE CHARTS
# -------------------------------------------------

st.markdown("---")

col1, col2 = st.columns(2)


# Factory Production
with col1:

    st.subheader("🏭 Factory Production")

    factory_df = DashboardService.factory_summary(
    selected_factory,
    selected_shift,
    selected_status,
    start_date,
    end_date
    )

    factory_fig = factory_production_chart(
        factory_df
    )

    st.plotly_chart(
        factory_fig,
        width="stretch"
    )


# Machine Status
with col2:

    st.subheader("⚙ Machine Status")

    machine_df = DashboardService.machine_status(
        selected_factory,
        selected_status
    )
    machine_fig = machine_status_chart(
        machine_df
    )

    st.plotly_chart(
        machine_fig,
        use_container_width=True
    )


# -------------------------------------------------
# MONTHLY TRENDS
# -------------------------------------------------

st.markdown("---")

col3, col4 = st.columns(2)


# Monthly Production
with col3:

    st.subheader("📈 Monthly Production")

    trend_df = DashboardService.monthly_production(
    selected_factory,
    selected_shift,
    selected_status,
    start_date,
    end_date
    )

    trend_fig = monthly_production_chart(
        trend_df
    )

    st.plotly_chart(
        trend_fig,
        width="stretch"
    )


# Monthly Defects
with col4:

    st.subheader("📉 Monthly Defect Trend")

    defect_df = DashboardService.monthly_defects(
    selected_factory,
    selected_shift,
    selected_status,
    start_date,
    end_date
    )

    defect_fig = monthly_defect_chart(
        defect_df
    )

    st.plotly_chart(
        defect_fig,
        width="stretch"
    )


# -------------------------------------------------
# TOP EMPLOYEES
# -------------------------------------------------

st.markdown("---")

st.subheader("🏆 Top Performing Employees")

employee_df = DashboardService.top_employees(
    10,
    selected_factory,
    selected_shift,
    selected_status
)
st.dataframe(
    employee_df,
    use_container_width=True,
    hide_index=True
)

col1, col2 = st.columns(2)

with col1:

    employee_fig = top_employees_chart(
        employee_df
    )

    st.plotly_chart(
        employee_fig,
        width="stretch"
    )

with col2:

    st.dataframe(
        employee_df,
        width="stretch",
        hide_index=True
    )
