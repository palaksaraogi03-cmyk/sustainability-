import streamlit as st
import pandas as pd

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
# GLOBAL THEME (PASTEL GREEN)
# -----------------------------
st.markdown("""
<style>

/* Background */
.stApp {
    background-color: #f6fbf7;
}

/* Titles */
h1, h2, h3 {
    color: #1B5E20;
}

/* Metric Cards */
[data-testid="stMetric"] {
    background-color: #E8F5E9;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #ffffff;
}

/* Buttons */
.stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 10px;
    border: none;
}

/* Tables */
[data-testid="stDataFrame"] {
    background-color: #ffffff;
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
st.sidebar.image("logo.png", width=120)
st.sidebar.markdown("## 🌱 EcoSense AI")
st.sidebar.caption("Sustainable Intelligence Platform")

st.sidebar.markdown("---")

# -----------------------------
# NAVIGATION
# -----------------------------
page = st.sidebar.radio(
    "Go to",
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
# ROUTING
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
