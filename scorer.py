
import streamlit as st

def show(df):
    st.title("New Customer Scorer")
    st.write(df.head())
