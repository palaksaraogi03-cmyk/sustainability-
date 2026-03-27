import streamlit as st
import plotly.express as px

def show(df):
    st.title("🌱 Sustainable Marketplace Dashboard")

    st.markdown("### 📊 Executive Summary")

    # KPIs
    high_intent = (df['Purchase_Intent'] > 3).mean() * 100
    avg_awareness = df['Awareness'].mean()
    avg_price_sensitivity = df['Price_Sensitivity'].mean()

    col1, col2, col3 = st.columns(3)

    col1.metric("High Purchase Intent (%)", f"{high_intent:.1f}%")
    col2.metric("Avg Awareness", f"{avg_awareness:.2f}")
    col3.metric("Price Sensitivity", f"{avg_price_sensitivity:.2f}")

    st.markdown("---")

    # Pie Chart
    st.subheader("🛍️ Popular Product Categories")
    fig = px.pie(df, names="Preferred_Category")
    st.plotly_chart(fig)

    # Insights
    st.markdown("### 🔍 Key Insights")

    st.write("""
    - There is strong demand for sustainable products in the UAE.
    - A significant portion of users show high purchase intent.
    - Price sensitivity remains a major barrier to adoption.
    - Awareness levels directly impact buying behavior.
    """)

    st.markdown("### 🚀 Business Opportunity")

    st.success("""
    Target price-sensitive but environmentally conscious users with:
    - Discounts
    - Bundles
    - Educational content
    """)
