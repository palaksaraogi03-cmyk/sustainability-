import streamlit as st
import pandas as pd

# IMPORT ALL PAGES
import exec_summary
import descriptive
import clustering
import association
import prediction
import prescriptive
import scorer

from utils import load_data

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="EcoSense AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# GLOBAL PASTEL THEME
# -----------------------------
st.markdown("""
<style>

/* Background */
.stApp {
    background-color: #f7fcf9;
}

/* Headings */
h1, h2, h3 {
    color: #1b4332;
}

/* Metric Cards */
[data-testid="stMetric"] {
    background-color: #e6f4ea;
    padding: 12px;
    border-radius: 10px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #ffffff;
}

/* Buttons */
.stButton>button {
    background-color: #74c69d;
    color: white;
    border-radius: 8px;
    border: none;
}

/* Tables */
[data-testid="stDataFrame"] {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# LOAD DATA
# -----------------------------
df = load_data()

# -----------------------------
# SIDEBAR BRANDING
# -----------------------------
try:
    st.sidebar.image("logo.png", width=120)
except:
    pass

st.sidebar.markdown("## 🌱 EcoSense AI")
st.sidebar.caption("Sustainable Intelligence Platform")

st.sidebar.markdown("---")

# -----------------------------
# NAVIGATION
# -----------------------------
page = st.sidebar.radio(
    "Navigate",
    [
        "Executive Summary",
        "Descriptive Analysis",
        "Clustering",
        "Association Rules",
        "Prediction Models",
        "Prescriptive Analysis",
        "New Customer Scorer"
    ]
)

# -----------------------------
# PAGE ROUTING (VERY IMPORTANT)
# -----------------------------
if page == "Executive Summary":
    exec_summary.show(df)

elif page == "Descriptive Analysis":
    descriptive.show(df)

elif page == "Clustering":
    clustering.show(df)

elif page == "Association Rules":
    association.show(df)

elif page == "Prediction Models":
    prediction.show(df)

elif page == "Prescriptive Analysis":
    prescriptive.show(df)

elif page == "New Customer Scorer":
    scorer.show(df)
