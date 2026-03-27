
import streamlit as st

def show(df):
    st.title("Descriptive Analysis")
    st.write(df.head())
