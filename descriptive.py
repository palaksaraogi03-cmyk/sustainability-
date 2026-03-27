import streamlit as st
import plotly.express as px

def show(df):
    st.title("📊 Descriptive Analysis")
    st.caption("Understanding customer demographics, behavior, and preferences")

    st.markdown(" ")

    # -----------------------------
    # Demographics
    # -----------------------------
    st.markdown("### 👥 Customer Demographics")

    col1, col2 = st.columns(2)

    # Age Distribution
    with col1:
        fig_age = px.histogram(df, x="Age", nbins=20)
        fig_age.update_layout(
            template="simple_white",
            margin=dict(l=10, r=10, t=30, b=10)
        )
        st.plotly_chart(fig_age, use_container_width=True)

    # Gender Distribution
    with col2:
        fig_gender = px.pie(df, names="Gender")
        fig_gender.update_layout(
            template="simple_white",
            margin=dict(l=10, r=10, t=30, b=10)
        )
        st.plotly_chart(fig_gender, use_container_width=True)

    st.markdown("---")

    # -----------------------------
    # Awareness & Behavior
    # -----------------------------
    st.markdown("### 🌱 Awareness & Behavior")

    col3, col4 = st.columns(2)

    # Awareness Levels
    with col3:
        fig_awareness = px.histogram(df, x="Awareness")
        fig_awareness.update_layout(
            template="simple_white",
            margin=dict(l=10, r=10, t=30, b=10)
        )
        st.plotly_chart(fig_awareness, use_container_width=True)

    # Purchase Frequency
    with col4:
        fig_freq = px.pie(df, names="Purchase_Frequency")
        fig_freq.update_layout(
            template="simple_white",
            margin=dict(l=10, r=10, t=30, b=10)
        )
        st.plotly_chart(fig_freq, use_container_width=True)

    st.markdown("---")

    # -----------------------------
    # Product Preferences
    # -----------------------------
    st.markdown("### 🛍️ Product Preferences")

    cat_df = df['Preferred_Category'].value_counts().reset_index()
    cat_df.columns = ['Category', 'Count']

    fig_cat = px.bar(cat_df, x='Category', y='Count')

    fig_cat.update_layout(
        template="simple_white",
        margin=dict(l=10, r=10, t=30, b=10)
    )

    st.plotly_chart(fig_cat, use_container_width=True)

    st.markdown("---")

    # -----------------------------
    # Income Distribution
    # -----------------------------
    st.markdown("### 💰 Income Distribution")

    fig_income = px.pie(df, names="Income")
    fig_income.update_layout(
        template="simple_white",
        margin=dict(l=10, r=10, t=30, b=10)
    )

    st.plotly_chart(fig_income, use_container_width=True)

    st.markdown("---")

    # -----------------------------
    # Key Insights (Minimal + Clean)
    # -----------------------------
    st.markdown("### 🔍 Key Insights")

    st.markdown("""
- Majority of users are **young and digitally active**  
- Awareness of sustainable products is **moderate but growing**  
- Most users purchase sustainable products **occasionally**  
- **Home Products and Personal Care** lead demand  
- Middle-income users dominate the customer base  
""")
