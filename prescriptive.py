
import streamlit as st

def show(df):
    st.title("Prescriptive Analysis")
    st.write(df.head())
