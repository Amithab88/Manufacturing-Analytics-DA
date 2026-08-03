import streamlit as st
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from dashboard_service import DashboardService
from components import metric_card
from charts import factory_production_chart

st.set_page_config(
    page_title="Manufacturing Analytics Dashboard",
    page_icon="🏭",
    layout="wide"
)

st.title("🏭 Manufacturing Analytics Dashboard")
st.markdown("---")

summary = DashboardService.production_summary()

summary = summary.iloc[0]

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
        round(summary["avg_production_hours"],2)
    )

st.markdown("---")

st.subheader("🏭 Factory-wise Production")

factory_df = DashboardService.factory_summary()

fig = factory_production_chart(factory_df)

st.plotly_chart(fig, use_container_width=True)