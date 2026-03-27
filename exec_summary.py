import streamlit as st
import plotly.express as px

# -----------------------------
# HEADER
# -----------------------------
def header():
    col1, col2 = st.columns([1, 6])

    with col1:
        st.image("logo.png", width=60)

    with col2:
        st.markdown("## EcoSense AI")


# -----------------------------
# MAIN FUNCTION
# -----------------------------
def show(df):

    header()
    st.markdown("---")

    st.title("📊 Executive Summary")
    st.caption("Key insights and market overview")

    # -----------------------------
    # KPI
    # -----------------------------
    high_intent = (df['Purchase_Intent'] > 3).mean() * 100
    avg_awareness = df['Awareness'].mean()
    avg_price = df['Price_Sensitivity'].mean()

    col1, col2, col3 = st.columns(3)

    col1.metric("High Intent Users", f"{high_intent:.1f}%")
    col2.metric("Avg Awareness", f"{avg_awareness:.2f}")
    col3.metric("Price Sensitivity", f"{avg_price:.2f}")

    st.markdown("---")

    # -----------------------------
    # PIE CHART (PASTEL)
    # -----------------------------
    st.markdown("### 🛍️ Product Preferences")

    fig = px.pie(
        df,
        names="Preferred_Category",
        color_discrete_sequence=[
            "#52b788",
            "#74c69d",
            "#95d5b2",
            "#d8f3dc"
        ]
    )

    fig.update_traces(textinfo="percent+label")

    fig.update_layout(
        template="simple_white",
        paper_bgcolor="#f7fcf9",
        plot_bgcolor="#f7fcf9",
        font=dict(color="#1b4332")
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # -----------------------------
    # SCATTER
    # -----------------------------
    st.markdown("### 📈 Awareness vs Purchase Intent")

    fig2 = px.scatter(
        df,
        x="Awareness",
        y="Purchase_Intent",
        color_discrete_sequence=["#74c69d"],
        opacity=0.6
    )

    fig2.update_layout(
        template="simple_white",
        paper_bgcolor="#f7fcf9",
        plot_bgcolor="#f7fcf9",
        font=dict(color="#1b4332")
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # -----------------------------
    # INSIGHTS
    # -----------------------------
    st.markdown("### 🔍 Key Insights")

    st.markdown("""
- Strong demand for sustainable products  
- Awareness drives purchase behavior  
- Price sensitivity is a key barrier  
""")

    st.markdown("---")

    # -----------------------------
    # STRATEGY
    # -----------------------------
    st.markdown("### 🚀 Strategic Opportunity")

    st.success("""
Focus on **price-sensitive but aware users**:

• Offer discounts  
• Build trust  
• Educate customers  

👉 Highest ROI segment
""")
