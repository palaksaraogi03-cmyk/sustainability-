
import streamlit as st

def show(df):
    st.title("Association Rules")
    st.write(df.head())
