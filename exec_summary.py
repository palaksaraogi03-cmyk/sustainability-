
import streamlit as st

def show(df):
    st.title("Executive Summary")
    st.write(df.head())
