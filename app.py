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
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Sustainable Marketplace",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Custom Minimal Theme (🔥 UI Upgrade)
# -----------------------------
st.markdown("""
<style>

    /* Background */
    .stApp {
        background-color: #f8f9fb;
    }

    /* Headings */
    h1, h2, h3 {
        font-weight: 600;
        color: #111827;
    }

    /* Remove top padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Metric Cards */
    [data-testid="stMetric"] {
        background-color: white;
        padding: 18px;
        border-radius: 14px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
        text-align: center;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #eee;
    }

    /* Sidebar text */
    .css-1d391kg {
        font-size: 16px;
    }

    /* Buttons */
    .stButton>button {
        border-radius: 10px;
        background-color: #111827;
        color: white;
        border: none;
        padding: 8px 16px;
    }

    /* Divider spacing */
    hr {
        margin-top: 20px;
        margin-bottom: 20px;
    }

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Load Data
# -----------------------------
df = load_data()

# -----------------------------
# Sidebar Navigation
# -----------------------------
st.sidebar.title("🌿 Navigation")

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
# Page Routing
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
