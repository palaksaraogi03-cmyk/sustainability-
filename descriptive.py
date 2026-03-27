import streamlit as st
import plotly.express as px

def show(df):
    st.title("📊 Descriptive Analysis")

    st.markdown("### 👥 Customer Demographics")

    col1, col2 = st.columns(2)

    # Age Distribution
    with col1:
        fig_age = px.histogram(df, x="Age", nbins=20, title="Age Distribution")
        st.plotly_chart(fig_age, use_container_width=True)

    # Gender Distribution
    with col2:
        fig_gender = px.pie(df, names="Gender", title="Gender Distribution")
        st.plotly_chart(fig_gender, use_container_width=True)

    st.markdown("---")

    # -----------------------------
    # Awareness & Behavior
    # -----------------------------
    st.markdown("### 🌱 Awareness & Behavior")

    col3, col4 = st.columns(2)

    with col3:
        fig_awareness = px.histogram(df, x="Awareness", title="Awareness Levels")
        st.plotly_chart(fig_awareness, use_container_width=True)

    with col4:
        fig_freq = px.pie(df, names="Purchase_Frequency", title="Purchase Frequency")
        st.plotly_chart(fig_freq, use_container_width=True)

    st.markdown("---")

    # -----------------------------
    # Preferences
    # -----------------------------
    st.markdown("### 🛍️ Product Preferences")

    fig_cat = px.bar(
        df['Preferred_Category'].value_counts().reset_index(),
        x='index',
        y='Preferred_Category',
        labels={'index': 'Category', 'Preferred_Category': 'Count'},
        title="Preferred Categories"
    )
    st.plotly_chart(fig_cat, use_container_width=True)

    st.markdown("---")

    # -----------------------------
    # Income Distribution
    # -----------------------------
    st.markdown("### 💰 Income Distribution")

    fig_income = px.pie(df, names="Income", title="Income Segments")
    st.plotly_chart(fig_income, use_container_width=True)

    st.markdown("---")

    # -----------------------------
    # Insights
    # -----------------------------
    st.markdown("### 🔍 Key Insights")

    st.write("""
    - Majority of users are **young and digitally active**.
    - Awareness of sustainable products is **moderate but growing**.
    - Most users purchase sustainable products **occasionally**.
    - Categories like **Home Products and Personal Care** dominate demand.
    - Middle-income users form the **largest customer base**.
    """)
