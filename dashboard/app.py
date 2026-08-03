import sys
from pathlib import Path

# Add the project root to Python's import path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

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