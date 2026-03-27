
import streamlit as st
import pandas as pd
from utils import load_data
from pages import exec_summary, descriptive, clustering, association, prediction, prescriptive, scorer

st.set_page_config(page_title="Sustainable Marketplace Analytics", layout="wide")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "Executive Summary",
    "Descriptive Analysis",
    "Clustering",
    "Association Rules",
    "Prediction Models",
    "Prescriptive Analysis",
    "New Customer Scorer"
])

df = load_data()

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
