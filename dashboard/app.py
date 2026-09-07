import sys
from pathlib import Path
from datetime import date

import streamlit as st

from styles import load_css

# -------------------------------------------------
# PROJECT PATH
# -------------------------------------------------

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from dashboard_service import DashboardService
from components import metric_card
from charts import (
    factory_production_chart,
    machine_status_chart,
    monthly_production_chart,
    monthly_defect_chart,
    factory_quality_chart,
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

st.markdown(load_css(), unsafe_allow_html=True)

# -------------------------------------------------
# SIDEBAR FILTERS
# -------------------------------------------------

st.sidebar.title("🏭 Manufacturing Analytics")
st.sidebar.markdown("---")
st.sidebar.header("Filters")

factory_options = ["All"] + DashboardService.get_factory_names()
selected_factory = st.sidebar.selectbox("Select Factory", factory_options)

shift_options = ["All", "Morning", "Afternoon", "Night"]
selected_shift = st.sidebar.selectbox("Select Shift", shift_options)

selected_status = st.sidebar.multiselect(
    "Machine Status",
    ["Running", "Idle", "Under Maintenance", "Retired"],
    default=["Running", "Idle", "Under Maintenance", "Retired"]
)

st.sidebar.markdown("---")
st.sidebar.subheader("📅 Date Range")

start_date = st.sidebar.date_input("Start Date", value=date(2023, 1, 1))
end_date = st.sidebar.date_input("End Date", value=date(2026, 6, 30))

if start_date > end_date:
    st.sidebar.error("Start Date must be before End Date.")
    st.stop()

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
# KPI CARDS — PRODUCTION
# -------------------------------------------------

summary = DashboardService.production_summary(
    selected_factory, selected_shift, selected_status, start_date, end_date
).iloc[0]

col1, col2, col3, col4 = st.columns(4)

with col1:
    metric_card("Total Batches", f"{int(summary['total_batches']):,}")

with col2:
    metric_card("Units Produced", f"{int(summary['total_units_produced']):,}")

with col3:
    metric_card("Defect Rate", f"{summary['defect_rate_percentage']} %")

with col4:
    metric_card("Avg Production Hours", f"{summary['avg_production_hours']:.2f}")

# -------------------------------------------------
# SHIFT PERFORMANCE
# -------------------------------------------------

st.markdown("---")
st.subheader("🕐 Shift Performance")

shift_df = DashboardService.shift_performance(
    selected_shift, selected_factory, start_date, end_date
)
st.dataframe(shift_df, width="stretch", hide_index=True)

# -------------------------------------------------
# FACTORY & MACHINE CHARTS
# -------------------------------------------------

st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏭 Factory Production")
    factory_df = DashboardService.factory_summary(
        selected_factory, selected_shift, selected_status, start_date, end_date
    )
    st.plotly_chart(factory_production_chart(factory_df), width="stretch")

with col2:
    st.subheader("⚙ Machine Status")
    machine_df = DashboardService.machine_status(selected_factory, selected_status)
    st.plotly_chart(machine_status_chart(machine_df), width="stretch")

# -------------------------------------------------
# MONTHLY TRENDS
# -------------------------------------------------

st.markdown("---")
col3, col4 = st.columns(2)

with col3:
    st.subheader("📈 Monthly Production")
    trend_df = DashboardService.monthly_production(
        selected_factory, selected_shift, selected_status, start_date, end_date
    )
    st.plotly_chart(monthly_production_chart(trend_df), width="stretch")

with col4:
    st.subheader("📉 Monthly Defect Trend")
    defect_df = DashboardService.monthly_defects(
        selected_factory, selected_shift, selected_status, start_date, end_date
    )
    st.plotly_chart(monthly_defect_chart(defect_df), width="stretch")

# -------------------------------------------------
# QUALITY ANALYTICS (single section — chart + KPIs + table)
# -------------------------------------------------

st.markdown("---")
st.subheader("🛡️ Quality Summary")

quality = DashboardService.quality_summary(
    selected_factory, selected_shift, selected_status, start_date, end_date
).iloc[0]

col1, col2, col3 = st.columns(3)

with col1:
    metric_card("Total Units Inspected", f"{int(quality['total_units_produced']):,}")

with col2:
    metric_card("Total Defective Units", f"{int(quality['total_defective_units']):,}")

with col3:
    metric_card("Quality Defect Rate", f"{quality['defect_rate_percentage']} %")

st.subheader("🏭 Factory Quality Performance")

factory_quality_df = DashboardService.factory_quality(
    selected_factory, selected_shift, selected_status, start_date, end_date
)

st.plotly_chart(factory_quality_chart(factory_quality_df), width="stretch")
st.dataframe(factory_quality_df, width="stretch", hide_index=True)

# -------------------------------------------------
# TOP EMPLOYEES
# -------------------------------------------------

st.markdown("---")
st.subheader("🏆 Top Performing Employees")

employee_df = DashboardService.top_employees(
    10, selected_factory, selected_shift, selected_status
)

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(top_employees_chart(employee_df), width="stretch")

with col2:
    st.dataframe(employee_df, width="stretch", hide_index=True)
