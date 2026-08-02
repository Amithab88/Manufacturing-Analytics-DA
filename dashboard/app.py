import streamlit as st
from dashboard_service import DashboardService

st.set_page_config(
    page_title="Manufacturing Analytics Dashboard",
    page_icon="🏭",
    layout="wide"
)

st.title("🏭 Manufacturing Analytics Dashboard")
st.markdown("---")

st.header("Production Summary")

summary = DashboardService.production_summary()

st.dataframe(summary, use_container_width=True)