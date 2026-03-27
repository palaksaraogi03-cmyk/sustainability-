import streamlit as st

st.set_page_config(
    page_title="Sustainable Marketplace",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS (🔥 THIS MAKES IT BEAUTIFUL)
st.markdown("""
<style>
    /* Background */
    .stApp {
        background-color: #f8f9fb;
    }

    /* Titles */
    h1, h2, h3 {
        font-weight: 600;
        color: #1f2937;
    }

    /* Cards */
    .block-container {
        padding-top: 2rem;
    }

    /* Metrics */
    [data-testid="stMetric"] {
        background-color: white;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #eee;
    }

    /* Buttons */
    .stButton>button {
        border-radius: 10px;
        background-color: #111827;
        color: white;
    }
</style>
""", unsafe_allow_html=True)
